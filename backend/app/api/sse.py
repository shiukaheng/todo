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

    async def subscribe(self) -> AsyncGenerator[str, None]:
        """Subscribe to task updates. Yields SSE-formatted events."""
        queue: asyncio.Queue = asyncio.Queue()

        async with self._lock:
            self._subscribers.add(queue)

        try:
            # Send initial state
            data = self._get_current_state()
            yield f"event: init\ndata: {json.dumps(data)}\n\n"

            # Wait for updates
            while True:
                data = await queue.get()
                yield f"event: update\ndata: {json.dumps(data)}\n\n"
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
        """Get current task list state."""
        with get_session() as session:
            tasks, has_cycles = session.execute_read(services.list_tasks)

        return {
            "tasks": [
                {
                    "task": asdict(et.task),
                    "direct_deps": et.direct_deps,
                    "calculated_completed": et.calculated_completed,
                    "calculated_due": et.calculated_due,
                    "deps_clear": et.deps_clear,
                }
                for et in tasks
            ],
            "has_cycles": has_cycles,
        }


# Global publisher instance
publisher = SSEPublisher()
