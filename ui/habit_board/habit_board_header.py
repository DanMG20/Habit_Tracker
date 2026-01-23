import customtkinter as ctk
from infrastructure.config import defaults as df
from ui.dialogs.view_settings import (COLUMN_HABIT_TABLE_WIDTH)
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

class HabitBoardHeader(ctk.CTkFrame):

    def __init__(self,master,fonts, theme_colors,on_check_yesterday, get_week_days, today):
        super().__init__(master,corner_radius=df.CORNER_RADIUS,fg_color=theme_colors["frame"])
        self.master = master
        self.fonts = fonts 
        self.theme_colors =theme_colors
        self.on_check_yesterday = on_check_yesterday
        self.week_days = get_week_days
        self.today = today
        
        self.build()
        
        logger.info("Succesfully Build")


    def build(self):
        self.draw_habit_board_header()
        


    def draw_habit_board_header(self):
        # --------------------------------------FRAME
        self.go_yesterday_button = ctk.CTkButton(
            self,
            text="¿Olvidaste marcar ayer?",
            command=self.on_check_yesterday,
            width=COLUMN_HABIT_TABLE_WIDTH,
            font=self.fonts["SMALL"],
        )
        self.go_yesterday_button.grid(
            row=0, column=0, sticky="nsew", padx=df.PADX, pady=df.PADY
        )
        # Labels dias actuales
        for indice, dia in enumerate(self.week_days):
            if dia < self.today:
                color_label = self.theme_colors["top_frame"]
            elif dia == self.today:
                color_label = self.theme_colors["button"]
            elif dia > self.today:
                color_label = self.theme_colors["progressbar"]

            ctk.CTkLabel(
                self,
                text=dia.day,
                font=self.fonts["SMALL"],
                fg_color=color_label,
                corner_radius=999,
            ).grid(row=0, column=indice + 1, sticky="nsew", padx=1, pady=df.PADY)
            self.columnconfigure(indice + 1, weight=1, uniform="col")
        encabezados = [
            "Actividad",
            "Domingo",
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
        ]
        for ind, encabezado in enumerate(encabezados):
            ctk.CTkLabel(
                self, text=encabezado, font=self.fonts["SMALL"]
            ).grid(
                row=1,
                column=ind,
                sticky="nsew",
                padx=2,
                pady=df.PADY,
            )
