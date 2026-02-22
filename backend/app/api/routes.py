"""API routes."""
from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException
from sse_starlette.sse import EventSourceResponse

logger = logging.getLogger(__name__)

from app.core.db import get_session
from app.core import services
from app.models import (
    TaskOut,
    TaskListOut,
    DependencyOut,
    OperationResult,
    PlanOut,
    PlanListOut,
    StepData,
    AppState,
    BatchRequest,
    BatchOperationResult,
    BatchResponse,
    CreateNodeOp,
    UpdateNodeOp,
    DeleteNodeOp,
    RenameNodeOp,
    LinkOp,
    UnlinkOp,
    CreatePlanOp,
    UpdatePlanOp,
    DeletePlanOp,
    RenamePlanOp,
    ViewOut,
    ViewListOut,
    DisplayBatchRequest,
    CreateViewOp,
    DeleteViewOp,
    UpdatePositionsOp,
    RemovePositionsOp,
    SetWhitelistOp,
    SetBlacklistOp,
)
from app.api.sse import publisher, display_publisher

router = APIRouter()


def _dep_to_out(dep: services.Dependency) -> DependencyOut:
    """Convert Dependency to Pydantic model."""
    return DependencyOut(
        id=dep.id,
        from_id=dep.from_id,
        to_id=dep.to_id,
        created_at=dep.created_at,
    )


def _step_to_data(step: services.Step) -> StepData:
    """Convert Step to StepData."""
    return StepData(
        node_id=step.node_id,
        order=step.order,
    )


def _plan_to_out(plan: services.Plan, steps: list[services.Step]) -> PlanOut:
    """Convert Plan to Pydantic model."""
    return PlanOut(
        id=plan.id,
        text=plan.text,
        created_at=plan.created_at or 0,
        updated_at=plan.updated_at or 0,
        steps=[_step_to_data(s) for s in steps],
    )


# ============================================================================
# State endpoints
# ============================================================================


