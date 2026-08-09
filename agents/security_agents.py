"""
Modular specialized security agents for lab scenarios.
"""

from core.agent import BaseAgent
from core.llm_provider import LLMProvider
from typing import Optional

def create_security_analyst(provider: Optional[LLMProvider] = None) -> BaseAgent:
    return BaseAgent(
        name="Analyst-Alpha",
        role="SOC Security Analyst",
        goal="Triage telemetry logs, detect anomalies, identify attack patterns, and produce incident reports.",
        backstory="Senior SOC analyst experienced in Windows Event Logs, Sysmon, Linux auditd, and network packet capture triage.",
        provider=provider
    )

def create_detection_engineer(provider: Optional[LLMProvider] = None) -> BaseAgent:
    return BaseAgent(
        name="Sentinel-Beta",
        role="Detection Engineer",
        goal="Design, construct, and validate SIEM/Sigma rules, YARA signatures, and behavioral detections based on threat intel.",
        backstory="Detection engineer focused on translating adversary behaviors (TTPs) into robust, low-false-positive detection logic.",
        provider=provider
    )

def create_purple_team_agent(provider: Optional[LLMProvider] = None) -> BaseAgent:
    return BaseAgent(
        name="Aegis-Gamma",
        role="Purple Team Specialist",
        goal="Plan controlled adversary emulation tests mapped to MITRE ATT&CK and assess defense coverage.",
        backstory="Purple team practitioner specializing in aligning offensive test plans with defensive verification in lab setups.",
        provider=provider
    )
