"""Testcontainer fixtures with dynamic port allocation."""

import os
from collections.abc import Generator
from contextlib import contextmanager
from dataclasses import dataclass

from testcontainers.core.container import DockerContainer
from testcontainers.core.wait_strategies import LogMessageWaitStrategy
from testcontainers.postgres import PostgresContainer


@dataclass(frozen=True)
class Container:
    """Connection info for a running testcontainer.

    Attributes:
        host: Container host (always localhost)
        port: Dynamic mapped port
        url: Pre-built connection URL
    """

    host: str
    port: int
    url: str


@contextmanager
def _start_container(
    image: str,
    port: int,
    *,
    env: dict[str, str] | None = None,
    wait_for_log: str | None = None,
) -> Generator[Container]:
    """Start a generic Docker container with dynamic port. Internal building block.

    Args:
        image: Docker image
        port: Internal container port to expose
        env: Environment variables
        wait_for_log: Log message indicating readiness

    Yields:
        Container with http:// URL and dynamic port
    """
    c = DockerContainer(image).with_exposed_ports(port)
    if env:
        for k, v in env.items():
            c = c.with_env(k, v)
    if wait_for_log:
        c = c.waiting_for(LogMessageWaitStrategy(wait_for_log))

    with c:
        mapped = int(c.get_exposed_port(port))
        yield Container(
            host="localhost",
            port=mapped,
            url=f"http://localhost:{mapped}",
        )


@contextmanager
def start_postgres(
    image: str = "postgres:15",
    password: str | None = None,
    username: str = "postgres",
    dbname: str = "postgres",
) -> Generator[Container]:
    """Start a Postgres container with dynamic port.

    Args:
        image: Docker image (postgres:15, pgvector/pgvector:pg16)
        password: DB password. Defaults to POSTGRES_PASSWORD env var.
        username: Database username
        dbname: Database name

    Yields:
        Container with postgresql:// URL and dynamic port
    """
    password = password or os.environ["POSTGRES_PASSWORD"]
    with PostgresContainer(image, username=username, password=password, dbname=dbname) as c:
        port = int(c.get_exposed_port(5432))
        yield Container(
            host="localhost",
            port=port,
            url=f"postgres://{username}:{password}@localhost:{port}/{dbname}",
        )


@contextmanager
def start_neo4j(password: str) -> Generator[Container]:
    """Start a Neo4j container with dynamic bolt port.

    Args:
        password: Neo4j auth password

    Yields:
        Container with bolt:// URL and dynamic port
    """
    with _start_container(
        "neo4j:latest",
        7687,
        env={"NEO4J_AUTH": f"neo4j/{password}"},
    ) as c:
        yield Container(
            host=c.host,
            port=c.port,
            url=f"bolt://localhost:{c.port}",
        )
