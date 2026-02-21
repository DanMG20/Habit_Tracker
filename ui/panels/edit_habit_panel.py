from ui.panels.check_panel_base import CheckPanelBase


class UpdateHabitCheckPanel(CheckPanelBase):

    TITLE = "— Selecciona el hábito para editarlo —"
    SUBTITLE = ("NO SE PUEDE DESHACER")

    state_key  ="panels.update"
    events = {"habit_changed", "day_changed"}

    def __init__(self, master, style_settings, on_edit):
        super().__init__(
            master=master,
            style_settings=style_settings,
            complete=on_edit,
        )

