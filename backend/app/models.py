"""Pydantic models for API."""
from __future__ import annotations

from pydantic import BaseModel


class TaskBase(BaseModel):
    """Base task properties."""
    text: str | None = None
    completed: bool = False
    inferred: bool = False
    due: str | None = None


class TaskCreate(TaskBase):
    """Task creation request."""
    id: str
    depends: list[str] | None = None
    blocks: list[str] | None = None


class TaskUpdate(BaseModel):
    """Task update request."""
    text: str | None = None
    completed: bool | None = None
    inferred: bool | None = None
    due: str | None = None


class TaskOut(BaseModel):
    """Task response with calculated fields."""
    id: str
    text: str
    completed: bool
    inferred: bool
    due: int | None
    created_at: int | None
    updated_at: int | None
    calculated_completed: bool | None
    calculated_due: int | None
    deps_clear: bool | None
    parents: list[str]    # dependency IDs where this task is to_id (high-level goals depending on this)
    children: list[str]   # dependency IDs where this task is from_id (sub-tasks this depends on)


class DependencyOut(BaseModel):
    """Dependency relationship."""
    id: str
    from_id: str
    to_id: str


class TaskListOut(BaseModel):
    """Task list response."""
    tasks: dict[str, TaskOut]
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
