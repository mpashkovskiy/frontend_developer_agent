from docker.models.containers import Container

from frontend_developer_agent.tools.docker_shell import ERROR_MESSAGE, SUCCESS_MESSAGE, DockerShellTool


def test_doker_shell_success(container: Container) -> None:
    tool = DockerShellTool(container=container)
    assert tool.run(
        "echo 'aaa'") == SUCCESS_MESSAGE.format(result="aaa\n")


def test_doker_shell_error(container: Container) -> None:
    tool = DockerShellTool(container=container)
    assert tool.run(
        "lsaaa") == ERROR_MESSAGE.format(error='OCI runtime exec failed: exec failed: unable to start container process: exec: "lsaaa": executable file not found in $PATH: unknown\r\n')
