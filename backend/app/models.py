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
    """Task response."""
    id: str
    text: str
    completed: bool
    inferred: bool
    due: int | None
    created_at: int | None
    updated_at: int | None


class EnrichedTaskOut(BaseModel):
    """Enriched task response with computed properties."""
    task: TaskOut
    direct_deps: list[str]
    calculated_completed: bool | None
    calculated_due: int | None
    deps_clear: bool | None


class TaskListOut(BaseModel):
    """Task list response."""
    tasks: list[EnrichedTaskOut]
    has_cycles: bool


class LinkRequest(BaseModel):
    """Link/unlink request."""
    from_id: str
    to_id: str


class OperationResult(BaseModel):
    """Generic operation result."""
    success: bool
    message: str | None = None
