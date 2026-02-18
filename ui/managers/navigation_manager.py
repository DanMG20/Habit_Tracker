from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

class NavigationUIManager:

    def __init__(
        self,
        controller,
        top_nav_bar,
        graph_nav_bar,
        trigger_refresh,
        go_to_monthly_graph,
        go_to_yearly_graph,
    ):

        self.controller = controller
        self.top_nav_bar = top_nav_bar
        self.graph_nav_bar = graph_nav_bar

        self.go_to_monthly_graph = go_to_monthly_graph
        self.go_to_yearly_graph = go_to_yearly_graph
        self.trigger_refresh = trigger_refresh
        self.set_weekly_mode()


    def set_weekly_mode(self):

        self.top_nav_bar.bind_navigation(
            self.go_to_previous_week,
            self.go_to_next_week
        )

    def set_monthly_mode(self):
        self.graph_nav_bar.bind_navigation(self.go_to_yearly_graph,"monthly")
        self.top_nav_bar.bind_navigation(
            self.go_to_previous_month,
            self.go_to_next_month
        )
    def set_yearly_mode(self):
        self.graph_nav_bar.bind_navigation(self.go_to_monthly_graph,"yearly")
        self.top_nav_bar.bind_navigation(
            on_left=self.go_to_previous_year,
              on_right=self.go_to_next_year
        )
    def go_to_previous_week(self):
        moved = self.controller.go_previous_week()
        if moved:
            self.trigger_refresh("week_changed")

    def go_to_next_week(self):
        if self.controller.go_next_week():
            self.trigger_refresh("week_changed")

    def go_to_previous_month(self):
        if self.controller.go_to_previous_month():
            self.trigger_refresh("graph_changed")

    def go_to_next_month(self):
        if self.controller.go_to_next_month():
            self.trigger_refresh("graph_changed")

    def go_to_previous_year(self):
        if self.controller.go_to_previous_year():
            self.trigger_refresh("graph_changed")

    def go_to_next_year(self):
        if self.controller.go_to_next_year():
            self.trigger_refresh("graph_changed")

