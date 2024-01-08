from typing import Any

from langchain.tools import BaseTool
from langchain.tools.shell.tool import ShellTool


class FeedbackAdapterTool(BaseTool):
    args_schema: Any
    base_tool: BaseTool
    description: str
    feedback_cmd: str
    name: str

    @classmethod
    def from_tool(
        cls: "FeedbackAdapterTool", base_tool: BaseTool, feedback_cmd: str
    ) -> "FeedbackAdapterTool":
        return cls(
            args_schema=base_tool.args_schema,
            base_tool=base_tool,
            description=base_tool.description,
            feedback_cmd=feedback_cmd,
            name=base_tool.name,
        )

    def _run(
        self,
        **kwargs: Any,
    ) -> str:
        base_tool_result = self.base_tool._run(**kwargs)
        feedback = ShellTool().run(
            self.feedback_cmd,
            kwargs.get("run_manager")
        )
        if "error" in feedback.lower():
            return "\n\n".join([
                base_tool_result,
                "Error occured during the application testing:",
                feedback
            ]).strip()

        return base_tool_result
