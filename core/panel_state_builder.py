"""Module responsible for building structural states required by specific UI interaction panels."""

from datetime import date
from typing import Any, Dict, List, Set


class PanelStateBuilder:
    """Factory class that shapes configuration and completion states.
    
    Tailored specifically for checking, updating, and deleting habit panels.
    """

    def __init__(
        self,
        calendar_service: Any,
        executions_service: Any,
        habit_service: Any
    ) -> None:
        """Initializes the builder with its required domain services.

        Args:
            calendar_service: Service handling calendar operations.
            executions_service: Service tracking habit completion history.
            habit_service: Service managing core habit rules and metadata.
        """
        self.calendar_service: Any = calendar_service
        self.executions_service: Any = executions_service
        self.habit_service: Any = habit_service

    def build_check_panel(
        self,
        target_date: date,
        habits: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Builds the interaction state for the checklist panel on a specific date.

        Filters habits ensuring only those scheduled for the target date are included.

        Args:
            target_date: The date context for the panel.
            habits: The global list of available habits to filter.

        Returns:
            A dictionary containing scheduled habits, completed habit IDs, 
            the current date, and active categories.
        """
        scheduled_habits: List[Dict[str, Any]] = [
            habit for habit in habits
            if self.habit_service.is_habit_scheduled_for_date(habit, target_date)
        ]
        
        completed_habits: Set[str] = self.executions_service.get_habits_completed_on_date(target_date)

        return {
            "habits": scheduled_habits,
            "completed": completed_habits,
            "date": target_date,
            "categories": self.habit_service.get_categories()
        }

    def build_static_panel(self, habits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Builds a static representation state of habits without date context.

        Args:
            habits: The list of habits to display.

        Returns:
            A dictionary containing the habits and an empty completion set.
        """
        return {
            "habits": habits,
            "completed": []
        }