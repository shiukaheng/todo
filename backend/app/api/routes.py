"""API routes."""
from __future__ import annotations

from dataclasses import asdict

from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse

from app.core.db import get_session
from app.core import services
from app.models import (
    TaskCreate,
    TaskUpdate,
    TaskOut,
    EnrichedTaskOut,
    TaskListOut,
    LinkRequest,
    RenameRequest,
    OperationResult,
)
from app.api.sse import publisher

router = APIRouter()


def _enriched_to_out(et: services.EnrichedTask) -> EnrichedTaskOut:
    """Convert EnrichedTask to Pydantic model."""
    return EnrichedTaskOut(
        task=TaskOut(**asdict(et.task)),
        direct_deps=et.direct_deps,
        calculated_completed=et.calculated_completed,
        calculated_due=et.calculated_due,
        deps_clear=et.deps_clear,
    )


# ============================================================================
# Task CRUD
# ============================================================================


@router.get("/tasks", response_model=TaskListOut)
async def list_tasks():
    """List all tasks with computed properties."""
    with get_session() as session:
        tasks, has_cycles = session.execute_read(services.list_tasks)
    return TaskListOut(
        tasks=[_enriched_to_out(t) for t in tasks],
        has_cycles=has_cycles,
    )


@router.post("/tasks", response_model=TaskOut)
async def add_task(req: TaskCreate):
    """Create a new task."""
    try:
        with get_session() as session:
            task = session.execute_write(
                lambda tx: services.add_task(
                    tx,
                    id=req.id,
                    text=req.text,
                    completed=req.completed,
                    inferred=req.inferred,
                    due=req.due,
                    depends=req.depends,
                    blocks=req.blocks,
                )
            )
    except Exception as e:
        if "already exists" in str(e).lower() or "unique" in str(e).lower():
            raise HTTPException(status_code=409, detail=f"Task '{req.id}' already exists")
        raise HTTPException(status_code=400, detail=str(e))

    await publisher.broadcast()
    return TaskOut(**asdict(task))


@router.patch("/tasks/{task_id}", response_model=OperationResult)
async def set_task(task_id: str, req: TaskUpdate):
    """Update a task's properties."""
    with get_session() as session:
        found = session.execute_write(
            lambda tx: services.update_task(
                tx,
                id=task_id,
                text=req.text,
                completed=req.completed,
                inferred=req.inferred,
                due=req.due,
            )
        )

    if not found:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")

    await publisher.broadcast()
    return OperationResult(success=True)


@router.delete("/tasks/{task_id}", response_model=OperationResult)
async def remove_task(task_id: str):
    """Delete a task and its edges."""
    with get_session() as session:
        found = session.execute_write(
            lambda tx: services.remove_task(tx, task_id)
        )

    if not found:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")

    await publisher.broadcast()
    return OperationResult(success=True, message=f"Deleted task '{task_id}'")


@router.post("/tasks/{task_id}/rename", response_model=OperationResult)
async def rename_task(task_id: str, req: RenameRequest):
    """Rename a task (change its ID)."""
    try:
        with get_session() as session:
            session.execute_write(
                lambda tx: services.rename_task(tx, task_id, req.new_id)
            )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    await publisher.broadcast()
    return OperationResult(success=True, message=f"Renamed '{task_id}' to '{req.new_id}'")


# ============================================================================
# Link/Unlink
# ============================================================================


@router.post("/links", response_model=OperationResult)
async def link_tasks(req: LinkRequest):
    """Create a dependency: from_id depends on to_id."""
    try:
        with get_session() as session:
            session.execute_write(
                lambda tx: services.link_tasks(tx, req.from_id, req.to_id)
            )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    await publisher.broadcast()
    return OperationResult(success=True, message=f"{req.from_id} now depends on {req.to_id}")


@router.delete("/links", response_model=OperationResult)
async def unlink_tasks(req: LinkRequest):
    """Remove a dependency."""
    with get_session() as session:
        found = session.execute_write(
            lambda tx: services.unlink_tasks(tx, req.from_id, req.to_id)
        )

    if not found:
        raise HTTPException(status_code=404, detail="Link not found")

    await publisher.broadcast()
    return OperationResult(success=True, message=f"Removed dependency {req.from_id} -> {req.to_id}")


# ============================================================================
# SSE Subscription
# ============================================================================


@router.get("/tasks/subscribe")
async def subscribe_tasks():
    """Subscribe to real-time task updates via SSE."""
    return EventSourceResponse(publisher.subscribe())


# ============================================================================
# Admin
# ============================================================================


@router.post("/init", response_model=OperationResult)
async def init_db():
    """Initialize the database schema."""
    with get_session() as session:
        session.execute_write(services.init_db)
        session.execute_write(services.prime_tokens)
    return OperationResult(success=True, message="Database initialized")
