from docker.models.containers import Container

from frontend_developer_agent.tools.docker_shell import DockerShellTool


def test_doker_shell_success(container: Container) -> None:
    tool = DockerShellTool(container=container)
    assert "aaa" in tool.run("echo 'aaa'")


def test_doker_shell_success_with_quotes(container: Container) -> None:
    tool = DockerShellTool(container=container)
    assert "The command successfully executed." in tool.run(
        'cd /root && git config --global user.email "frontend_developer_agent@github.com"'
    )


def test_doker_shell_error(container: Container) -> None:
    tool = DockerShellTool(container=container)
    assert 'lsaaa: command not found' in tool.run("lsaaa")
