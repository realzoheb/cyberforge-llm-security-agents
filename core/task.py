from typing import Optional, Dict, Any
from .agent import BaseAgent

class BaseTask:
    """Encapsulates a specific security task assigned to an agent."""

    def __init__(
        self,
        name: str,
        description: str,
        agent: BaseAgent,
        expected_output: str = "Detailed structured security analysis markdown report.",
        inputs: Optional[Dict[str, Any]] = None
    ):
        self.name = name
        self.description = description
        self.agent = agent
        self.expected_output = expected_output
        self.inputs = inputs or {}

    def run(self, context: Optional[str] = None) -> str:
        """Runs the task using its assigned agent."""
        task_prompt = (
            f"TASK NAME: {self.name}\n"
            f"INSTRUCTIONS: {self.description}\n"
            f"EXPECTED OUTPUT FORMAT: {self.expected_output}"
        )
        if self.inputs:
            task_prompt += f"\nTASK INPUT DATA: {self.inputs}"

        return self.agent.execute_task(task_prompt, context=context)

    def __repr__(self) -> str:
        return f"<Task name='{self.name}' agent='{self.agent.name}'>"
