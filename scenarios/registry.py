"""
Central registry for discovering and executing named security scenarios.
"""

from typing import Dict, Callable, List, Any
from core.workflow import Workflow

class ScenarioRegistry:
    def __init__(self):
        self._scenarios: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, description: str, builder_func: Callable[[], Workflow]):
        """Registers a new scenario by name."""
        self._scenarios[name.lower()] = {
            "name": name,
            "description": description,
            "builder": builder_func
        }

    def list_scenarios(self) -> Dict[str, str]:
        return {k: v["description"] for k, v in self._scenarios.items()}

    def get_all(self) -> Dict[str, Dict[str, Any]]:
        return self._scenarios

    def run_scenario(self, name: str) -> bool:
        key = name.lower()
        if key not in self._scenarios:
            return False
        workflow: Workflow = self._scenarios[key]["builder"]()
        workflow.run()
        return True

# Global Registry instance
registry = ScenarioRegistry()
