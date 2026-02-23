from ui.panels.check_panel_base import CheckPanelBase


class YesterdayCheckPanel(CheckPanelBase):

    TITLE = "— Selecciona el hábito para completarlo! ✅ —"
    SUBTITLE = "(Esto marcará los hábitos como completados ayer)"


    state_key  ="panels.yesterday"
    events = {"habit_changed", "day_changed"}
    def __init__(self, master, style_settings, on_date_check):
        super().__init__(
            master=master,
            styles=style_settings,
            complete=on_date_check,
        )
