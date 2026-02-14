from ui.panels.check_panel_base import CheckPanelBase
from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)

class YesterdayCheckPanel(CheckPanelBase):
    def __init__(self, master, fonts, theme_colors,date, get_state, on_date_check):
        super().__init__(
            master=master,
            fonts=fonts,
            theme_colors=theme_colors,
            date=date,
            get_habits= lambda : get_state()["habits"],
            get_completed_habits=lambda : get_state()["completed"],
            on_check=on_date_check,
            title="Selecciona el hábito para completarlo!",
            subtitle="(Esto marcará los hábitos como completados ayer)",
        )
        logger.info("Succesfully built")
