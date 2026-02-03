"""Utility functions."""
from __future__ import annotations


def would_create_cycle(tx, from_id: str, to_id: str) -> bool:
    """Check if adding edge from_id -> to_id would create a cycle."""
    if from_id == to_id:
        return True

    result = tx.run(
        "MATCH (a:Task {id: $from_id}), (b:Task {id: $to_id}) "
        "RETURN EXISTS { MATCH (b)-[:DEPENDS_ON*]->(a) } AS would_cycle",
        from_id=from_id,
        to_id=to_id,
    )
    record = result.single()
    return record["would_cycle"] if record else False
