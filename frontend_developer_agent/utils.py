import logging
import os
from typing import List

from docker.client import DockerClient
from docker.models.containers import Container
from hydra.core.hydra_config import HydraConfig
from langchain.agents.agent import AgentExecutor
from langchain.agents.structured_chat.base import StructuredChatAgent
from langchain.schema.language_model import BaseLanguageModel
from langchain.tools import BaseTool
from langchain_experimental.plan_and_execute.executors.base import ChainExecutor

from frontend_developer_agent.tools.docker_shell import DEFAULT_WORKING_DIRECTORY


HUMAN_MESSAGE_TEMPLATE = """Previous steps: {previous_steps}

Current directory structure:
{directory_structure}

Current objective: {current_step}

{agent_scratchpad}"""


def build_container(
    app_path: str,
    image: str = "frontend_developer_agent"
) -> Container:
    logger = logging.getLogger(__name__)
    try:
        container: Container = DockerClient.from_env().containers.run(
            image,
            "sleep infinity",
            auto_remove=True,
            detach=True,
            volumes=(
                [f"{app_path}:{DEFAULT_WORKING_DIRECTORY}"]
                if app_path
                else []
            ),
            working_dir=DEFAULT_WORKING_DIRECTORY,
        )
        return container
    except Exception as e:
        logger.exception("Failed to build container")
        raise e


def load_agent_executor(
    llm: BaseLanguageModel,
    tools: List[BaseTool],
) -> ChainExecutor:
    input_variables = [
        "previous_steps",
        "directory_structure",
        "current_step",
        "agent_scratchpad",
    ]
    template = HUMAN_MESSAGE_TEMPLATE
    agent = StructuredChatAgent.from_llm_and_tools(
        llm,
        tools,
        human_message_template=template,
        input_variables=input_variables,
    )
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, handle_parsing_errors=True
    )
    return ChainExecutor(chain=agent_executor)


def prepare_environment():
    app_path = os.path.join(HydraConfig.get().runtime.output_dir, "app")
    os.makedirs(app_path)
    container = build_container(app_path)
    return app_path, container
