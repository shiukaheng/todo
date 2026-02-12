"""Pure functional service layer for node operations - UPDATED FOR BOOLEAN GRAPH."""
from __future__ import annotations

import functools
import logging
import time
import uuid
import warnings
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# Valid node types for whitelist validation
VALID_NODE_TYPES = frozenset(["Task", "And", "Or", "Not", "ExactlyOne"])


@dataclass
class Node:
    """Node data (any type)."""
    id: str
    node_type: str  # "Task", "And", "Or", "Not", "ExactlyOne" - DERIVED from labels
    text: str = ""
    completed: bool | None = None  # Only for Task nodes
    due: int | None = None
    created_at: int | None = None
    updated_at: int | None = None


@dataclass
class EnrichedNode:
    """Node with calculated properties."""
    node: Node
    calculated_value: bool | None = None  # Renamed from calculated_completed
    calculated_due: int | None = None
    deps_clear: bool | None = None
    is_actionable: bool | None = None


@dataclass
class Dependency:
    """Dependency relationship."""
    id: str
    from_id: str
    to_id: str


@dataclass
class Plan:
    """Plan data (organizational layer, not part of Node graph)."""
    id: str
    text: str | None = None
    created_at: int | None = None
    updated_at: int | None = None


@dataclass
class Step:
    """Step in a plan (STEP relationship)."""
    id: str
    order: float
    node_id: str


# ============================================================================
# Helper functions
# ============================================================================


def _extract_node_type(labels: list[str]) -> str:
    """Extract node type from labels list."""
    for label in labels:
        if label in VALID_NODE_TYPES:
            return label
    return "Task"  # Default fallback


def _record_to_node(record) -> Node:
    """Convert Neo4j record to Node."""
    node_data = dict(record["n"])
    labels = record["labels"]

    return Node(
        id=node_data.get("id", ""),
        node_type=_extract_node_type(labels),
        text=node_data.get("text", ""),
        completed=node_data.get("completed"),  # None for gates
        due=node_data.get("due"),
        created_at=node_data.get("created_at"),
        updated_at=node_data.get("updated_at"),
    )


def _record_to_enriched(record) -> EnrichedNode:
    """Convert query record to EnrichedNode (values calculated separately in Python)."""
    return EnrichedNode(
        node=_record_to_node(record),
        calculated_value=None,  # Calculated in Python later
        calculated_due=None,     # Calculated in Python later
        deps_clear=None,         # Calculated in Python later
    )


def _sort_by_updated(records: list) -> list:
    """Sort records by updated_at desc, falling back to created_at."""
    return sorted(
        records,
        key=lambda r: dict(r["n"]).get("updated_at") or dict(r["n"]).get("created_at") or 0,
        reverse=True,
    )


# ============================================================================
# Pure calculation utilities (stateless, compositional)
# ============================================================================

def _calculate_gate_logic(node_type: str, dep_values: list[bool]) -> bool:
    """Calculate gate-specific logic on dependencies (used for both calculated_value and deps_clear).

    For Task and And: AND logic (all deps must be true)
    For Or: OR logic (any dep must be true)
    For Not: NOR logic (no deps must be true)
    For ExactlyOne: XOR logic (exactly one dep must be true)
    """
    match node_type:
        case "Task" | "And": return not dep_values or all(dep_values)
        case "Or": return bool(dep_values) and any(dep_values)
        case "Not": return not any(dep_values)
        case "ExactlyOne": return sum(dep_values) == 1
        case _: return True


def _build_value_calculator(nodes: dict[str, Node], deps: dict[str, list[str]]):
    """Build a memoized value calculator closure.

    calculated_value = own_value AND deps_clear
    - Task: own_value = completed, deps_clear = all(deps.calculated_value)
    - Gates: own_value = true (identity), deps_clear = gate_logic(deps.calculated_value)
    """
    @functools.lru_cache(maxsize=1024)
    def calculate(node_id: str) -> bool:
        node = nodes[node_id]
        dep_values = [calculate(dep_id) for dep_id in deps.get(node_id, [])]

        # deps_clear is gate-specific evaluation of dependencies
        deps_clear = _calculate_gate_logic(node.node_type, dep_values)

        if node.node_type == "Task":
            # Task: calculated_value = completed AND deps_clear
            return (node.completed if node.completed is not None else False) and deps_clear
        else:
            # Gates: calculated_value = deps_clear (no own value)
            return deps_clear
    return calculate


