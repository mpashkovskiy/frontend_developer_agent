import logging
from pathlib import Path

import hydra
from hydra.core.hydra_config import HydraConfig
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.chat_models import ChatOpenAI
from langchain.globals import set_debug
from langchain_experimental.plan_and_execute import load_chat_planner
from omegaconf import DictConfig

from frontend_developer_agent.chains.plan_and_execute import PlanAndExecute
from frontend_developer_agent.tools.docker_shell import DockerShellTool
from frontend_developer_agent.utils import (
    load_agent_executor,
    prepare_environment
)


@hydra.main(
    version_base=None,
    config_path="configs",
    config_name=Path(__file__).stem
)
def main(_: DictConfig) -> None:
    set_debug(True)
    logger = logging.getLogger(__name__)

    app_path, container = prepare_environment()
    tools = [
        DockerShellTool(container=container),
    ] + FileManagementToolkit(
        root_dir=HydraConfig.get().runtime.output_dir,
        selected_tools=["read_file", "write_file"],
    ).get_tools()

    model = ChatOpenAI(temperature=0)
    agent = PlanAndExecute(
        executor=load_agent_executor(model, tools),
        container=container,
        planner=load_chat_planner(model),
    )

    prompt = (
        "Create Angular application described with the following scenarios:\n"
        + open("scenarios.txt", "r").read()
    )
    try:
        agent.run(prompt)
    except Exception as e:
        logger.error(e)
    finally:
        container.kill()
        logger.info(f"------- Results are saved in {app_path} -------")
