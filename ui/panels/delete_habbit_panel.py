from infrastructure.logging.logger import get_logger
from ui.panels.check_panel_base import CheckPanelBase
logger = get_logger(__name__)



class DeleteHabitCheckPanel(CheckPanelBase):
    def __init__(
        self,
        master,
        fonts,
        theme_colors,
        get_habits,
        on_delete,
    ):
        super().__init__(
            master=master,
            fonts=fonts,
            theme_colors=theme_colors,
            date=None,
            get_habits=get_habits,
            get_completed_habits=lambda : set(),
            on_check=on_delete,
            title="Selecciona el hábito para eliminarlo",
            subtitle="ESTA ACCIÓN NO SE PUEDE DESHACER",
        )
        logger.info("Succesfully built")
