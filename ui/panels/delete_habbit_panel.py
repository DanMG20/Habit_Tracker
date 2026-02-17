from infrastructure.logging.logger import get_logger
from ui.panels.check_panel_base import CheckPanelBase
logger = get_logger(__name__)



class DeleteHabitCheckPanel(CheckPanelBase):

    TITLE="Selecciona el hábito para eliminarlo"
    SUBTITLE="ESTA ACCIÓN NO SE PUEDE DESHACER"

    def __init__(
        self,
        master,
        style_settings,
        on_delete,
    ):
        super().__init__(
            master=master,
            on_delete=on_delete,
            style_settings=style_settings
        )