@router.get("/state", response_model=AppState)
async def get_state():
    """Get current complete application state (one-shot)."""
    with get_session() as session:
        # Get graph data
        nodes, dependencies, has_cycles = session.execute_read(services.list_nodes)

        # Build parent/child lookup
        parents_map: dict[str, list[str]] = {}
        children_map: dict[str, list[str]] = {}
        for dep in dependencies:
            parents_map.setdefault(dep.to_id, []).append(dep.id)
            children_map.setdefault(dep.from_id, []).append(dep.id)

        # Get plans
        plans = session.execute_read(services.list_plans)

    # Build tasks dict
    tasks_out = {}
    for t in nodes:
        tasks_out[t.node.id] = TaskOut(
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

    # Build plans dict
    plans_out = {}
    with get_session() as session:
        for plan in plans:
            steps = session.execute_read(
                lambda tx: services._get_plan_steps(tx, plan.id)
            )
            plans_out[plan.id] = _plan_to_out(plan, steps)

    return AppState(
        tasks=tasks_out,
        dependencies={d.id: _dep_to_out(d) for d in dependencies},
        has_cycles=has_cycles,
        plans=plans_out,
    )


# ============================================================================
# SSE Subscription (must be before /tasks/{task_id} to avoid path conflict)
# ============================================================================


@router.get("/state/subscribe")
async def subscribe_state():
    """Subscribe to real-time state updates via SSE."""
    return EventSourceResponse(publisher.subscribe())


@router.get("/tasks/subscribe")
async def subscribe_tasks():
    """Subscribe to real-time task updates via SSE (deprecated - use /state/subscribe)."""
    logger.warning("Deprecated: /tasks/subscribe - use /state/subscribe instead")
    return EventSourceResponse(publisher.subscribe())


# ============================================================================
# Read-only Task endpoints
# ============================================================================


@router.get("/tasks", response_model=TaskListOut)
async def list_tasks():
    """List all tasks with computed properties."""
    with get_session() as session:
        nodes, dependencies, has_cycles = session.execute_read(services.list_nodes)

    parents_map: dict[str, list[str]] = {}
    children_map: dict[str, list[str]] = {}
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
        dependencies = session.execute_read(services.list_dependencies)

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


# ============================================================================
# Read-only Plan endpoints
# ============================================================================


@router.get("/plans", response_model=PlanListOut)
async def list_plans():
    """List all plans with their steps."""
    with get_session() as session:
        plans = session.execute_read(services.list_plans)

    plans_out = {}
    with get_session() as session:
        for plan in plans:
            steps = session.execute_read(
                lambda tx: services._get_plan_steps(tx, plan.id)
            )
            plans_out[plan.id] = _plan_to_out(plan, steps)

    return PlanListOut(plans=plans_out)


@router.get("/plans/{plan_id}", response_model=PlanOut)
async def get_plan(plan_id: str):
    """Get a single plan with its steps."""
    with get_session() as session:
        plan = session.execute_read(
            lambda tx: services.get_plan(tx, plan_id)
        )
        if not plan:
            raise HTTPException(status_code=404, detail=f"Plan '{plan_id}' not found")

        steps = session.execute_read(
            lambda tx: services._get_plan_steps(tx, plan_id)
        )

    return _plan_to_out(plan, steps)


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
    with get_session() as session:
        session.execute_write(services.migrate_to_boolean_graph)
    with get_session() as session:
        session.execute_write(services.migrate_completed_bool_to_timestamp)
    with get_session() as session:
        session.execute_write(services.migrate_dependency_created_at)
    return OperationResult(success=True, message="Database initialized and migrated")


# ============================================================================
# Batch Operations
# ============================================================================


def _dispatch_operation(tx, op) -> None:
    """Dispatch a single operation to the appropriate service function."""
    if isinstance(op, CreateNodeOp):
        services.add_node(
            tx,
            id=op.id,
            node_type=op.node_type.value if op.node_type else "Task",
            text=op.text,
            completed=op.completed,
            due=op.due,
            depends=op.depends,
            blocks=op.blocks,
        )
    elif isinstance(op, UpdateNodeOp):
        update_data = op.model_dump(exclude_unset=True)
        kwargs: dict = {"id": op.id}
        if "node_type" in update_data:
            kwargs["node_type"] = op.node_type.value if op.node_type else None
        if "text" in update_data:
            kwargs["text"] = op.text
        if "completed" in update_data:
            kwargs["completed"] = op.completed  # int timestamp or None (to uncomplete)
        if "due" in update_data:
            kwargs["due"] = op.due
        found = services.update_node(tx, **kwargs)
        if not found:
            raise ValueError(f"Node '{op.id}' not found")
    elif isinstance(op, DeleteNodeOp):
        found = services.remove_node(tx, op.id)
        if not found:
            raise ValueError(f"Node '{op.id}' not found")
    elif isinstance(op, RenameNodeOp):
        services.rename_node(tx, op.id, op.new_id)
    elif isinstance(op, LinkOp):
        services.link_nodes(tx, op.from_id, op.to_id)
    elif isinstance(op, UnlinkOp):
        found = services.unlink_nodes(tx, op.from_id, op.to_id)
        if not found:
            raise ValueError(f"Link {op.from_id} -> {op.to_id} not found")
    elif isinstance(op, CreatePlanOp):
        steps_tuples = [(s.node_id, s.order) for s in op.steps] if op.steps else None
        services.create_plan(tx, id=op.id, text=op.text, steps=steps_tuples)
    elif isinstance(op, UpdatePlanOp):
        steps_tuples = None
        if op.steps is not None:
            steps_tuples = [(s.node_id, s.order) for s in op.steps]
        found = services.update_plan(tx, id=op.id, text=op.text, steps=steps_tuples)
        if not found:
            raise ValueError(f"Plan '{op.id}' not found")
    elif isinstance(op, DeletePlanOp):
        found = services.delete_plan(tx, op.id)
        if not found:
            raise ValueError(f"Plan '{op.id}' not found")
    elif isinstance(op, RenamePlanOp):
        services.rename_plan(tx, op.id, op.new_id)
    else:
        raise ValueError(f"Unknown operation type: {type(op)}")


@router.post("/batch", response_model=BatchResponse)
async def batch_operations(req: BatchRequest):
    """Execute multiple operations atomically in a single transaction."""
    results: list[BatchOperationResult] = []

    def _run_all(tx):
        for i, op in enumerate(req.operations):
            try:
                _dispatch_operation(tx, op)
                results.append(BatchOperationResult(op=op.op, success=True))
            except Exception as e:
                # Record failure for this op
                results.append(BatchOperationResult(
                    op=op.op, success=False, message=str(e)
                ))
                # Mark remaining ops as skipped
                for remaining in req.operations[i + 1:]:
                    results.append(BatchOperationResult(
                        op=remaining.op, success=False, message="skipped"
                    ))
                # Re-raise to trigger transaction rollback
                raise

    try:
        with get_session() as session:
            session.execute_write(_run_all)
    except Exception:
        failed = next((r for r in results if not r.success), None)
        return BatchResponse(
            success=False,
            results=results,
            message=failed.message if failed else "unknown error",
        )

    await publisher.broadcast()
    return BatchResponse(success=True, results=results)


# ============================================================================
# Display Layer (Views)
# ============================================================================


def _view_to_out(view: services.View) -> ViewOut:
    """Convert View to Pydantic model."""
    return ViewOut(
        id=view.id,
        positions=view.positions,
        whitelist=view.whitelist,
        blacklist=view.blacklist,
        created_at=view.created_at,
        updated_at=view.updated_at,
    )


@router.get("/views", response_model=ViewListOut)
async def list_views():
    """List all views."""
    with get_session() as session:
        views = session.execute_read(services.list_views)
    return ViewListOut(views={v.id: _view_to_out(v) for v in views})


@router.get("/views/{view_id}", response_model=ViewOut)
async def get_view(view_id: str):
    """Get a single view."""
    with get_session() as session:
        view = session.execute_read(lambda tx: services.get_view(tx, view_id))
    if not view:
        raise HTTPException(status_code=404, detail=f"View '{view_id}' not found")
    return _view_to_out(view)


@router.get("/display/subscribe")
async def subscribe_display():
    """Subscribe to real-time display layer updates via SSE."""
    return EventSourceResponse(display_publisher.subscribe())


def _dispatch_display_operation(tx, op) -> None:
    """Dispatch a single display operation to the appropriate service function."""
    if isinstance(op, CreateViewOp):
        services.create_view(tx, id=op.id)
    elif isinstance(op, DeleteViewOp):
        found = services.delete_view(tx, op.id)
        if not found:
            raise ValueError(f"View '{op.id}' not found")
    elif isinstance(op, UpdatePositionsOp):
        found = services.update_positions(tx, view_id=op.view_id, positions=op.positions)
        if not found:
            raise ValueError(f"View '{op.view_id}' not found")
    elif isinstance(op, RemovePositionsOp):
        found = services.remove_positions(tx, view_id=op.view_id, node_ids=op.node_ids)
        if not found:
            raise ValueError(f"View '{op.view_id}' not found")
    elif isinstance(op, SetWhitelistOp):
        found = services.set_whitelist(tx, view_id=op.view_id, node_ids=op.node_ids)
        if not found:
            raise ValueError(f"View '{op.view_id}' not found")
    elif isinstance(op, SetBlacklistOp):
        found = services.set_blacklist(tx, view_id=op.view_id, node_ids=op.node_ids)
        if not found:
            raise ValueError(f"View '{op.view_id}' not found")
    else:
        raise ValueError(f"Unknown display operation type: {type(op)}")


@router.post("/display/batch", response_model=BatchResponse)
async def display_batch_operations(req: DisplayBatchRequest):
    """Execute multiple display operations atomically in a single transaction."""
    results: list[BatchOperationResult] = []

    def _run_all(tx):
        for i, op in enumerate(req.operations):
            try:
                _dispatch_display_operation(tx, op)
                results.append(BatchOperationResult(op=op.op, success=True))
            except Exception as e:
                results.append(BatchOperationResult(
                    op=op.op, success=False, message=str(e)
                ))
                for remaining in req.operations[i + 1:]:
                    results.append(BatchOperationResult(
                        op=remaining.op, success=False, message="skipped"
                    ))
                raise

    try:
        with get_session() as session:
            session.execute_write(_run_all)
    except Exception:
        failed = next((r for r in results if not r.success), None)
        return BatchResponse(
            success=False,
            results=results,
            message=failed.message if failed else "unknown error",
        )

    await display_publisher.broadcast()
    return BatchResponse(success=True, results=results)
