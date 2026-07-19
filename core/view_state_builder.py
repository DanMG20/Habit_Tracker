"""
Module responsible for aggregating domain service data to build the UI state snapshot.
"""

from typing import Dict, Any, List
from core.graph_state_builder import GraphStateBuilder
from core.panel_state_builder import PanelStateBuilder
from core.board_state_builder import BoardStateBuilder
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class ViewStateBuilder:
    """
    Coordinates and combines data from various domain services to produce 
    a single unified application state snapshot for the presentation layer.
    """

    def __init__(
        self,
        calendar_service: Any,
        habit_service: Any,
        executions_service: Any,
        metrics_service: Any,
        quote_service: Any,
        goal_service: Any,
    ) -> None:
        self.calendar_service: Any = calendar_service
        self.habit_service: Any = habit_service
        self.executions_service: Any = executions_service
        self.metrics_service: Any = metrics_service
        self.goal_service: Any = goal_service 
        self.quote_service: Any = quote_service
        
        self.graph_builder: GraphStateBuilder = GraphStateBuilder(
            calendar_service,
            metrics_service
        )
        self.panel_builder: PanelStateBuilder = PanelStateBuilder(
            calendar_service,
            executions_service,
            habit_service
        )
        self.board_builder: BoardStateBuilder = BoardStateBuilder(calendar_service)

    def build(self) -> Dict[str, Any]:
        """
        Gathers and processes metrics, executions, goals, and calendar logs 
        to compile the final view state dictionary.

        Returns:
            Dict[str, Any]: The fully constructed UI state data map payload.
        """
        habits: List[Dict[str, Any]] = self.habit_service.get_all()
        executions: List[Dict[str, Any]] = self.executions_service.get_all()

        calendar_state: Dict[str, Any] = self.calendar_service.get_calendar_state()
        logger.debug(f"Compiling UI state snapshot. Current calendar context: {calendar_state}")
        
        headers: List[str] = self.calendar_service.get_date_headers()
        week_days: List[Any] = self.calendar_service.get_current_week_days()
        month: Any = self.calendar_service.get_month_nav()
        month_year: Any = self.calendar_service.get_year_month_nav()
        year_nav: int = self.calendar_service.get_year()

        today: Any = calendar_state["today"]
        yesterday: Any = calendar_state["yesterday"]
        current_year: int = calendar_state["current_year"]
        current_quarter_period: str = calendar_state["current_period"]

        performances: Dict[str, Any] = self.metrics_service.calculate_all_performances(
            habits=habits,
            executions=executions,
            current_week_days=week_days,
            current_month=month,
            current_month_year=month_year,
            current_year=year_nav,
            reference_date=today
        )

        panels: Dict[str, Any] = {
            "today": self.panel_builder.build_check_panel(today, habits),
            "yesterday": self.panel_builder.build_check_panel(yesterday, habits),
            "update": self.panel_builder.build_static_panel(habits),
            "delete": self.panel_builder.build_static_panel(habits),
            "goals": {
                "goals": self.goal_service.get_all(),
                "current_goals": self.goal_service.get_from_quarter(current_quarter_period, current_year),
                "current_period": self.calendar_service.get_current_period(),
            },
            "graph_goals": {
                "goals_per_year": self.goal_service.get_all_per_year(year_nav),
                "rate": self.goal_service.get_rate_per_year(year_nav)
            }
        }

        board: Any = self.board_builder.build(
            habits,
            executions,
            today,
            week_days
        )

        graphs: Any = self.graph_builder.build(
            month_year,
            performances
        )

        return {
            "quote": self.quote_service.get_quote(),
            "headers": headers,
            "performances": {
                "weekly": performances["weekly"],
                "monthly": performances["monthly"],
                "yearly": performances["yearly"]["yearly"], 
            },
            "panels": panels,
            "habit_board": board,
            "graphs": graphs,
            "current_period": self.calendar_service.get_current_period(),
            "current_years": self.calendar_service.get_current_years(),
            "habit_categories": self.habit_service.get_categories(),
        }