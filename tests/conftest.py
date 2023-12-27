import pytest
from docker.client import DockerClient
from docker.models.containers import Container


@pytest.fixture(scope="session")
def container() -> Container:
    docker_client = DockerClient.from_env()
    container: Container = docker_client.containers.run(
        "ubuntu",
        "sleep infinity",
        auto_remove=True,
        detach=True,
        working_dir="/app",
    )
    yield container
    container.kill()