def _build_due_calculator(nodes: dict[str, Node], downstream: dict[str, list[str]]):
    """Build a memoized due date calculator closure."""
    @functools.lru_cache(maxsize=1024)
    def calculate(node_id: str) -> int | None:
        dues = [nodes[node_id].due] if nodes[node_id].due else []
        dues.extend(filter(None, [calculate(d) for d in downstream.get(node_id, [])]))
        return min(dues) if dues else None
    return calculate


def _build_graph_indexes(nodes: list[Node], deps: list[Dependency]):
    """Build lookup indexes from raw data."""
    nodes_by_id = {n.id: n for n in nodes}

    deps_fwd = {}  # from_id -> [to_id, ...]
    deps_rev = {}  # to_id -> [from_id, ...]
    for d in deps:
        deps_fwd.setdefault(d.from_id, []).append(d.to_id)
        deps_rev.setdefault(d.to_id, []).append(d.from_id)

    return nodes_by_id, deps_fwd, deps_rev


# Simplified Cypher query - just fetch data
_ENRICHMENT = """ RETURN n, labels(n) AS labels """


# ============================================================================
# Read operations
# ============================================================================


def has_cycles(tx) -> bool:
    """Check if the graph has any cycles."""
    result = tx.run(
        "MATCH (n:Node) WHERE (n)-[:DEPENDS_ON*1..]->(n) RETURN n.id LIMIT 1"
    )
    return result.single() is not None


