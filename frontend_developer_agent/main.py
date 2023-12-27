import os
from anyio import Path

from docker.client import DockerClient
from docker.models.containers import Container
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


@hydra.main(version_base=None,
            config_path="configs",
            config_name=Path(__file__).stem)
def main(_: DictConfig) -> None:
    set_debug(True)

    app_path = os.path.join(
        HydraConfig.get().runtime.output_dir,
        "app",
    )
    os.makedirs(app_path)

    container: Container = DockerClient.from_env().containers.run(
        "frontend_developer_agent",
        "sleep infinity",
        auto_remove=True,
        detach=True,
        volumes=[f"{app_path}:/app"],
        working_dir="/app",
    )
    tools = [
        DockerShellTool(container=container),
    ]

    model = ChatOpenAI(temperature=0)
    planner = load_chat_planner(model)
    executor = load_agent_executor(model, tools, verbose=True)
    agent = PlanAndExecute(planner=planner, executor=executor)

    scenario = open("scenarios.txt", "r").read()
    prompt = (
        "Create Angular application described with the following scenario"
        f":\n{scenario}"
    )
    try:
        agent.run(prompt)
    except Exception as e:
        print(e)
    finally:
        container.kill()
        print("----------------------------------------")
        print(f"Results are saved in {app_path}")
        print("----------------------------------------")
