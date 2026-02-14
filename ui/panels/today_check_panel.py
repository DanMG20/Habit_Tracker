import customtkinter as ctk
from infrastructure.config import defaults as df
from utils.tooltip import Tooltip
from infrastructure.logging.logger import get_logger
from ui.panels.check_panel_base import CheckPanelBase
logger = get_logger(__name__)


class TodayCheckPanel(CheckPanelBase):
    def __init__(self, master, fonts, theme_colors, get_state,date, on_date_check):
        super().__init__(
            master=master,
            fonts=fonts,
            theme_colors=theme_colors,
            date=date,
            get_habits=lambda :get_state()["habits"],
            get_completed_habits= lambda: get_state()["completed"],
            on_check=on_date_check,
            title="Selecciona el hábito para completarlo!",
        )
