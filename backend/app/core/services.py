"""Pure functional service layer for task operations."""
from __future__ import annotations

import time
from dataclasses import dataclass, field

from app.core.utils import parse_due, would_create_cycle


@dataclass
class Task:
    """Task data."""
    id: str
    text: str = ""
    completed: bool = False
    inferred: bool = False
    due: int | None = None
    created_at: int | None = None
    updated_at: int | None = None


@dataclass
class EnrichedTask:
    """Task with calculated properties and dependencies."""
    task: Task
    direct_deps: list[str] = field(default_factory=list)
    calculated_completed: bool | None = None
    calculated_due: int | None = None
    deps_clear: bool | None = None


_ENRICHMENT = """
    OPTIONAL MATCH (t)-[:DEPENDS_ON]->(dep:Task)
    WHERE NOT EXISTS { MATCH (t)-[:DEPENDS_ON*2..]->(dep) }
    OPTIONAL MATCH (t)<-[:DEPENDS_ON*]-(downstream:Task)
    WHERE downstream <> t
    OPTIONAL MATCH (t)-[:DEPENDS_ON]->(anyDep:Task)
    WITH t,
         collect(DISTINCT dep.id) AS direct_deps,
         collect(DISTINCT anyDep) AS all_deps,
         [x IN collect(DISTINCT downstream.due) WHERE x IS NOT NULL] +
           (CASE WHEN t.due IS NULL THEN [] ELSE [t.due] END) AS dues
    RETURN t,
           direct_deps,
           t.completed AND (size(all_deps) = 0 OR all(d IN all_deps WHERE d.completed = true))
             AS calculated_completed,
           CASE WHEN size(dues) = 0 THEN NULL
                ELSE reduce(d = head(dues), x IN dues | CASE WHEN x < d THEN x ELSE d END)
           END AS calculated_due,
           size(all_deps) = 0 OR all(d IN all_deps WHERE d.completed = true)
             AS deps_clear
"""


def _node_to_task(node) -> Task:
    """Convert Neo4j node to Task."""
    d = dict(node)
    return Task(
        id=d.get("id", ""),
        text=d.get("text", ""),
        completed=d.get("completed", False),
        inferred=d.get("inferred", False),
        due=d.get("due"),
        created_at=d.get("created_at"),
        updated_at=d.get("updated_at"),
    )


def _record_to_enriched(record, skip_calculated: bool = False) -> EnrichedTask:
    """Convert query record to EnrichedTask."""
    return EnrichedTask(
        task=_node_to_task(record["t"]),
        direct_deps=record.get("direct_deps", []),
        calculated_completed=None if skip_calculated else record.get("calculated_completed"),
        calculated_due=None if skip_calculated else record.get("calculated_due"),
        deps_clear=None if skip_calculated else record.get("deps_clear"),
    )


def _sort_by_updated(records: list) -> list:
    """Sort records by updated_at desc, falling back to created_at."""
    return sorted(
        records,
        key=lambda r: dict(r["t"]).get("updated_at") or dict(r["t"]).get("created_at") or 0,
        reverse=True,
    )


# ============================================================================
# Read operations
# ============================================================================


def has_cycles(tx) -> bool:
    """Check if the graph has any cycles."""
    result = tx.run(
        "MATCH (t:Task) WHERE (t)-[:DEPENDS_ON*1..]->(t) RETURN t.id LIMIT 1"
    )
    return result.single() is not None


def list_tasks(tx) -> tuple[list[EnrichedTask], bool]:
    """List all tasks with computed properties.

    Returns (tasks, has_cycles).
    """
    graph_has_cycles = has_cycles(tx)
    result = tx.run("MATCH (t:Task)" + _ENRICHMENT)
    records = _sort_by_updated(list(result))
    tasks = [_record_to_enriched(r, skip_calculated=graph_has_cycles) for r in records]
    return tasks, graph_has_cycles


# ============================================================================
# Write operations
# ============================================================================


