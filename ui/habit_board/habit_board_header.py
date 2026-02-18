import customtkinter as ctk
from infrastructure.config import defaults as df
from ui.dialogs.view_settings import (COLUMN_HABIT_TABLE_WIDTH)
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

class HabitBoardHeader(ctk.CTkFrame):

    def __init__(self, 
                 master,
                 style_settings, 
                 show_yesterday_panel,
                 show_today_panel):
        super().__init__(master,
                         corner_radius=df.CORNER_RADIUS,
                         fg_color=style_settings["colors"]["frame"])

        self.fonts = style_settings["fonts"]
        self.theme_colors = style_settings["colors"]
        self.show_yesterday_panel = show_yesterday_panel
        self.show_today_panel = show_today_panel
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

        self._draw_buttons()



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


    def _draw_buttons(self): 

        button_frame = ctk.CTkFrame(
            self,
            width=COLUMN_HABIT_TABLE_WIDTH,
            fg_color= self.theme_colors["frame"]
        )

        button_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY
        )

        self.go_today_button = ctk.CTkButton(
            button_frame, 
            text="🏠", 
            command=self.show_today_panel, 
            font=self.fonts["SMALL"], )
        
        self.go_today_button.pack(
            side ="left", 
            padx=df.PADX, 
            ) 
        
        self.go_yesterday_button = ctk.CTkButton(
            button_frame, 
            text="¿Olvidaste marcar ayer?", 
            command=self.show_yesterday_panel, 
            font=self.fonts["SMALL"], 
            ) 
        self.go_yesterday_button.pack( 
            side ="left", 
            padx=df.PADX, 
            )