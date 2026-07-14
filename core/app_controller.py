"""
Module acting as the central Application Controller.

This controller implements the Facade pattern, coordinating actions between 
the UI layer and the underlying domain services while maintaining clean decoupling.
"""

from typing import List, Dict, Any, Callable
from datetime import date

from core.runtime import restart_application
from core.view_state_builder import ViewStateBuilder
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class AppController:
    """
    Main controller coordinates requests from the UI and delegates them to services.
    
    It encapsulates the system services and exposes clean unified actions 
    to the interface components.
    """

    def __init__(
        self,
        settings_service: Any,
        habit_service: Any,
        calendar: Any,
        reset_service: Any,
        executions_service: Any,
        metrics_service: Any,
        quote_service: Any,
        goal_service: Any,
        style_service: Any,
        close_db_connection: Callable[[], None],
    ) -> None:
        """
        Initializes the AppController injecting all required application services.

        Args:
            settings_service: Service managing configuration and user preferences.
            habit_service: Service managing habit CRUD operations.
            calendar: Service tracking current dates, tracking scope, and history.
            reset_service: Service handling database resets.
            executions_service: Service tracking historical log completion of habits.
            metrics_service: Service responsible for calculating progress analytics.
            quote_service: Service managing daily dynamic quotes.
            goal_service: Service managing quarterly goals operations.
            style_service: Service managing visual customization and styling parameters.
            close_db_connection (Callable[[], None]): Callback to cleanly close the database connection.
        """
        self.calendar_service: Any = calendar
        self.metrics_service: Any = metrics_service
        self.quote_service: Any = quote_service
        self.reset_service: Any = reset_service
        self.executions_service: Any = executions_service
        self.habit_service: Any = habit_service
        self.goal_service: Any = goal_service
        self.settings_service: Any = settings_service
        self.style_service: Any = style_service
        self.close_db_connection: Callable[[], None] = close_db_connection
        
        self.view_state_builder: ViewStateBuilder = ViewStateBuilder(
            calendar_service=calendar,
            metrics_service=metrics_service,
            goal_service=goal_service,
            habit_service=habit_service,
            executions_service=executions_service,
            quote_service=quote_service,
        )
        self.settings_service.apply()

    # ======================== STATE ===================
    def build_view_state(self) -> Dict[str, Any]:
        """
        Builds the unified state snapshot required to render UI views.

        Returns:
            Dict[str, Any]: Consolidated dictionary payload mapping current UI context data.
        """
        return self.view_state_builder.build()

    # ======================== NAV ===================
    def go_previous_week(self) -> Any:
        return self.calendar_service.go_to_previous_week()

    def go_next_week(self) -> Any:
        return self.calendar_service.go_to_next_week()
 
    def go_to_previous_month(self) -> Any:
        return self.calendar_service.go_to_previous_month()

    def go_to_next_month(self) -> Any:
        return self.calendar_service.go_to_next_month()

    def go_to_previous_year(self) -> Any:
        return self.calendar_service.go_to_previous_year()

    def go_to_next_year(self) -> Any:
        return self.calendar_service.go_to_next_year()
    
    # ======================== QUOTES ===================
    def get_quote(self) -> Dict[str, Any]:
        return self.quote_service.get_quote()

    def get_quotes(self) -> List[Dict[str, Any]]:
        return self.quote_service.get_all_quotes()
    
    def add_quotes(self, quotes: List[Dict[str, Any]]) -> None:
        self.quote_service.add_quotes(quotes)

    def update_quote(self, quote_id: int, new_quote: str, new_author: str) -> None:
        self.quote_service.update_quote(quote_id, new_quote, new_author) 

    def delete_quote(self, quote_id: int) -> None:
        self.quote_service.delete_selected_quote(quote_id)

    # ======================== HABITS ===================
    def get_habit_by_id(self, habit_id: int) -> Dict[str, Any]: 
        return self.habit_service.get_by_id(habit_id)
    
    def get_habit_categories(self) -> List[str]:
        return self.habit_service.get_categories()
    
    def update_habit(self, habit: Dict[str, Any]) -> None:
        self.habit_service.update(habit)

    def add_new_habit(self, habit: Dict[str, Any]) -> None: 
        self.habit_service.add_new(habit)
    
    def delete_habit(self, habit_id: int) -> None: 
        self.habit_service.delete_by_id(habit_id)

    def get_all_habits(self) -> List[Dict[str, Any]]:
        return self.habit_service.get_all()

    # ======================== GOALS ===================
    def complete_goal(self, goal_id: int) -> None:
        return self.goal_service.complete_goal(goal_id, self._get_today())
    
    def get_goals(self) -> List[Dict[str, Any]]:
        return self.goal_service.get_all()
    
    def delete_goal(self, goal_id: int) -> None: 
        self.goal_service.delete_by_id(goal_id)

    def update_goal(self, goal_id: int, goal_name: str, period: str, year: int) -> None: 
        self.goal_service.update(goal_id, goal_name, period, year)
        
    def add_goal(self, goal: Dict[str, Any]) -> None:
        self.goal_service.insert(
            goal["name"], 
            goal["period_year"],
            goal["period_quarter"],
            self._get_today()
        )

    # ======================== EXECUTIONS ===================
    def check_habit_today(self, habit_name: str) -> None:
        """Logs a standard validation mark checkpoint execution event on today's date."""
        self.executions_service.complete_habit_on_date(habit_name, self._get_today())
        logger.info(f"Habit completed today: '{habit_name}'")

    def check_habit_yesterday(self, habit_name: str) -> None:
        """Logs a baseline post-dated performance completion checkpoint execution event on yesterday's date."""
        self.executions_service.complete_habit_on_date(habit_name, self._get_yesterday())
        logger.info(f"Habit completed yesterday: '{habit_name}'")

    # ======================== CALENDAR ===================
    def _get_today(self) -> date:
        return self.calendar_service.get_calendar_state()["today"]

    def _get_yesterday(self) -> date:
        return self.calendar_service.get_calendar_state()["yesterday"]

    def get_current_period(self) -> Any:
        return self.calendar_service.get_current_period()
    
    def get_current_years(self) -> List[int]:
        return self.calendar_service.get_current_years()
        
    def verify_date(self) -> bool:
        """Verifies if the real-world operational day transition threshold occurred."""
        return self.calendar_service.has_day_changed()

    # ======================== SETTINGS ===================
    def get_styles(self) -> Dict[str, Any]: 
        return self.style_service.get_style_settings()

    def update_theme(self, new_theme: str) -> None:
        self.settings_service.update_theme(new_theme)

    def update_appearance(self, new_appearance: str) -> None:
        self.settings_service.update_appearance(new_appearance)

    def update_font(self, new_font: str) -> None:
        self.settings_service.update_font(new_font)

    def reset_files(self) -> None:
        """Closes all operational handlers and cleans up system persistent data storage completely."""
        self.close_db()
        self.reset_service.reset_files()

    def close_db(self) -> None:
        self.close_db_connection()

    def restart(self) -> None: 
        restart_application()