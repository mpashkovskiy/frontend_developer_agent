from typing import Optional

from docker.models.containers import Container
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain.tools import BaseTool


SUCCESS_MESSAGE = "The command successfully executed with result:\n{result}\n"
ERROR_MESSAGE = "The command failed to execute with error:\n{error}\n"


class DockerShellTool(BaseTool):
    name = "shell"
    description = "useful for when you need to execute linux shell commands"
    container: Container = None
    default_working_directory_absolute_path = "/app"

    def _run(
        self,
        command: str,
        working_directory_absolute_path: str = default_working_directory_absolute_path,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        # That approach is better because allows to interract with the process
        # process = subprocess.Popen(
        #     f"docker exec -it {self.container_id} ls {path}".split(" "),
        #     shell=False,
        #     stdout=subprocess.PIPE,
        #     stderr=subprocess.PIPE
        # )
        # res = process.stdout.readlines().decode("utf-8").split("\n")

        result = self.container.exec_run(
            command,
            workdir=working_directory_absolute_path,
            # If ``stream=True``, a generator yielding response chunks.
        )
        if result.exit_code != 0:
            return ERROR_MESSAGE.format(error=result.output.decode("utf-8"))

        return SUCCESS_MESSAGE.format(result=result.output.decode("utf-8"))
