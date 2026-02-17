import customtkinter as ctk
from infrastructure.config import defaults as df
from ui.dialogs.view_settings import (COLUMN_HABIT_TABLE_WIDTH)
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

class HabitBoardHeader(ctk.CTkFrame):

    def __init__(self, master,style_settings, on_check_yesterday_event):
        super().__init__(master,
                         corner_radius=df.CORNER_RADIUS,
                         fg_color=style_settings["colors"]["frame"])

        self.fonts = style_settings["fonts"]
        self.theme_colors = style_settings["colors"]
        self.on_check_yesterday_event = on_check_yesterday_event
        self.date_labels = []
        self.week_days = []
        self.today = None

        self.build()

    def build(self):
        self.draw_habit_board_header()

    def refresh(self, habit_board_state):   
        week_days = habit_board_state.get("week_days", [])
        today = habit_board_state.get("today")

        for label, dia in zip(self.date_labels, week_days):

            if dia < today:
                color_label = self.theme_colors["top_frame"]
            elif dia == today:
                color_label = self.theme_colors["button"]
            else:
                color_label = self.theme_colors["progressbar"]

            label.configure(
                text=dia.day,
                fg_color=color_label
            )

    def clean_dates(self):
        for widget in self.winfo_children():
            info = widget.grid_info()

            if info.get("row") == 0 and info.get("column") != 0:
                widget.destroy()


    def draw_habit_board_header(self):

        # 🔘 Botón (se crea una sola vez)
        self.go_yesterday_button = ctk.CTkButton(
            self,
            text="¿Olvidaste marcar ayer?",
            command=self.on_check_yesterday_event,
            width=COLUMN_HABIT_TABLE_WIDTH,
            font=self.fonts["SMALL"],
        )
        self.go_yesterday_button.grid(
            row=0, column=0, sticky="nsew",
            padx=df.PADX, pady=df.PADY
        )

        # 📅 Crear 7 labels vacías solo una vez
        for i in range(7):
            label = ctk.CTkLabel(
                self,
                text="",
                font=self.fonts["SMALL"],
                corner_radius=999,
            )
            label.grid(
                row=0,
                column=i + 1,
                sticky="nsew",
                padx=1,
                pady=df.PADY
            )
            self.columnconfigure(i + 1, weight=1, uniform="col")

            self.date_labels.append(label)

        # 🏷 Encabezados constantes (no cambian nunca)
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
                self,
                text=encabezado,
                font=self.fonts["SMALL"]
            ).grid(
                row=1,
                column=ind,
                sticky="nsew",
                padx=2,
                pady=df.PADY,
            )
