import customtkinter as ctk
from infrastructure.config import defaults as df
from utils.tooltip import Tooltip
from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)


class CheckPanelBase(ctk.CTkFrame):
    def __init__(
        self,
        master,
        fonts,
        theme_colors,
        date,
        habits,
        completed_habits,
        on_check,
        title,
        subtitle=None,
    ):
        super().__init__(master, corner_radius=df.CORNER_RADIUS)

        self.fonts = fonts
        self.theme_colors = theme_colors
        self.date = date
        self.habits = habits
        self.completed_habits = completed_habits
        self.on_check = on_check
        self.title = title
        self.subtitle = subtitle

        self.build()

    def build(self):
        self.scroll = ctk.CTkScrollableFrame(
            self,
            corner_radius=df.CORNER_RADIUS,
            fg_color=self.theme_colors["frame"],
        )
        self.scroll.pack(fill="both", expand=True, padx=df.PADX, pady=df.PADY)

        self.draw_titles()
        self.draw_buttons()

    def draw_titles(self):
        ctk.CTkLabel(
            self.scroll,
            text=self.title,
            font=self.fonts["SMALL"],
            text_color=df.COLOR_BORDE,
        ).pack(pady=5)

        if self.subtitle:
            ctk.CTkLabel(
                self.scroll,
                text=self.subtitle,
                font=self.fonts["SMALL"],
                text_color=df.COLOR_AUTOR,
            ).pack(pady=2)

    def draw_buttons(self):
        if not self.habits:
            ctk.CTkLabel(
                self.scroll,
                text="No hay hábitos registrados.",
                font=self.fonts["SMALL"],
                text_color=df.COLOR_BORDE,
            ).pack(pady=5)
            return

        for habit in self.habits:
            name = habit["nombre_habito"]
            btn = ctk.CTkButton(
                self.scroll,
                text=name,
                fg_color=habit["color"],
                text_color=df.COLOR_BORDE,
                font=self.fonts["SMALL"],
                command=lambda h=name: self.on_check(h),
            )
            btn.pack(fill="x", pady=1, padx=2)

            if name in self.completed_habits:
                btn.configure(text=f"{name} - Completado!", state="disabled")
