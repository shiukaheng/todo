"""Pydantic models for API - UPDATED FOR BOOLEAN GRAPH."""
from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field


# NEW: Node type enum
class NodeType(str, Enum):
    """Node type labels."""
    TASK = "Task"
    AND = "And"
    OR = "Or"
    NOT = "Not"
    EXACTLY_ONE = "ExactlyOne"


class NodeBase(BaseModel):
    """Base node properties."""
    text: str | None = None
    completed: int | None = None  # Unix timestamp when completed (null = not completed)
    node_type: NodeType = NodeType.TASK  # NEW: replaces 'inferred'
    due: int | None = None


class NodeCreate(NodeBase):
    """Node creation request."""
    id: str
    depends: list[str] | None = None  # Still using depends/blocks (DEPENDS_ON relationship)
    blocks: list[str] | None = None


class NodeUpdate(BaseModel):
    """Node update request."""
    text: str | None = None
    completed: int | None = None
    node_type: NodeType | None = None  # NEW: can change node type
    due: int | None = None


class NodeOut(BaseModel):
    """Node response with calculated fields."""
    id: str
    text: str
    node_type: NodeType  # NEW: derived from labels
    completed: int | None  # Unix timestamp when completed (None = not completed / gate node)
    due: int | None
    created_at: int | None
    updated_at: int | None
    calculated_value: bool | None  # NEW: renamed from calculated_completed
    calculated_due: int | None
    deps_clear: bool | None
    is_actionable: bool | None  # NEW: only true for Tasks that are incomplete and unblocked
    parents: list[str]    # dependency IDs where this node is to_id
    children: list[str]   # dependency IDs where this node is from_id


class DependencyOut(BaseModel):
    """Dependency relationship."""
    id: str
    from_id: str
    to_id: str
    created_at: int | None = None


class NodeListOut(BaseModel):
    """Node list response."""
    tasks: dict[str, NodeOut]  # Keep name 'tasks' for backward compatibility
    dependencies: dict[str, DependencyOut]
    has_cycles: bool


class LinkRequest(BaseModel):
    """Link/unlink request."""
    from_id: str
    to_id: str


class RenameRequest(BaseModel):
    """Rename request."""
    new_id: str


class OperationResult(BaseModel):
    """Generic operation result."""
    success: bool
    message: str | None = None


# ============================================================================
# Plan Models
# ============================================================================


class StepData(BaseModel):
    """Step in a plan."""
    node_id: str
    order: float


class PlanCreate(BaseModel):
    """Create a plan with steps."""
    id: str
    text: str | None = None
    steps: list[StepData] = []


class PlanUpdate(BaseModel):
    """Update a plan (text and/or steps)."""
    text: str | None = None
    steps: list[StepData] | None = None


class PlanOut(BaseModel):
    """Plan response."""
    id: str
    text: str | None
    created_at: int
    updated_at: int
    steps: list[StepData]


class PlanListOut(BaseModel):
    """All plans."""
    plans: dict[str, PlanOut]


# ============================================================================
# Combined State (for /state endpoint and subscription)
# ============================================================================


class AppState(BaseModel):
    """Complete application state (graph + plans)."""
    tasks: dict[str, NodeOut]
    dependencies: dict[str, DependencyOut]
    has_cycles: bool
    plans: dict[str, PlanOut]


# Backward compatibility aliases (optional)
TaskCreate = NodeCreate
TaskUpdate = NodeUpdate
TaskOut = NodeOut
TaskListOut = NodeListOut


# ============================================================================
# Batch Operation Models
# ============================================================================


class CreateNodeOp(BaseModel):
    """Create a node."""
    op: Literal["create_node"]
    id: str
    text: str | None = None
    completed: int | None = None
    node_type: NodeType = NodeType.TASK
    due: int | None = None
    depends: list[str] | None = None
    blocks: list[str] | None = None


class UpdateNodeOp(BaseModel):
    """Update a node."""
    op: Literal["update_node"]
    id: str
    text: str | None = None
    completed: int | None = None
    node_type: NodeType | None = None
    due: int | None = None


class DeleteNodeOp(BaseModel):
    """Delete a node."""
    op: Literal["delete_node"]
    id: str


class RenameNodeOp(BaseModel):
    """Rename a node."""
    op: Literal["rename_node"]
    id: str
    new_id: str


class LinkOp(BaseModel):
    """Create a dependency link."""
    op: Literal["link"]
    from_id: str
    to_id: str


class UnlinkOp(BaseModel):
    """Remove a dependency link."""
    op: Literal["unlink"]
    from_id: str
    to_id: str


class CreatePlanOp(BaseModel):
    """Create a plan."""
    op: Literal["create_plan"]
    id: str
    text: str | None = None
    steps: list[StepData] = []


class UpdatePlanOp(BaseModel):
    """Update a plan."""
    op: Literal["update_plan"]
    id: str
    text: str | None = None
    steps: list[StepData] | None = None


class DeletePlanOp(BaseModel):
    """Delete a plan."""
    op: Literal["delete_plan"]
    id: str


class RenamePlanOp(BaseModel):
    """Rename a plan."""
    op: Literal["rename_plan"]
    id: str
    new_id: str


BatchOperation = Annotated[
    Union[
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
    ],
    Field(discriminator="op"),
]


class BatchRequest(BaseModel):
    """Batch of operations to execute atomically."""
    operations: list[BatchOperation]


class BatchOperationResult(BaseModel):
    """Result of a single operation in a batch."""
    op: str
    success: bool
    message: str | None = None


class BatchResponse(BaseModel):
    """Response for a batch operation."""
    success: bool
    results: list[BatchOperationResult]
    message: str | None = None


# ============================================================================
# View / Display Layer Models
# ============================================================================


class ViewOut(BaseModel):
    """View response."""
    id: str
    positions: dict  # {nodeId: [x, y], ...}
    whitelist: list[str]
    blacklist: list[str]
    created_at: int | None
    updated_at: int | None


class ViewListOut(BaseModel):
    """All views."""
    views: dict[str, ViewOut]


class CreateViewOp(BaseModel):
    """Create a view."""
    op: Literal["create_view"]
    id: str


class DeleteViewOp(BaseModel):
    """Delete a view."""
    op: Literal["delete_view"]
    id: str


class UpdatePositionsOp(BaseModel):
    """Merge positions into a view."""
    op: Literal["update_positions"]
    view_id: str
    positions: dict  # {nodeId: [x, y], ...}


class RemovePositionsOp(BaseModel):
    """Remove positions from a view."""
    op: Literal["remove_positions"]
    view_id: str
    node_ids: list[str]


class SetWhitelistOp(BaseModel):
    """Replace whitelist of a view."""
    op: Literal["set_whitelist"]
    view_id: str
    node_ids: list[str]


class SetBlacklistOp(BaseModel):
    """Replace blacklist of a view."""
    op: Literal["set_blacklist"]
    view_id: str
    node_ids: list[str]


DisplayBatchOperation = Annotated[
    Union[
        CreateViewOp,
        DeleteViewOp,
        UpdatePositionsOp,
        RemovePositionsOp,
        SetWhitelistOp,
        SetBlacklistOp,
    ],
    Field(discriminator="op"),
]


class DisplayBatchRequest(BaseModel):
    """Batch of display operations to execute atomically."""
    operations: list[DisplayBatchOperation]
