"""
Scenario 01: Hello Agents Demo
Proves agent initialization, LLM provider connectivity, and multi-agent task execution.
"""

from core.agent import BaseAgent
from core.task import BaseTask
from core.workflow import Workflow
from agents.security_agents import create_security_analyst, create_detection_engineer

def build_hello_agents_scenario() -> Workflow:
    analyst = create_security_analyst()
    engineer = create_detection_engineer()

    task1 = BaseTask(
        name="Agent Self-Test & Lab Verification",
        description="Introduce yourself, verify connection to the LLM backend, and state your role in the lab.",
        agent=analyst,
        expected_output="Short confirmation message detailing agent status and lab operational readiness."
    )

    task2 = BaseTask(
        name="Defensive Handshake",
        description="Acknowledge the analyst's readiness and suggest 3 high-priority log sources for monitoring in a lab VM.",
        agent=engineer,
        expected_output="Structured bullet-point list of recommended Windows & Linux log sources."
    )

    return Workflow(
        name="Hello Agents Demo Scenario",
        description="Initial verification scenario to confirm environment configuration and agent task pipeline functionality.",
        tasks=[task1, task2]
    )
