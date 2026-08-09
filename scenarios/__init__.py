"""
Scenario registry loader - registers all available scenarios centrally.
"""

from .registry import registry
from .hello_agents import build_hello_agents_scenario
from .log_analysis_scenario import build_log_analysis_scenario
from .purple_team_scenario import build_purple_team_scenario

def register_all_scenarios():
    registry.register(
        name="hello_agents",
        description="Verify LLM provider setup and basic multi-agent communication.",
        builder_func=build_hello_agents_scenario
    )
    registry.register(
        name="log_analysis",
        description="Triage suspicious log snippet and generate a corresponding Sigma detection rule.",
        builder_func=build_log_analysis_scenario
    )
    registry.register(
        name="purple_team",
        description="Plan controlled adversary emulation (T1059.001) and produce defensive detections.",
        builder_func=build_purple_team_scenario
    )

# Execute auto-registration upon import
register_all_scenarios()
