import logging
import os
from pathlib import Path

import hydra
from hydra.core.hydra_config import HydraConfig
from langchain.chat_models import ChatOpenAI
from langchain_experimental.plan_and_execute import (
    PlanAndExecute,
    load_agent_executor,
    load_chat_planner,
)
from langchain.globals import set_debug
from omegaconf import DictConfig

from frontend_developer_agent.tools.docker_shell import DockerShellTool
from frontend_developer_agent.utils import build_container


@hydra.main(version_base=None,
            config_path="configs",
            config_name=Path(__file__).stem)
def main(_: DictConfig) -> None:
    set_debug(True)
    logger = logging.getLogger(__name__)

    app_path = os.path.join(HydraConfig.get().runtime.output_dir, "app")
    os.makedirs(app_path)
    container = build_container(app_path)
    tools = [
        DockerShellTool(container=container),
    ]

    model = ChatOpenAI(temperature=0)
    planner = load_chat_planner(model)
    executor = load_agent_executor(model, tools, verbose=True)
    agent = PlanAndExecute(planner=planner, executor=executor)

    scenarios = open("scenarios.txt", "r").read()
    prompt = (
        "Create Angular application described with the following scenarios:\n"
        + scenarios
    )
    try:
        agent.run(prompt)
    except Exception as e:
        logger.error(e)
    finally:
        container.kill()
        logger.info(f"------- Results are saved in {app_path} -------")
