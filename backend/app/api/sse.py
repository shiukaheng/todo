"""SSE subscription manager for real-time task updates."""
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
        """Subscribe to task updates. Yields SSE-formatted events."""
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
        """Get current task list state matching TaskListOut schema."""
        with get_session() as session:
            tasks, dependencies, has_cycles = session.execute_read(services.list_tasks)

        # Build parent/child lookup: task_id -> list of dependency IDs
        parents_map: dict[str, list[str]] = {}   # from_id -> [dep.id, ...]
        children_map: dict[str, list[str]] = {}  # to_id -> [dep.id, ...]
        for dep in dependencies:
            parents_map.setdefault(dep.from_id, []).append(dep.id)
            children_map.setdefault(dep.to_id, []).append(dep.id)

        return {
            "tasks": {
                et.task.id: {
                    "id": et.task.id,
                    "text": et.task.text,
                    "completed": et.task.completed,
                    "inferred": et.task.inferred,
                    "due": et.task.due,
                    "created_at": et.task.created_at,
                    "updated_at": et.task.updated_at,
                    "calculated_completed": et.calculated_completed,
                    "calculated_due": et.calculated_due,
                    "deps_clear": et.deps_clear,
                    "parents": parents_map.get(et.task.id, []),
                    "children": children_map.get(et.task.id, []),
                }
                for et in tasks
            },
            "dependencies": {
                dep.id: {
                    "id": dep.id,
                    "from_id": dep.from_id,
                    "to_id": dep.to_id,
                }
                for dep in dependencies
            },
            "has_cycles": has_cycles,
        }


# Global publisher instance
publisher = SSEPublisher()
