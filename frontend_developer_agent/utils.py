import re
from typing import List

from langchain.agents.agent import AgentExecutor
from langchain.agents.structured_chat.base import StructuredChatAgent
from langchain.schema.language_model import BaseLanguageModel
from langchain.tools import BaseTool
from langchain.tools.shell.tool import ShellTool
from langchain_experimental.plan_and_execute.executors.base import (
    ChainExecutor
)

PREFIX = "Perform the following task one action at the time using only the following tools:"
TOOLS_SECTION = """Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or {tool_names}

Provide only ONE action per $JSON_BLOB, as shown:

```
{{{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}}}
```"""
FORMAT_INSTRUCTIONS = TOOLS_SECTION + """

Follow this format:

Task: input task to perform
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{{{
  "action": "Final Answer",
  "action_input": "Final response to human"
}}}}
```"""
SUFFIX = """Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation:.
Task:"""
HANDLE_PARSING_ERROR_MESSAGE = (
    "Action JSON is invalid. "
    "Perform one action at the time using only the following tools:"
)


def load_agent_executor(
    llm: BaseLanguageModel,
    tools: List[BaseTool],
    verbose: bool = False,
) -> ChainExecutor:
    agent = StructuredChatAgent.from_llm_and_tools(
        format_instructions=FORMAT_INSTRUCTIONS,
        llm=llm,
        prefix=get_episodic_memory() + PREFIX,
        suffix=SUFFIX,
        tools=tools,
    )
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        handle_parsing_errors=build_handle_parsing_error_message(tools),
        tools=tools,
        verbose=verbose,
    )
    return ChainExecutor(chain=agent_executor)


def get_episodic_memory():
    listing = ShellTool().run("tree /app/app -f -i -I node_modules")
    return (
        "You are a software engineer building an Angular application. "
        f"Here is the list of files in the project:\n\n{listing}\n\n"
    )


def build_handle_parsing_error_message(tools: List[BaseTool]) -> str:
    tool_strings = []
    for tool in tools:
        args_schema = re.sub("}", "}}", re.sub("{", "{{", str(tool.args)))
        tool_strings.append(
            f"{tool.name}: {tool.description}, args: {args_schema}"
        )
    formatted_tools = "\n".join(tool_strings)
    tool_names = ", ".join([tool.name for tool in tools])
    format_instructions = TOOLS_SECTION.format(tool_names=tool_names)
    return "\n\n".join([
        HANDLE_PARSING_ERROR_MESSAGE,
        formatted_tools,
        format_instructions
    ])
