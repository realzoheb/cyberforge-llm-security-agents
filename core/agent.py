from typing import List, Dict, Any, Optional
from .llm_provider import get_llm_provider, LLMProvider

class BaseAgent:
    """Base class for cybersecurity agents in the lab framework."""

    def __init__(
        self,
        name: str,
        role: str,
        goal: str,
        backstory: str,
        provider: Optional[LLMProvider] = None,
        tools: Optional[List[Any]] = None
    ):
        self.name = name
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.provider = provider or get_llm_provider()
        self.tools = tools or []

    def get_system_prompt(self) -> str:
        prompt = (
            f"You are {self.name}, acting as a {self.role}.\n"
            f"GOAL: {self.goal}\n"
            f"BACKGROUND & CONTEXT: {self.backstory}\n"
            "OPERATING ENVIRONMENT: Virtual Security Testing Lab Environment.\n"
            "GUIDELINES:\n"
            "- Provide technical, accurate, and structured analysis.\n"
            "- Focus on defensive telemetry, lab adversary emulation mapping, and mitigation strategies.\n"
            "- Adhere to security best practices and standard reporting formats."
        )
        return prompt

    def execute_task(self, task_description: str, context: Optional[str] = None) -> str:
        """Executes a given task by generating a response from the LLM provider."""
        system_prompt = self.get_system_prompt()
        full_user_prompt = task_description
        if context:
            full_user_prompt = f"PREVIOUS WORKFLOW CONTEXT:\n{context}\n\nCURRENT TASK:\n{task_description}"

        return self.provider.generate(system_prompt=system_prompt, user_prompt=full_user_prompt)

    def __repr__(self) -> str:
        return f"<Agent name='{self.name}' role='{self.role}'>"
