"""
Scenario 02: Triage and Detection Pipeline
Simulates a multi-agent workflow: SOC Analyst triages log -> Detection Engineer writes Sigma Rule.
"""

from core.workflow import Workflow
from agents.security_agents import create_security_analyst, create_detection_engineer
from tasks.security_tasks import task_log_analysis, task_generate_sigma_rule

SAMPLE_SYS_LOG = """
[Sysmon Event 1] - Process Creation
Timestamp: 2026-08-09 14:22:01.412
Image: C:\\Windows\\System32\\cmd.exe
CommandLine: cmd.exe /c powershell -ExecutionPolicy Bypass -WindowStyle Hidden -Enc Q2hhbmdlTWVQYXNzd29yZA==
ParentImage: C:\\Windows\\System32\\wmic.exe
User: LAB-DOMAIN\\Administrator
Hashes: SHA256=A1B2C3D4E5F67890ABCDEF1234567890ABCDEF1234567890ABCDEF1234567890
"""

def build_log_analysis_scenario() -> Workflow:
    analyst = create_security_analyst()
    engineer = create_detection_engineer()

    triage_task = task_log_analysis(analyst, log_data=SAMPLE_SYS_LOG)
    detection_task = task_generate_sigma_rule(engineer, threat_context="Output from previous log analysis triage.")

    return Workflow(
        name="Log Analysis & Sigma Rule Pipeline",
        description="End-to-end workflow: Triaging encoded command execution logs and generating a Sigma rule.",
        tasks=[triage_task, detection_task]
    )
