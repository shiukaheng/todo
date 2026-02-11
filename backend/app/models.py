"""Pydantic models for API - UPDATED FOR BOOLEAN GRAPH."""
from __future__ import annotations

from enum import Enum
from pydantic import BaseModel


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
    completed: bool = False  # Only used for Task nodes (ignored for gates)
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
    completed: bool | None = None
    node_type: NodeType | None = None  # NEW: can change node type
    due: int | None = None


class NodeOut(BaseModel):
    """Node response with calculated fields."""
    id: str
    text: str
    node_type: NodeType  # NEW: derived from labels
    completed: bool | None  # None for gate nodes
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
