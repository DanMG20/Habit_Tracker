from core.graph_state_builder import GraphStateBuilder
from core.panel_state_builder import PanelStateBuilder
from core.board_state_builder import BoardStateBuilder

from infrastructure.logging.logger import get_logger 
logger = get_logger(__name__)
class ViewStateBuilder:

    def __init__(self, calendar_service, habit_service, executions_service, metrics_service, quote_service, goal_service):
        self.calendar_service = calendar_service
        self.habit_service = habit_service
        self.executions_service = executions_service
        self.metrics_service = metrics_service
        self.goal_service = goal_service 
        self.quote_service = quote_service
        self.graph_builder = GraphStateBuilder(
            calendar_service,
            metrics_service
            )
        self.panel_builder = PanelStateBuilder(
            calendar_service,
            executions_service
        )

        self.board_builder = BoardStateBuilder(calendar_service)


    def build(self):

        habits = self.habit_service.get_all()
        executions = self.executions_service.get_all()

        calendar_state = self.calendar_service.get_calendar_state()
        headers = self.calendar_service.get_date_headers()

        week_days = self.calendar_service.get_current_week_days()
        month = self.calendar_service.get_month_nav()

        month_year = self.calendar_service.get_year_month_nav()
        year_nav = self.calendar_service.get_year()


        today = calendar_state["today"]
        yesterday = calendar_state["yesterday"]

        # ==============================
        # 2️⃣ Calcular métricas UNA sola vez
        # ==============================

        performances = self.metrics_service.calculate_all_performances(
            habits=habits,
            executions=executions,
            current_week_days=week_days,
            current_month=month,
            current_month_year=month_year,
            current_year=year_nav,
        )

        panels = {
            "today": self.panel_builder.build_check_panel(today, habits),
            "yesterday": self.panel_builder.build_check_panel(yesterday, habits),
            "update": self.panel_builder.build_static_panel(habits),
            "delete": self.panel_builder.build_static_panel(habits),
            "goals": {
                "goals": self.goal_service.get_all(),
                "current_period": self.calendar_service.get_current_period(),
                    },
            "graph_goals": {
                "goals_per_year": self.goal_service.get_all_per_year(year_nav),
                "rate": self.goal_service.get_rate_per_year(year_nav)
            }
            }

        board = self.board_builder.build(
            habits,
            executions,
            today,
            week_days
        )

        graphs = self.graph_builder.build(
            habits,
            executions,
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
            "graphs":graphs,
            "current_period": self.calendar_service.get_current_period(),
            "current_years": self.calendar_service.get_current_years(),
            "habit_categories": self.habit_service.get_categories(),
        }
    



    


