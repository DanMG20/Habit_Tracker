import customtkinter as ctk

import infrastructure.config.defaults as df
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

class GoalPanel(ctk.CTkScrollableFrame): 
    def __init__(self, master ,current_period,style_settings):
        super().__init__(master, corner_radius=df.CORNER_RADIUS, width= 100)
        self.static_header = "— Objetivos Trimestrales —"
        self.current_period = current_period
        self.fonts = style_settings["fonts"]

        self.build()


    def build(self):
        self.draw_static_header()
        self.draw_dinamic_header()

    def clear_widgets(self):
        pass

    def draw_static_header(self):
        ctk.CTkLabel(
            self,
            text=self.static_header,
            font=self.fonts["SMALL"],
            text_color=df.COLOR_BORDE,
        ).pack(pady=5)

    def draw_dinamic_header(self): 
                ctk.CTkLabel(
            self,
            text="Semana "+ self.current_period,
            font=self.fonts["SMALL"],
            text_color=df.COLOR_BORDE,
        ).pack(pady=5)
