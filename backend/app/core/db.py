"""Neo4j driver management."""
from __future__ import annotations

import os
from contextlib import contextmanager

from dotenv import load_dotenv
from neo4j import GraphDatabase, Driver

load_dotenv()

_driver: Driver | None = None


def get_driver() -> Driver:
    """Get or create a Neo4j driver instance."""
    global _driver
    if _driver is None:
        url = os.environ.get("NEO4J_URL", "bolt://localhost:7687")
        user = os.environ.get("NEO4J_USER", "neo4j")
        password = os.environ.get("NEO4J_PASSWORD", "")
        _driver = GraphDatabase.driver(url, auth=(user, password))
    return _driver


def close_driver() -> None:
    """Close the driver connection."""
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None


@contextmanager
def get_session():
    """Get a Neo4j session."""
    driver = get_driver()
    session = driver.session()
    try:
        yield session
    finally:
        session.close()
