"""API routes."""
from __future__ import annotations

import logging
from dataclasses import asdict

from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse

logger = logging.getLogger(__name__)

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


def _enriched_to_out(et: services.EnrichedNode) -> TaskOut:
    """Convert EnrichedNode to Pydantic model."""
    return TaskOut(
        id=et.node.id,
        text=et.node.text,
        node_type=et.node.node_type,
        completed=et.node.completed,
        due=et.node.due,
        created_at=et.node.created_at,
        updated_at=et.node.updated_at,
        calculated_value=et.calculated_value,
        calculated_due=et.calculated_due,
        deps_clear=et.deps_clear,
        is_actionable=et.is_actionable,
    )


def _dep_to_out(dep: services.Dependency) -> DependencyOut:
    """Convert Dependency to Pydantic model."""
    return DependencyOut(
        id=dep.id,
        from_id=dep.from_id,
        to_id=dep.to_id,
    )


# ============================================================================
# SSE Subscription (must be before /tasks/{task_id} to avoid path conflict)
# ============================================================================


@router.get("/tasks/subscribe")
async def subscribe_tasks():
    """Subscribe to real-time task updates via SSE."""
    return EventSourceResponse(publisher.subscribe())


# ============================================================================
# Task CRUD
# ============================================================================


@router.get("/tasks", response_model=TaskListOut)
async def list_tasks():
    """List all tasks with computed properties."""
    with get_session() as session:
        nodes, dependencies, has_cycles = session.execute_read(services.list_nodes)

    # Build parent/child lookup: node_id -> list of dependency IDs
    # Edge: from_id -[DEPENDS_ON]-> to_id means from_id depends on to_id
    # parents = high-level goals that depend on this node (things this node blocks)
    # children = sub-nodes this node depends on (things that block this node)
    parents_map: dict[str, list[str]] = {}   # to_id -> [dep.id, ...] (things that depend on to_id)
    children_map: dict[str, list[str]] = {}  # from_id -> [dep.id, ...] (things from_id depends on)
    for dep in dependencies:
        parents_map.setdefault(dep.to_id, []).append(dep.id)
        children_map.setdefault(dep.from_id, []).append(dep.id)

    return TaskListOut(
        tasks={
            t.node.id: TaskOut(
                id=t.node.id,
                text=t.node.text,
                node_type=t.node.node_type,
                completed=t.node.completed,
                due=t.node.due,
                created_at=t.node.created_at,
                updated_at=t.node.updated_at,
                calculated_value=t.calculated_value,
                calculated_due=t.calculated_due,
                deps_clear=t.deps_clear,
                is_actionable=t.is_actionable,
                parents=parents_map.get(t.node.id, []),
                children=children_map.get(t.node.id, []),
            )
            for t in nodes
        },
        dependencies={d.id: _dep_to_out(d) for d in dependencies},
        has_cycles=has_cycles,
    )


@router.get("/tasks/{task_id}", response_model=TaskOut)
async def get_task(task_id: str):
    """Get a single task with computed properties."""
    with get_session() as session:
        node = session.execute_read(
            lambda tx: services.get_node(tx, task_id)
        )
        if not node:
            raise HTTPException(status_code=404, detail=f"Node '{task_id}' not found")
        # Get dependencies to build parents/children
        dependencies = session.execute_read(services.list_dependencies)

    # Build parent/child lists for this node
    parents = [d.id for d in dependencies if d.to_id == task_id]
    children = [d.id for d in dependencies if d.from_id == task_id]

    return TaskOut(
        id=node.node.id,
        text=node.node.text,
        node_type=node.node.node_type,
        completed=node.node.completed,
        due=node.node.due,
        created_at=node.node.created_at,
        updated_at=node.node.updated_at,
        calculated_value=node.calculated_value,
        calculated_due=node.calculated_due,
        deps_clear=node.deps_clear,
        is_actionable=node.is_actionable,
        parents=parents,
        children=children,
    )


@router.post("/tasks", response_model=TaskOut)
async def add_task(req: TaskCreate):
    """Create a new task."""
    try:
        with get_session() as session:
            node = session.execute_write(
                lambda tx: services.add_node(
                    tx,
                    id=req.id,
                    node_type=req.node_type.value if req.node_type else "Task",
                    text=req.text,
                    completed=req.completed,
                    due=req.due,
                    depends=req.depends,
                    blocks=req.blocks,
                )
            )
    except Exception as e:
        if "already exists" in str(e).lower() or "unique" in str(e).lower():
            raise HTTPException(status_code=409, detail=f"Node '{req.id}' already exists")
        raise HTTPException(status_code=400, detail=str(e))

    await publisher.broadcast()
    return TaskOut(
        id=node.id,
        text=node.text,
        node_type=node.node_type,
        completed=node.completed,
        due=node.due,
        created_at=node.created_at,
        updated_at=node.updated_at,
        calculated_value=None,
        calculated_due=None,
        deps_clear=None,
        is_actionable=None,
        parents=[],   # caller should re-fetch if depends/blocks were provided
        children=[],
    )


@router.patch("/tasks/{task_id}", response_model=OperationResult)
async def set_task(task_id: str, req: TaskUpdate):
    """Update a task's properties."""
    logger.debug(f"Updating task {task_id} with node_type={req.node_type}")
    # Use model_dump to get only fields that were explicitly set
    update_data = req.model_dump(exclude_unset=True)

    # Build kwargs for update_node with only provided fields
    kwargs = {'id': task_id}
    if 'node_type' in update_data:
        kwargs['node_type'] = req.node_type.value if req.node_type else None
    if 'text' in update_data:
        kwargs['text'] = req.text
    if 'completed' in update_data:
        kwargs['completed'] = req.completed
    if 'due' in update_data:
        kwargs['due'] = req.due  # Can be None to clear, or int to set

    with get_session() as session:
        found = session.execute_write(
            lambda tx: services.update_node(tx, **kwargs)
        )

    if not found:
        raise HTTPException(status_code=404, detail=f"Node '{task_id}' not found")

    await publisher.broadcast()
    return OperationResult(success=True)


@router.delete("/tasks/{task_id}", response_model=OperationResult)
async def remove_task(task_id: str):
    """Delete a task and its edges."""
    with get_session() as session:
        found = session.execute_write(
            lambda tx: services.remove_node(tx, task_id)
        )

    if not found:
        raise HTTPException(status_code=404, detail=f"Node '{task_id}' not found")

    await publisher.broadcast()
    return OperationResult(success=True, message=f"Deleted node '{task_id}'")


@router.post("/tasks/{task_id}/rename", response_model=OperationResult)
async def rename_task(task_id: str, req: RenameRequest):
    """Rename a task (change its ID)."""
    try:
        with get_session() as session:
            session.execute_write(
                lambda tx: services.rename_node(tx, task_id, req.new_id)
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
                lambda tx: services.link_nodes(tx, req.from_id, req.to_id)
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
            lambda tx: services.unlink_nodes(tx, req.from_id, req.to_id)
        )

    if not found:
        raise HTTPException(status_code=404, detail="Link not found")

    await publisher.broadcast()
    return OperationResult(success=True, message=f"Removed dependency {req.from_id} -> {req.to_id}")


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
