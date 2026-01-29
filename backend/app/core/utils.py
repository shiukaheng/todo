"""Utility functions."""
from __future__ import annotations

import time

import dateparser
import parsedatetime


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


def parse_due(due_str: str) -> int:
    """Parse a due date string to unix timestamp."""
    parsed = dateparser.parse(due_str, settings={"PREFER_DATES_FROM": "future"})
    if parsed is not None:
        return int(parsed.timestamp())

    cal = parsedatetime.Calendar()
    time_struct, parse_status = cal.parse(due_str)
    if parse_status:
        return int(time.mktime(time_struct))

    raise ValueError(f"Could not parse date: {due_str}")
