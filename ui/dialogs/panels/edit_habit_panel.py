from infrastructure.logging.logger import get_logger
from ui.dialogs.panels.check_panel_base import CheckPanelBase
logger = get_logger(__name__)



class UpdateHabitCheckPanel(CheckPanelBase):
    def __init__(
        self,
        master,
        fonts,
        theme_colors,
        get_habits,
        on_edit,
    ):
        super().__init__(
            master=master,
            fonts=fonts,
            theme_colors=theme_colors,
            date=None,
            get_habits=get_habits,
            get_completed_habits=lambda : set(),
            on_check=on_edit,
            title="Selecciona el hábito para EDITARLO",
        )

        logger.info("Succesfully built")

