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
    TaskListOut,
    DependencyOut,
    LinkRequest,
    RenameRequest,
    OperationResult,
)
from app.api.sse import publisher

router = APIRouter()


def _enriched_to_out(et: services.EnrichedTask) -> TaskOut:
    """Convert EnrichedTask to Pydantic model."""
    return TaskOut(
        id=et.task.id,
        text=et.task.text,
        completed=et.task.completed,
        inferred=et.task.inferred,
        due=et.task.due,
        created_at=et.task.created_at,
        updated_at=et.task.updated_at,
        calculated_completed=et.calculated_completed,
        calculated_due=et.calculated_due,
        deps_clear=et.deps_clear,
    )


def _dep_to_out(dep: services.Dependency) -> DependencyOut:
    """Convert Dependency to Pydantic model."""
    return DependencyOut(
        id=dep.id,
        from_id=dep.from_id,
        to_id=dep.to_id,
    )


# ============================================================================
# Task CRUD
# ============================================================================


@router.get("/tasks", response_model=TaskListOut)
async def list_tasks():
    """List all tasks with computed properties."""
    with get_session() as session:
        tasks, dependencies, has_cycles = session.execute_read(services.list_tasks)

    # Build parent/child lookup: task_id -> list of dependency IDs
    parents_map: dict[str, list[str]] = {}   # from_id -> [dep.id, ...]
    children_map: dict[str, list[str]] = {}  # to_id -> [dep.id, ...]
    for dep in dependencies:
        parents_map.setdefault(dep.from_id, []).append(dep.id)
        children_map.setdefault(dep.to_id, []).append(dep.id)

    return TaskListOut(
        tasks={
            t.task.id: TaskOut(
                id=t.task.id,
                text=t.task.text,
                completed=t.task.completed,
                inferred=t.task.inferred,
                due=t.task.due,
                created_at=t.task.created_at,
                updated_at=t.task.updated_at,
                calculated_completed=t.calculated_completed,
                calculated_due=t.calculated_due,
                deps_clear=t.deps_clear,
                parents=parents_map.get(t.task.id, []),
                children=children_map.get(t.task.id, []),
            )
            for t in tasks
        },
        dependencies={d.id: _dep_to_out(d) for d in dependencies},
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
    return TaskOut(
        id=task.id,
        text=task.text,
        completed=task.completed,
        inferred=task.inferred,
        due=task.due,
        created_at=task.created_at,
        updated_at=task.updated_at,
        calculated_completed=None,
        calculated_due=None,
        deps_clear=None,
        parents=[],   # caller should re-fetch if depends/blocks were provided
        children=[],
    )


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


@router.post("/links", response_model=DependencyOut)
async def link_tasks(req: LinkRequest):
    """Create a dependency: from_id depends on to_id."""
    try:
        with get_session() as session:
            dep_id = session.execute_write(
                lambda tx: services.link_tasks(tx, req.from_id, req.to_id)
            )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    await publisher.broadcast()
    return DependencyOut(id=dep_id, from_id=req.from_id, to_id=req.to_id)


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
    """Initialize the database schema and run migrations."""
    with get_session() as session:
        session.execute_write(services.init_db)
    with get_session() as session:
        session.execute_write(services.prime_tokens)
    with get_session() as session:
        session.execute_write(services.migrate_dependency_ids)
    return OperationResult(success=True, message="Database initialized")
