"""Pure functional service layer for task operations."""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field




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
    """Task with calculated properties."""
    task: Task
    calculated_completed: bool | None = None
    calculated_due: int | None = None
    deps_clear: bool | None = None


@dataclass
class Dependency:
    """Dependency relationship."""
    id: str
    from_id: str
    to_id: str


_ENRICHMENT = """
    OPTIONAL MATCH (t)-[:DEPENDS_ON]->(anyDep:Task)
    OPTIONAL MATCH (t)<-[:DEPENDS_ON*]-(downstream:Task)
    WHERE downstream <> t
    WITH t,
         collect(DISTINCT anyDep) AS all_deps,
         [x IN collect(DISTINCT downstream.due) WHERE x IS NOT NULL] +
           (CASE WHEN t.due IS NULL THEN [] ELSE [t.due] END) AS dues
    RETURN t,
           (t.inferred OR t.completed) AND (size(all_deps) = 0 OR all(d IN all_deps WHERE d.completed = true))
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


# Reusable finalization suffix. Expects `_passthrough` variable to exist.
# Returns: _passthrough (preserved), _reduced (count), _errors (list)
_FINALIZE_SUFFIX = """
// Transitive reduction: remove edges implied by longer paths
CALL {
    MATCH (a:Task)-[direct:DEPENDS_ON]->(c:Task)
    WHERE EXISTS { MATCH (a)-[:DEPENDS_ON*2..]->(c) }
    DELETE direct
    RETURN count(direct) AS cnt
}
WITH _passthrough, cnt AS _reduced

// Collect validation errors
CALL {
    OPTIONAL MATCH (t:Task) WHERE (t)-[:DEPENDS_ON*1..]->(t)
    WITH t LIMIT 1
    RETURN CASE WHEN t IS NOT NULL THEN 'Cycle involving: ' + t.id ELSE NULL END AS err
    UNION ALL
    OPTIONAL MATCH (t:Task)-[:DEPENDS_ON]->(t)
    WITH t LIMIT 1
    RETURN CASE WHEN t IS NOT NULL THEN 'Self-loop: ' + t.id ELSE NULL END AS err
    UNION ALL
    OPTIONAL MATCH (a:Task)-[r:DEPENDS_ON]->(b:Task)
    WITH a.id AS from_id, b.id AS to_id, count(r) AS cnt
    WHERE cnt > 1
    WITH from_id, to_id, cnt LIMIT 1
    RETURN CASE WHEN cnt > 1 THEN 'Duplicate edges: ' + from_id + ' -> ' + to_id ELSE NULL END AS err
    UNION ALL
    OPTIONAL MATCH (a:Task)-[r:DEPENDS_ON]->(b:Task)
    WHERE r.id IS NULL
    WITH a, b LIMIT 1
    RETURN CASE WHEN a IS NOT NULL THEN 'Missing ID: ' + a.id + ' -> ' + b.id ELSE NULL END AS err
}
WITH _passthrough, _reduced, collect(err) AS _errs
WITH _passthrough, _reduced, [e IN _errs WHERE e IS NOT NULL] AS _errors
"""


def _check_finalize_errors(record) -> None:
    """Check finalize result for errors and raise if any."""
    errors = record["_errors"]
    if errors:
        raise ValueError("; ".join(errors))


def list_dependencies(tx) -> list[Dependency]:
    """List all dependencies."""
    result = tx.run(
        "MATCH (a:Task)-[r:DEPENDS_ON]->(b:Task) "
        "RETURN r.id AS id, a.id AS from_id, b.id AS to_id"
    )
    return [
        Dependency(
            id=record["id"] or "unknown",
            from_id=record["from_id"],
            to_id=record["to_id"],
        )
        for record in result
    ]


def get_task(tx, id: str) -> EnrichedTask | None:
    """Get a single task with computed properties."""
    result = tx.run(
        "MATCH (t:Task {id: $id})" + _ENRICHMENT,
        id=id
    )
    record = result.single()
    if not record:
        return None
    return _record_to_enriched(record)


def list_tasks(tx) -> tuple[list[EnrichedTask], list[Dependency], bool]:
    """List all tasks with computed properties.

    Returns (tasks, dependencies, has_cycles).
    """
    graph_has_cycles = has_cycles(tx)
    result = tx.run("MATCH (t:Task)" + _ENRICHMENT)
    records = _sort_by_updated(list(result))
    tasks = [_record_to_enriched(r, skip_calculated=graph_has_cycles) for r in records]
    dependencies = list_dependencies(tx)
    return tasks, dependencies, graph_has_cycles


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
        props["due"] = due

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
        props["due"] = due

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


def link_tasks(tx, from_id: str, to_id: str) -> str:
    """Create dependency: from_id depends on to_id. Returns the dependency ID."""
    return _create_dependency(tx, from_id, to_id)


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


_CREATE_DEPENDENCY_QUERY = (
    "MATCH (a:Task {id: $from_id}), (b:Task {id: $to_id}) "
    "MERGE (a)-[r:DEPENDS_ON]->(b) "
    "ON CREATE SET r.id = $dep_id "
    "WITH {dep_id: r.id, found: true} AS _passthrough "
    + _FINALIZE_SUFFIX +
    "RETURN _passthrough.dep_id AS dep_id, _passthrough.found AS found, _reduced, _errors"
)


def _create_dependency(tx, from_id: str, to_id: str) -> str:
    """Create a dependency edge with finalization. Returns the dependency ID."""
    if from_id == to_id:
        raise ValueError(f"Self-loop not allowed: {from_id}")

    dep_id = str(uuid.uuid4())
    result = tx.run(
        _CREATE_DEPENDENCY_QUERY,
        from_id=from_id, to_id=to_id, dep_id=dep_id
    )
    record = result.single()
    if not record or not record["found"]:
        raise ValueError(f"Task not found: {from_id} or {to_id}")
    _check_finalize_errors(record)
    return record["dep_id"]


# ============================================================================
# Admin operations
# ============================================================================


def init_db(tx) -> None:
    """Initialize database constraints."""
    tx.run(
        "CREATE CONSTRAINT task_id_unique IF NOT EXISTS "
        "FOR (t:Task) REQUIRE t.id IS UNIQUE"
    )


def migrate_dependency_ids(tx) -> None:
    """Assign UUIDs to any relationships missing an ID."""
    tx.run(
        "MATCH (a:Task)-[r:DEPENDS_ON]->(b:Task) "
        "WHERE r.id IS NULL "
        "SET r.id = randomUUID()"
    )


def prime_tokens(tx) -> None:
    """Create and delete a dummy node to register property keys."""
    tx.run(
        "CREATE (t:__InitTokenRegistration:Task {id: '__init__', due: 0, completed: false, inferred: false, created_at: 0, updated_at: 0, text: ''}) "
        "CREATE (t)-[:DEPENDS_ON {id: '__init__'}]->(t) "
        "DETACH DELETE t"
    )