def list_dependencies(tx) -> list[Dependency]:
    """List all dependencies."""
    result = tx.run(
        "MATCH (a:Node)-[r:DEPENDS_ON]->(b:Node) "
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


def get_node(tx, id: str) -> EnrichedNode | None:
    """Get a single node with computed properties."""
    record = tx.run("MATCH (n:Node {id: $id})" + _ENRICHMENT, id=id).single()
    if not record:
        return None

    enriched = _record_to_enriched(record)

    if not has_cycles(tx):
        # Fetch only nodes in transitive closure (dependencies of this node)
        closure_records = tx.run(
            "MATCH (start:Node {id: $id}) "
            "OPTIONAL MATCH path = (start)-[:DEPENDS_ON*]->(dep) "
            "WITH start, collect(DISTINCT dep) AS deps "
            "UNWIND [start] + deps AS node "
            "RETURN node AS n, labels(node) AS labels",
            id=id
        )
        closure_nodes = [_record_to_node(r) for r in closure_records]

        # Fetch dependencies only within closure
        closure_ids = {n.id for n in closure_nodes}
        all_deps = list_dependencies(tx)
        relevant_deps = [d for d in all_deps if d.from_id in closure_ids and d.to_id in closure_ids]

        nodes_map, deps_fwd, deps_rev = _build_graph_indexes(closure_nodes, relevant_deps)
        calc_value = _build_value_calculator(nodes_map, deps_fwd)
        calc_due = _build_due_calculator(nodes_map, deps_rev)

        enriched.calculated_value = calc_value(id)
        enriched.calculated_due = calc_due(id)
        dep_values = [calc_value(d) for d in deps_fwd.get(id, [])]
        enriched.deps_clear = _calculate_gate_logic(enriched.node.node_type, dep_values)
        enriched.is_actionable = enriched.node.node_type == "Task" and not (enriched.node.completed if enriched.node.completed is not None else False) and enriched.deps_clear

    return enriched


def list_nodes(tx) -> tuple[list[EnrichedNode], list[Dependency], bool]:
    """List all nodes with computed properties."""
    # Fetch data
    records = _sort_by_updated(list(tx.run("MATCH (n:Node)" + _ENRICHMENT)))
    enriched = [_record_to_enriched(r) for r in records]
    dependencies = list_dependencies(tx)
    graph_has_cycles = has_cycles(tx)

    if not graph_has_cycles:
        # Build indexes and calculators
        nodes_map, deps_fwd, deps_rev = _build_graph_indexes([e.node for e in enriched], dependencies)
        calc_value = _build_value_calculator(nodes_map, deps_fwd)
        calc_due = _build_due_calculator(nodes_map, deps_rev)

        # Calculate properties
        for e in enriched:
            e.calculated_value = calc_value(e.node.id)
            e.calculated_due = calc_due(e.node.id)
            # deps_clear = gate-specific evaluation of dependencies
            dep_values = [calc_value(d) for d in deps_fwd.get(e.node.id, [])]
            e.deps_clear = _calculate_gate_logic(e.node.node_type, dep_values)
            e.is_actionable = e.node.node_type == "Task" and not (e.node.completed if e.node.completed is not None else False) and e.deps_clear

    return enriched, dependencies, graph_has_cycles


# ============================================================================
# Write operations
# ============================================================================


def add_node(
    tx,
    id: str,
    node_type: str = "Task",
    text: str | None = None,
    completed: bool = False,
    due: int | None = None,
    depends: list[str] | None = None,
    blocks: list[str] | None = None,
) -> Node:
    """Create a new node of any type."""
    if node_type not in VALID_NODE_TYPES:
        raise ValueError(f"Invalid node type: {node_type}")

    now = int(time.time())
    props = {
        "id": id,
        "created_at": now,
        "updated_at": now,
    }
    if text is not None:
        props["text"] = text
    if due is not None:
        props["due"] = due

    # Only add completed for Task nodes
    if node_type == "Task":
        props["completed"] = completed

    # Create with appropriate labels
    labels = f":Node:{node_type}"
    tx.run(f"CREATE (n{labels} $props)", props=props)

    # Create DEPENDS_ON relationships
    for dep_id in (depends or []):
        _create_dependency(tx, id, dep_id)
    for block_id in (blocks or []):
        _create_dependency(tx, block_id, id)

    return Node(
        id=id,
        node_type=node_type,
        text=props.get("text", ""),
        completed=props.get("completed"),
        due=props.get("due"),
        created_at=now,
        updated_at=now,
    )


_UNSET = object()  # Sentinel value to distinguish "not provided" from "None"


def _propagate_uncompletion(tx, task_id: str, now: int) -> list[str]:
    """
    Recursively uncomplete all dependent tasks (parents) that are currently marked as complete.

    When a task is marked incomplete, any task that depends on it should also be marked
    incomplete to maintain consistency between calculated_value and the completed flag.

    Returns list of task IDs that were updated.
    """
    updated_ids = []

    # Find all tasks that directly depend on this task (parents in dependency tree)
    result = tx.run(
        """
        MATCH (target:Node {id: $task_id})<-[:DEPENDS_ON]-(parent:Task)
        WHERE parent.completed = true
        RETURN parent.id AS parent_id
        """,
        task_id=task_id
    )

    dependent_ids = [record["parent_id"] for record in result]

    # Recursively uncomplete each dependent task
    for dep_id in dependent_ids:
        # Mark this dependent as incomplete
        tx.run(
            "MATCH (n:Task {id: $id}) SET n.completed = false, n.updated_at = $now",
            id=dep_id,
            now=now
        )
        updated_ids.append(dep_id)

        # Recursively propagate to its dependents
        child_updates = _propagate_uncompletion(tx, dep_id, now)
        updated_ids.extend(child_updates)

    return updated_ids


def update_node(
    tx,
    id: str,
    node_type: str | None = None,
    text: str | None = None,
    completed: bool | None = None,
    due: int | None | object = _UNSET,
) -> bool:
    """Update an existing node. Returns True if found."""
    now = int(time.time())

    # If changing type, handle label changes
    if node_type is not None:
        # Get current labels
        result = tx.run(
            "MATCH (n:Node {id: $id}) RETURN labels(n) AS labels",
            id=id
        )
        record = result.single()
        if not record:
            return False

        current_labels = record["labels"]
        current_type = _extract_node_type(current_labels)

        if current_type != node_type:
            # Validate node types against whitelist
            if current_type not in VALID_NODE_TYPES:
                raise ValueError(f"Invalid current node type: {current_type}")
            if node_type not in VALID_NODE_TYPES:
                raise ValueError(f"Invalid target node type: {node_type}")

            # Change node type
            logger.debug(f"Changing node type: {current_type} -> {node_type}")

            # Handle completed property based on type transition
            # Use WHERE clause to ensure atomicity - fails if type changed between read and write
            if node_type == "Task" and current_type != "Task":
                # Converting TO Task - add completed property
                completed_value = completed if completed is not None else False
                query = (
                    f"MATCH (n:{current_type} {{id: $id}}) "
                    f"WHERE $current_type IN labels(n) "  # Atomic check
                    f"REMOVE n:{current_type} "
                    f"SET n:{node_type}, n.updated_at = $now, n.completed = $completed "
                    "RETURN n"
                )
                result = tx.run(query, id=id, now=now, completed=completed_value, current_type=current_type)
            elif current_type == "Task" and node_type != "Task":
                # Converting FROM Task - remove completed property
                query = (
                    f"MATCH (n:{current_type} {{id: $id}}) "
                    f"WHERE $current_type IN labels(n) "  # Atomic check
                    f"REMOVE n:{current_type}, n.completed "
                    f"SET n:{node_type}, n.updated_at = $now "
                    "RETURN n"
                )
                result = tx.run(query, id=id, now=now, current_type=current_type)
            else:
                # Simple type change without completed handling
                query = (
                    f"MATCH (n:{current_type} {{id: $id}}) "
                    f"WHERE $current_type IN labels(n) "  # Atomic check
                    f"REMOVE n:{current_type} "
                    f"SET n:{node_type}, n.updated_at = $now "
                    "RETURN n"
                )
                result = tx.run(query, id=id, now=now, current_type=current_type)

            # Check if update succeeded
            updated_record = result.single()
            if not updated_record:
                # Type changed between our read and write, or node disappeared
                raise ValueError(
                    f"Failed to change node type from {current_type} to {node_type}. "
                    f"Node may have been modified concurrently."
                )

            logger.debug(f"Node type changed successfully: {current_type} -> {node_type}")

    # Check if we're marking a task as incomplete (for propagation)
    propagate_uncompletion = False
    if completed is not None and not completed:
        # Query current state to see if we're transitioning from complete to incomplete
        # Only Task nodes have completed property, so check node type
        result = tx.run(
            "MATCH (n:Node {id: $id}) "
            "WHERE 'Task' IN labels(n) AND n.completed = true "
            "RETURN n.completed AS current_completed",
            id=id
        )
        record = result.single()
        if record:
            # We're transitioning from complete to incomplete - need to propagate
            propagate_uncompletion = True

    # Update other properties
    props = {}
    if text is not None:
        props["text"] = text
    if completed is not None:
        props["completed"] = completed
    # Handle due: distinguish between not provided (_UNSET), explicitly None (clear), or a value
    if due is not _UNSET:
        if due is None:
            # Explicitly clearing due - we'll need to remove it separately
            # For now, set to null in Neo4j (which removes the property)
            props["due"] = None
        else:
            props["due"] = due

    if props:
        props["updated_at"] = now
        result = tx.run(
            "MATCH (n:Node {id: $id}) SET n += $props RETURN n",
            id=id, props=props
        )
        if result.single() is None:
            return False

    # Propagate uncompletion to dependent tasks if needed
    if propagate_uncompletion:
        updated_ids = _propagate_uncompletion(tx, id, now)
        if updated_ids:
            logger.debug(f"Propagated uncompletion from {id} to {len(updated_ids)} dependent task(s): {updated_ids}")

    return True


def link_nodes(tx, from_id: str, to_id: str) -> str:
    """Create dependency: from_id depends on to_id. Returns the dependency ID."""
    return _create_dependency(tx, from_id, to_id)


def unlink_nodes(tx, from_id: str, to_id: str) -> bool:
    """Remove dependency. Returns True if found."""
    result = tx.run(
        "MATCH (a:Node {id: $from_id})-[r:DEPENDS_ON]->(b:Node {id: $to_id}) "
        "DELETE r RETURN count(r) AS n",
        from_id=from_id, to_id=to_id
    )
    return result.single()["n"] > 0


def remove_node(tx, id: str) -> bool:
    """Remove a node. Returns True if found."""
    result = tx.run(
        "MATCH (n:Node {id: $id}) DETACH DELETE n RETURN count(n) AS n",
        id=id
    )
    return result.single()["n"] > 0


def rename_node(tx, old_id: str, new_id: str) -> None:
    """Rename a node. Raises if old not found or new already exists."""
    if old_id == new_id:
        raise ValueError("Old and new IDs are the same")

    # Check new ID doesn't exist
    if tx.run("MATCH (n:Node {id: $id}) RETURN n", id=new_id).single():
        raise ValueError(f"Node '{new_id}' already exists")

    result = tx.run(
        "MATCH (n:Node {id: $old_id}) SET n.id = $new_id, n.updated_at = $now RETURN n",
        old_id=old_id, new_id=new_id, now=int(time.time())
    )
    if not result.single():
        raise ValueError(f"Node '{old_id}' not found")


_CREATE_DEPENDENCY_QUERY = (
    "MATCH (a:Node {id: $from_id}), (b:Node {id: $to_id}) "
    "MERGE (a)-[r:DEPENDS_ON]->(b) "
    "ON CREATE SET r.id = $dep_id "
    "WITH {dep_id: r.id, found: true} AS _passthrough "
    # Transitive reduction: remove edges implied by longer paths
    "CALL { "
    "  MATCH (x:Node)-[direct:DEPENDS_ON]->(y:Node) "
    "  WHERE EXISTS { MATCH (x)-[:DEPENDS_ON*2..]->(y) } "
    "  DELETE direct "
    "  RETURN count(direct) AS cnt "
    "} "
    "RETURN _passthrough.dep_id AS dep_id, _passthrough.found AS found, cnt AS reduced"
)


def _create_dependency(tx, from_id: str, to_id: str) -> str:
    """Create a dependency edge. Returns the dependency ID.

    Validates:
    - Both nodes exist
    - No self-loops
    - No cycles would be created
    """
    if from_id == to_id:
        raise ValueError(f"Self-loop not allowed: {from_id}")

    # Check both nodes exist separately for better error messages
    from_exists = tx.run(
        "MATCH (n:Node {id: $id}) RETURN n.id AS id",
        id=from_id
    ).single()
    if not from_exists:
        raise ValueError(f"Source node not found: {from_id}")

    to_exists = tx.run(
        "MATCH (n:Node {id: $id}) RETURN n.id AS id",
        id=to_id
    ).single()
    if not to_exists:
        raise ValueError(f"Target node not found: {to_id}")

    # Check if this edge would create a cycle
    # A cycle would exist if there's already a path from to_id to from_id
    would_cycle = tx.run(
        "MATCH (a:Node {id: $to_id}), (b:Node {id: $from_id}) "
        "WHERE (a)-[:DEPENDS_ON*]->(b) "
        "RETURN true AS cycle",
        from_id=from_id, to_id=to_id
    ).single()

    if would_cycle:
        raise ValueError(
            f"Creating edge {from_id} -> {to_id} would create a cycle. "
            f"A path already exists from {to_id} to {from_id}"
        )

    # Create the dependency edge (MERGE handles duplicates)
    dep_id = str(uuid.uuid4())
    result = tx.run(
        _CREATE_DEPENDENCY_QUERY,
        from_id=from_id, to_id=to_id, dep_id=dep_id
    )
    record = result.single()
    if not record or not record["found"]:
        # This shouldn't happen since we checked above, but keep as safety
        raise ValueError(f"Failed to create dependency")

    reduced_count = record.get("reduced", 0)
    if reduced_count > 0:
        logger.debug(f"Transitive reduction: removed {reduced_count} redundant edge(s)")

    logger.debug(f"Created dependency: {from_id} -> {to_id} (id: {dep_id})")
    return record["dep_id"]


# ============================================================================
# Admin operations
# ============================================================================


def init_db(tx) -> None:
    """Initialize database constraints."""
    # Drop old constraint
    tx.run("DROP CONSTRAINT task_id_unique IF EXISTS")

    # Create node constraints
    tx.run(
        "CREATE CONSTRAINT node_id_unique IF NOT EXISTS "
        "FOR (n:Node) REQUIRE n.id IS UNIQUE"
    )

    # Create plan constraints
    tx.run(
        "CREATE CONSTRAINT plan_id_unique IF NOT EXISTS "
        "FOR (p:Plan) REQUIRE p.id IS UNIQUE"
    )

    # Create relationship constraints
    tx.run(
        "CREATE CONSTRAINT step_id_unique IF NOT EXISTS "
        "FOR ()-[r:STEP]->() REQUIRE r.id IS UNIQUE"
    )

    # Note: In Neo4j Enterprise, we could add a constraint to prevent
    # duplicate STEP relationships from a Plan to the same Node:
    # CREATE CONSTRAINT plan_unique_steps IF NOT EXISTS
    # FOR (p:Plan)-[s:STEP]->(n:Node) REQUIRE (p, n) IS UNIQUE
    # For Community Edition, this is enforced in Python code instead.


def migrate_to_boolean_graph(tx) -> None:
    """Migrate existing Task nodes to boolean graph schema."""
    # 1. Add :Node label to all tasks
    tx.run("MATCH (t:Task) SET t:Node")

    # 2. Convert inferred tasks to And gates
    tx.run(
        "MATCH (t:Task {inferred: true}) "
        "SET t:And "
        "REMOVE t:Task, t.completed, t.inferred"
    )

    # 3. Remove inferred from regular tasks
    tx.run(
        "MATCH (t:Task {inferred: false}) "
        "REMOVE t.inferred"
    )


def migrate_dependency_ids(tx) -> None:
    """Assign UUIDs to any relationships missing an ID."""
    tx.run(
        "MATCH (a:Node)-[r:DEPENDS_ON]->(b:Node) "
        "WHERE r.id IS NULL "
        "SET r.id = randomUUID()"
    )


def prime_tokens(tx) -> None:
    """Create and delete a dummy node to register property keys."""
    tx.run(
        "CREATE (n:__InitTokenRegistration:Node:Task "
        "{id: '__init__', due: 0, completed: false, created_at: 0, updated_at: 0, text: ''}) "
        "CREATE (n)-[:DEPENDS_ON {id: '__init__'}]->(n) "
        "DETACH DELETE n"
    )


# Backward compatibility aliases
Task = Node
EnrichedTask = EnrichedNode


def add_task(*args, **kwargs):
    """Deprecated: use add_node instead."""
    warnings.warn(
        "add_task is deprecated, use add_node instead",
        DeprecationWarning,
        stacklevel=2
    )
    return add_node(*args, **kwargs)


def update_task(*args, **kwargs):
    """Deprecated: use update_node instead."""
    warnings.warn(
        "update_task is deprecated, use update_node instead",
        DeprecationWarning,
        stacklevel=2
    )
    return update_node(*args, **kwargs)


def get_task(*args, **kwargs):
    """Deprecated: use get_node instead."""
    warnings.warn(
        "get_task is deprecated, use get_node instead",
        DeprecationWarning,
        stacklevel=2
    )
    return get_node(*args, **kwargs)


def list_tasks(*args, **kwargs):
    """Deprecated: use list_nodes instead."""
    warnings.warn(
        "list_tasks is deprecated, use list_nodes instead",
        DeprecationWarning,
        stacklevel=2
    )
    return list_nodes(*args, **kwargs)


def rename_task(*args, **kwargs):
    """Deprecated: use rename_node instead."""
    warnings.warn(
        "rename_task is deprecated, use rename_node instead",
        DeprecationWarning,
        stacklevel=2
    )
    return rename_node(*args, **kwargs)


def remove_task(*args, **kwargs):
    """Deprecated: use remove_node instead."""
    warnings.warn(
        "remove_task is deprecated, use remove_node instead",
        DeprecationWarning,
        stacklevel=2
    )
    return remove_node(*args, **kwargs)


def link_tasks(*args, **kwargs):
    """Deprecated: use link_nodes instead."""
    warnings.warn(
        "link_tasks is deprecated, use link_nodes instead",
        DeprecationWarning,
        stacklevel=2
    )
    return link_nodes(*args, **kwargs)


def unlink_tasks(*args, **kwargs):
    """Deprecated: use unlink_nodes instead."""
    warnings.warn(
        "unlink_tasks is deprecated, use unlink_nodes instead",
        DeprecationWarning,
        stacklevel=2
    )
    return unlink_nodes(*args, **kwargs)


# ============================================================================
# Plan operations (separate from Node graph)
# ============================================================================


def _get_plan_steps(tx, plan_id: str) -> list[Step]:
    """Get all steps for a plan, ordered by order field."""
    result = tx.run(
        "MATCH (p:Plan {id: $plan_id})-[s:STEP]->(n:Node) "
        "RETURN s.id AS id, s.order AS order, n.id AS node_id "
        "ORDER BY s.order ASC",
        plan_id=plan_id
    )
    return [
        Step(
            id=record["id"],
            order=record["order"],
            node_id=record["node_id"]
        )
        for record in result
    ]


def _set_plan_steps(tx, plan_id: str, steps: list[tuple[str, float]]) -> None:
    """Replace all steps for a plan. steps = [(node_id, order), ...]"""
    # Check for duplicate node_ids
    node_ids = [node_id for node_id, _ in steps]
    if len(node_ids) != len(set(node_ids)):
        # Find the duplicate(s)
        seen = set()
        duplicates = []
        for node_id in node_ids:
            if node_id in seen:
                duplicates.append(node_id)
            seen.add(node_id)
        raise ValueError(f"Duplicate node(s) in plan: {', '.join(set(duplicates))}")

    # Delete existing steps
    tx.run(
        "MATCH (p:Plan {id: $plan_id})-[s:STEP]->() DELETE s",
        plan_id=plan_id
    )

    # Create new steps
    for node_id, order in steps:
        # Verify node exists
        node_exists = tx.run(
            "MATCH (n:Node {id: $node_id}) RETURN n.id AS id",
            node_id=node_id
        ).single()
        if not node_exists:
            raise ValueError(f"Node not found: {node_id}")

        # Create step
        step_id = str(uuid.uuid4())
        tx.run(
            "MATCH (p:Plan {id: $plan_id}), (n:Node {id: $node_id}) "
            "CREATE (p)-[:STEP {id: $step_id, order: $order}]->(n)",
            plan_id=plan_id,
            node_id=node_id,
            step_id=step_id,
            order=order
        )


def list_plans(tx) -> list[Plan]:
    """List all plans with their steps."""
    result = tx.run(
        "MATCH (p:Plan) "
        "RETURN p.id AS id, p.text AS text, p.created_at AS created_at, p.updated_at AS updated_at "
        "ORDER BY p.updated_at DESC"
    )

    plans = []
    for record in result:
        plan = Plan(
            id=record["id"],
            text=record["text"],
            created_at=record["created_at"],
            updated_at=record["updated_at"]
        )
        plans.append(plan)

    return plans


def get_plan(tx, plan_id: str) -> Plan | None:
    """Get a single plan."""
    result = tx.run(
        "MATCH (p:Plan {id: $id}) "
        "RETURN p.id AS id, p.text AS text, p.created_at AS created_at, p.updated_at AS updated_at",
        id=plan_id
    )
    record = result.single()
    if not record:
        return None

    return Plan(
        id=record["id"],
        text=record["text"],
        created_at=record["created_at"],
        updated_at=record["updated_at"]
    )


def create_plan(
    tx,
    id: str,
    text: str | None = None,
    steps: list[tuple[str, float]] | None = None
) -> Plan:
    """Create a new plan. Returns the created plan."""
    now = int(time.time())

    # Check if plan already exists
    existing = tx.run("MATCH (p:Plan {id: $id}) RETURN p", id=id).single()
    if existing:
        raise ValueError(f"Plan '{id}' already exists")

    # Create plan
    props = {
        "id": id,
        "created_at": now,
        "updated_at": now,
    }
    if text is not None:
        props["text"] = text

    tx.run("CREATE (p:Plan $props)", props=props)

    # Add steps if provided
    if steps:
        _set_plan_steps(tx, id, steps)

    return Plan(
        id=id,
        text=text,
        created_at=now,
        updated_at=now
    )


def update_plan(
    tx,
    id: str,
    text: str | None = None,
    steps: list[tuple[str, float]] | None = None
) -> bool:
    """Update a plan. Returns True if found, False otherwise."""
    now = int(time.time())

    # Check if plan exists
    result = tx.run("MATCH (p:Plan {id: $id}) RETURN p", id=id)
    if not result.single():
        return False

    # Update text if provided
    if text is not None:
        tx.run(
            "MATCH (p:Plan {id: $id}) SET p.text = $text, p.updated_at = $now",
            id=id,
            text=text,
            now=now
        )

    # Update steps if provided
    if steps is not None:
        _set_plan_steps(tx, id, steps)
        # Update timestamp
        tx.run(
            "MATCH (p:Plan {id: $id}) SET p.updated_at = $now",
            id=id,
            now=now
        )

    return True


def delete_plan(tx, id: str) -> bool:
    """Delete a plan (steps are deleted via cascade, nodes are NOT deleted). Returns True if found."""
    result = tx.run(
        "MATCH (p:Plan {id: $id}) DETACH DELETE p RETURN count(p) AS n",
        id=id
    )
    return result.single()["n"] > 0
