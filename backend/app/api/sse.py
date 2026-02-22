"""SSE subscription manager for real-time application state updates."""
from __future__ import annotations

import asyncio
import json
from typing import AsyncGenerator
from dataclasses import asdict

from app.core.db import get_session
from app.core import services


class SSEPublisher:
    """Manages SSE subscriptions and broadcasts updates."""

    def __init__(self):
        self._subscribers: set[asyncio.Queue] = set()
        self._lock = asyncio.Lock()

    async def subscribe(self) -> AsyncGenerator[dict, None]:
        """Subscribe to application state updates. Yields SSE-formatted events."""
        queue: asyncio.Queue = asyncio.Queue()

        async with self._lock:
            self._subscribers.add(queue)

        try:
            # Send initial state
            data = self._get_current_state()
            yield {"event": "init", "data": json.dumps(data)}

            # Wait for updates
            while True:
                data = await queue.get()
                yield {"event": "update", "data": json.dumps(data)}
        finally:
            async with self._lock:
                self._subscribers.discard(queue)

    async def broadcast(self) -> None:
        """Broadcast current state to all subscribers."""
        if not self._subscribers:
            return

        data = self._get_current_state()

        async with self._lock:
            for queue in self._subscribers:
                try:
                    queue.put_nowait(data)
                except asyncio.QueueFull:
                    pass  # Skip slow clients

    def _get_current_state(self) -> dict:
        """Get current application state matching AppState schema."""
        with get_session() as session:
            # Get graph data
            nodes, dependencies, has_cycles = session.execute_read(services.list_nodes)

            # Get plans
            plans = session.execute_read(services.list_plans)

        # Build parent/child lookup: node_id -> list of dependency IDs
        # Edge: from_id -[DEPENDS_ON]-> to_id means from_id depends on to_id
        # parents = high-level goals that depend on this node (things this node blocks)
        # children = sub-nodes this node depends on (things that block this node)
        parents_map: dict[str, list[str]] = {}   # to_id -> [dep.id, ...] (things that depend on to_id)
        children_map: dict[str, list[str]] = {}  # from_id -> [dep.id, ...] (things from_id depends on)
        for dep in dependencies:
            parents_map.setdefault(dep.to_id, []).append(dep.id)
            children_map.setdefault(dep.from_id, []).append(dep.id)

        # Build plans dict with steps
        plans_dict = {}
        with get_session() as session:
            for plan in plans:
                steps = session.execute_read(
                    lambda tx: services._get_plan_steps(tx, plan.id)
                )
                plans_dict[plan.id] = {
                    "id": plan.id,
                    "text": plan.text,
                    "created_at": plan.created_at,
                    "updated_at": plan.updated_at,
                    "steps": [
                        {
                            "node_id": step.node_id,
                            "order": step.order,
                        }
                        for step in steps
                    ],
                }

        return {
            "tasks": {
                et.node.id: {
                    "id": et.node.id,
                    "text": et.node.text,
                    "node_type": et.node.node_type,
                    "completed": et.node.completed,
                    "due": et.node.due,
                    "created_at": et.node.created_at,
                    "updated_at": et.node.updated_at,
                    "calculated_value": et.calculated_value,
                    "calculated_due": et.calculated_due,
                    "deps_clear": et.deps_clear,
                    "is_actionable": et.is_actionable,
                    "parents": parents_map.get(et.node.id, []),
                    "children": children_map.get(et.node.id, []),
                }
                for et in nodes
            },
            "dependencies": {
                dep.id: {
                    "id": dep.id,
                    "from_id": dep.from_id,
                    "to_id": dep.to_id,
                    "created_at": dep.created_at,
                }
                for dep in dependencies
            },
            "has_cycles": has_cycles,
            "plans": plans_dict,
        }


class DisplaySSEPublisher:
    """Manages SSE subscriptions for display layer (views) updates."""

    def __init__(self):
        self._subscribers: set[asyncio.Queue] = set()
        self._lock = asyncio.Lock()

    async def subscribe(self) -> AsyncGenerator[dict, None]:
        """Subscribe to display state updates. Yields SSE-formatted events."""
        queue: asyncio.Queue = asyncio.Queue()

        async with self._lock:
            self._subscribers.add(queue)

        try:
            data = self._get_current_display_state()
            yield {"event": "init", "data": json.dumps(data)}

            while True:
                data = await queue.get()
                yield {"event": "update", "data": json.dumps(data)}
        finally:
            async with self._lock:
                self._subscribers.discard(queue)

    async def broadcast(self) -> None:
        """Broadcast current display state to all subscribers."""
        if not self._subscribers:
            return

        data = self._get_current_display_state()

        async with self._lock:
            for queue in self._subscribers:
                try:
                    queue.put_nowait(data)
                except asyncio.QueueFull:
                    pass

    def _get_current_display_state(self) -> dict:
        """Get current display state matching ViewListOut schema."""
        with get_session() as session:
            views = session.execute_read(services.list_views)

        return {
            "views": {
                view.id: {
                    "id": view.id,
                    "positions": view.positions,
                    "whitelist": view.whitelist,
                    "blacklist": view.blacklist,
                    "created_at": view.created_at,
                    "updated_at": view.updated_at,
                }
                for view in views
            }
        }


# Global publisher instances
publisher = SSEPublisher()
display_publisher = DisplaySSEPublisher()
