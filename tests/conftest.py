import pytest
from docker.models.containers import Container

from frontend_developer_agent.utils import build_container


@pytest.fixture(scope="session")
def container() -> Container:
    container = build_container(None)
    yield container
    container.kill()
