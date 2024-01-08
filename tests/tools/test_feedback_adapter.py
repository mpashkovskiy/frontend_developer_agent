from langchain.tools.shell.tool import ShellTool

from frontend_developer_agent.tools.feedback_adapter import FeedbackAdapterTool


def test_feedback_adapter_success() -> None:
    tool = FeedbackAdapterTool.from_tool(
        ShellTool(),
        "echo 'aaa'"
    )
    result = tool.run("echo '111'")
    assert "with result: aaa" in result
    assert "with result: 111" in result