def add_task(
    tx,
    id: str,
    text: str | None = None,
    completed: bool = False,
    inferred: bool = False,
    due: str | None = None,
    depends: list[str] | None = None,
    blocks: list[str] | None = None,
) -> Task:
    """Create a new task."""
    now = int(time.time())
    props = {
        "id": id,
        "completed": completed,
        "inferred": inferred,
        "created_at": now,
        "updated_at": now,
    }
    if text is not None:
        props["text"] = text
    if due is not None:
        props["due"] = parse_due(due)

    tx.run("CREATE (t:Task $props)", props=props)

    for dep_id in (depends or []):
        _create_dependency(tx, id, dep_id)
    for block_id in (blocks or []):
        _create_dependency(tx, block_id, id)

    return Task(**{k: v for k, v in props.items() if k in Task.__dataclass_fields__})


def update_task(
    tx,
    id: str,
    text: str | None = None,
    completed: bool | None = None,
    inferred: bool | None = None,
    due: str | None = None,
) -> bool:
    """Update an existing task. Returns True if found."""
    props = {}
    if text is not None:
        props["text"] = text
    if completed is not None:
        props["completed"] = completed
    if inferred is not None:
        props["inferred"] = inferred
    if due is not None:
        props["due"] = parse_due(due)

    if not props:
        # Check if task exists
        result = tx.run("MATCH (t:Task {id: $id}) RETURN t", id=id)
        return result.single() is not None

    props["updated_at"] = int(time.time())
    result = tx.run(
        "MATCH (t:Task {id: $id}) SET t += $props RETURN t",
        id=id, props=props
    )
    return result.single() is not None


def link_tasks(tx, from_id: str, to_id: str) -> None:
    """Create dependency: from_id depends on to_id."""
    _create_dependency(tx, from_id, to_id)


def unlink_tasks(tx, from_id: str, to_id: str) -> bool:
    """Remove dependency. Returns True if found."""
    result = tx.run(
        "MATCH (a:Task {id: $from_id})-[r:DEPENDS_ON]->(b:Task {id: $to_id}) "
        "DELETE r RETURN count(r) AS n",
        from_id=from_id, to_id=to_id
    )
    return result.single()["n"] > 0


def remove_task(tx, id: str) -> bool:
    """Remove a task. Returns True if found."""
    result = tx.run(
        "MATCH (t:Task {id: $id}) DETACH DELETE t RETURN count(t) AS n",
        id=id
    )
    return result.single()["n"] > 0


def rename_task(tx, old_id: str, new_id: str) -> None:
    """Rename a task. Raises if old not found or new already exists."""
    if old_id == new_id:
        raise ValueError("Old and new IDs are the same")

    # Check new ID doesn't exist
    if tx.run("MATCH (t:Task {id: $id}) RETURN t", id=new_id).single():
        raise ValueError(f"Task '{new_id}' already exists")

    result = tx.run(
        "MATCH (t:Task {id: $old_id}) SET t.id = $new_id, t.updated_at = $now RETURN t",
        old_id=old_id, new_id=new_id, now=int(time.time())
    )
    if not result.single():
        raise ValueError(f"Task '{old_id}' not found")


def _create_dependency(tx, from_id: str, to_id: str) -> None:
    """Create a dependency edge, checking for cycles."""
    if would_create_cycle(tx, from_id, to_id):
        raise ValueError(f"Would create cycle: {from_id} -> {to_id}")
    result = tx.run(
        "MATCH (a:Task {id: $from_id}), (b:Task {id: $to_id}) "
        "MERGE (a)-[:DEPENDS_ON]->(b) RETURN b",
        from_id=from_id, to_id=to_id
    )
    if not result.single():
        raise ValueError(f"Task not found: {from_id} or {to_id}")


# ============================================================================
# Admin operations
# ============================================================================


def init_db(tx) -> None:
    """Initialize database constraints."""
    tx.run(
        "CREATE CONSTRAINT task_id_unique IF NOT EXISTS "
        "FOR (t:Task) REQUIRE t.id IS UNIQUE"
    )


def prime_tokens(tx) -> None:
    """Create and delete a dummy node to register property keys."""
    tx.run(
        "CREATE (t:__InitTokenRegistration:Task {id: '__init__', due: 0, completed: false, inferred: false, created_at: 0, updated_at: 0, text: ''}) "
        "CREATE (t)-[:DEPENDS_ON]->(t) "
        "DETACH DELETE t"
    )
