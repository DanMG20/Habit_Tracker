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
        get_habits,
        get_completed_habits,
        title,
        on_check=None,
        on_delete=None,
        subtitle=None,
    ):
        super().__init__(master, corner_radius=df.CORNER_RADIUS)

        self.fonts = fonts
        self.theme_colors = theme_colors
        self.date = date
        self.get_habits = get_habits
        self.get_completed_habits = get_completed_habits
        self.on_check = on_check
        self.title = title
        self.subtitle = subtitle
        self.on_delete = on_delete

        self.build()

    def refresh(self):
        self.clean_widgets()
        self.draw_titles()
        self.draw_buttons()

    def clean_widgets(self):
        for widget in self.scroll.winfo_children():
            widget.destroy()

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
        habits = self.get_habits()
        completed_habits = self.get_completed_habits()
        if not habits:
            ctk.CTkLabel(
                self.scroll,
                text="No hay hábitos registrados.",
                font=self.fonts["SMALL"],
                text_color=df.COLOR_BORDE,
            ).pack(pady=5)
            return
        if self.on_check:
            command = self.on_check
        else:
            command = self.on_delete
        for habit in habits:
            name = habit["habit_name"]
            id = habit["id"]
            btn = ctk.CTkButton(
                self.scroll,
                text=name,
                fg_color=habit["habit_color"],
                text_color=df.COLOR_BORDE,
                font=self.fonts["SMALL"],
                command=lambda id=id: command(id),
            )
            btn.pack(fill="x", pady=1, padx=2)

            if id in completed_habits:
                btn.configure(text=f"{name} - Completado!", state="disabled")
