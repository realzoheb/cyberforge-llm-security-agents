"""
Reusable task definitions for common security operations.
"""

from core.task import BaseTask
from core.agent import BaseAgent
from typing import Dict, Any, Optional

def task_log_analysis(agent: BaseAgent, log_data: str) -> BaseTask:
    return BaseTask(
        name="Log Triage & Artifact Analysis",
        description=(
            "Analyze the provided log data or security event snippet. "
            "Identify suspicious indicators, affected entities, technique indicators, and assign a severity rating."
        ),
        agent=agent,
        expected_output="Structured incident report with Summary, Key Indicators, Affected Host, Severity (Low/Med/High/Critical), and Recommended Action.",
        inputs={"log_sample": log_data}
    )

def task_generate_sigma_rule(agent: BaseAgent, threat_context: str) -> BaseTask:
    return BaseTask(
        name="Sigma Detection Rule Generation",
        description=(
            "Based on the threat behavior analysis provided, write a valid YAML-formatted Sigma detection rule. "
            "Include proper title, status, description, logsource, detection logic, and level."
        ),
        agent=agent,
        expected_output="YAML formatted Sigma Rule with detailed explanation of detection logic.",
        inputs={"threat_context": threat_context}
    )

def task_adversary_emulation_plan(agent: BaseAgent, target_technique: str) -> BaseTask:
    return BaseTask(
        name="Adversary Emulation Test Plan",
        description=(
            f"Develop a safe, lab-only adversary emulation test plan for MITRE ATT&CK technique: {target_technique}. "
            "Outline safe powershell/cmd test commands to execute in a VM, telemetry expected to be generated, and defensive verification steps."
        ),
        agent=agent,
        expected_output="Step-by-step Lab Test Plan with Commands, Telemetry Log Sources to inspect, and Cleanup Steps.",
        inputs={"technique": target_technique}
    )
