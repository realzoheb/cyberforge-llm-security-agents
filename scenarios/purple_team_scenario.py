"""
Scenario 03: Purple Team Emulation and Mitigation Workflow
Purple Team Agent designs adversary test plan -> Analyst defines defense telemetry -> Engineer builds Sigma detection.
"""

from core.workflow import Workflow
from agents.security_agents import create_purple_team_agent, create_security_analyst, create_detection_engineer
from tasks.security_tasks import task_adversary_emulation_plan, task_log_analysis, task_generate_sigma_rule

def build_purple_team_scenario() -> Workflow:
    purple_agent = create_purple_team_agent()
    analyst_agent = create_security_analyst()
    engineer_agent = create_detection_engineer()

    task1 = task_adversary_emulation_plan(purple_agent, target_technique="T1059.001 - PowerShell Execution")
    task2 = task_log_analysis(analyst_agent, log_data="Context from Purple Team test plan.")
    task3 = task_generate_sigma_rule(engineer_agent, threat_context="Context from test plan and analyst assessment.")

    return Workflow(
        name="Purple Team Emulation & Detection Exercise",
        description="Collaborative Purple Team scenario designing adversary tests, telemetry verification, and Sigma rule generation.",
        tasks=[task1, task2, task3]
    )
