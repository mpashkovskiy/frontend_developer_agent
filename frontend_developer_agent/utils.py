from docker.client import DockerClient
from docker.models.containers import Container


def build_container(app_path: str,
                    image: str = "frontend_developer_agent") -> Container:
    container: Container = DockerClient.from_env().containers.run(
        image,
        "sleep infinity",
        auto_remove=True,
        detach=True,
        volumes=[f"{app_path}:/app"] if app_path else [],
        working_dir="/app",
    )
    return container
