from dataclasses import dataclass
from typing import Callable, Any


@dataclass
class MainUIActions:
    confirm_delete_habit: Callable[[Any], None]
    update_habit_event: Callable[[Any], None]
    habit_check_event: Callable[[Any], None]
    check_habit_yesterday_event: Callable[[Any], None]

    show_delete_panel: Callable[[], None]
    show_update_panel: Callable[[], None]
    show_yesterday_panel: Callable[[], None]
    show_today_panel: Callable[[], None]
    show_goals_panel: Callable[[], None]

    go_to_add_habit_view: Callable[[], None]
    go_to_graph_view: Callable[[], None]
