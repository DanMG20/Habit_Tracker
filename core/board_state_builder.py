"""
Module responsible for building the state specific to the habit tracking board.
"""

from typing import Dict, Any, List
from datetime import date


class BoardStateBuilder:
    """
    Factory class that structures and combines configuration data, daily records, 
    and timeline periods to yield the state required by the habit board UI.
    """

    def __init__(self, calendar_service: Any) -> None:
        self.calendar_service: Any = calendar_service

    def build(
        self, 
        habits: List[Dict[str, Any]], 
        executions: List[Dict[str, Any]], 
        today: date, 
        week_days: List[date]
    ) -> Dict[str, Any]:
        return {
            "today": today,
            "habits": habits,
            "executions": executions,
            "week_days": week_days,
            "week_start": self.calendar_service.calculate_week_start()
        }