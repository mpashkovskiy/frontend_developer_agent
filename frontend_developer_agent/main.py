from pathlib import Path

import hydra
from langchain.chat_models import ChatOpenAI
from langchain.tools.shell.tool import ShellTool
from langchain_community.tools.file_management.read import ReadFileTool
from langchain_community.tools.file_management.write import WriteFileTool
from langchain_experimental.plan_and_execute.planners.chat_planner import (
    load_chat_planner,
    SYSTEM_PROMPT,
)
from omegaconf import DictConfig
from frontend_developer_agent.chains.plan_and_execute import PlanAndExecute
from frontend_developer_agent.tools.feedback_adapter import FeedbackAdapterTool

from frontend_developer_agent.utils import (
    get_episodic_memory,
    load_agent_executor
)


@hydra.main(
    version_base=None,
    config_path="configs",
    config_name=Path(__file__).stem
)
def main(conf: DictConfig) -> None:
    tools = [
        ReadFileTool(),
        FeedbackAdapterTool.from_tool(
            base_tool=ShellTool(),
            feedback_cmd=conf.feedback_cmd,
        ),
        FeedbackAdapterTool.from_tool(
            base_tool=WriteFileTool(),
            feedback_cmd=conf.feedback_cmd,
        ),
        # create_retriever_tool(
        #     vector.as_retriever(),
        #     "episodic_memory",
        #     "Search for information about the project and the frameworks in use.",
        # )
    ]

    llm = ChatOpenAI(temperature=0)
    executor = load_agent_executor(llm, tools, verbose=True)
    planner = load_chat_planner(
        llm,
        system_prompt=get_episodic_memory() + SYSTEM_PROMPT
    )
    PlanAndExecute(
        executor=executor,
        planner=planner,
        verbose=True,
    ).run("Add transaction page with reciever and amount input fields and link the page from the main page of the application")
