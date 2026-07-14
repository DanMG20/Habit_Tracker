"""
Module responsible for building structural states required by specific UI interaction panels.
"""

from typing import Dict, Any, List, Set
from datetime import date


class PanelStateBuilder:
    """
    Factory class that shapes configuration and completion states 
    specifically tailored for checking, updating, and deleting habit panels.
    """

    def __init__(self, calendar_service: Any, executions_service: Any, habit_service: Any) -> None:
        self.calendar_service: Any = calendar_service
        self.executions_service: Any = executions_service
        self.habit_service: Any = habit_service

    def build_check_panel(self, target_date: date, habits: List[Dict[str, Any]]) -> Dict[str, Any]:
        completed_habits_on_date: Set[str] = self.executions_service.get_habits_completed_on_date(target_date)

        return {
            "habits": habits,
            "completed_habits": completed_habits_on_date,
            "categories": self.habit_service.get_categories()
        }

    def build_static_panel(self, habits: List[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "habits": habits,
        }