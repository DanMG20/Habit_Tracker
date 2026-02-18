from ui.navigation.top_nav_bar import TopNavBar
from ui.date_header import DateHeader
from ui.performance_bar import PerformanceBar
from ui.panels.goal_panel import GoalPanel
from ui.panels.delete_habbit_panel import DeleteHabitCheckPanel
from ui.panels.yesterday_check_panel import YesterdayCheckPanel
from ui.panels.today_check_panel import TodayCheckPanel
from ui.panels.edit_habit_panel import UpdateHabitCheckPanel
from ui.habit_board.habit_board import HabitBoard
from ui.navigation.bottom_nav_bar import BottomNavBar

from .main_views import MainViews


class MainViewBuilder:

    @staticmethod
    def build(master, style_settings, actions) -> MainViews:

        top_nav_bar = TopNavBar(master, style_settings)

        date_header = DateHeader(master, style_settings)

        performance_bar = PerformanceBar(master, style_settings)

        goal_panel = GoalPanel(
            master=master,
            complete_goal=master.complete_goal_event,
            style_settings=style_settings,
        )

        delete_check_panel = DeleteHabitCheckPanel(
            master=master,
            style_settings=style_settings,
            on_delete=actions.confirm_delete_habit,
        )

        yesterday_check_panel = YesterdayCheckPanel(
            master=master,
            style_settings=style_settings,
            on_date_check=actions.check_habit_yesterday_event,
        )

        today_check_panel = TodayCheckPanel(
            master=master,
            style_settings=style_settings,
            on_date_check=actions.habit_check_event,
        )

        update_check_panel = UpdateHabitCheckPanel(
            master=master,
            style_settings=style_settings,
            on_edit=actions.update_habit_event,
        )

        habit_board = HabitBoard(
            master=master,
            style_settings=style_settings,
            show_yesterday_check_panel=actions.show_yesterday_panel,
            show_today_panel=actions.show_today_panel,
        )

        bottom_nav_bar = BottomNavBar(
            master=master,
            style_settings=style_settings,
            show_goals_panel=actions.show_goals_panel,
            show_edit_panel=actions.show_update_panel,
            show_delete_panel=actions.show_delete_panel,
            go_to_add_habit_view=actions.go_to_add_habit_view,
            go_to_graph_view=actions.go_to_graph_view,
        )

        return MainViews(
            top_nav_bar=top_nav_bar,
            date_header=date_header,
            performance_bar=performance_bar,
            goal_panel=goal_panel,
            delete_check_panel=delete_check_panel,
            update_check_panel=update_check_panel,
            yesterday_check_panel=yesterday_check_panel,
            today_check_panel=today_check_panel,
            habit_board=habit_board,
            bottom_nav_bar=bottom_nav_bar,
        )
