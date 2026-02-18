import customtkinter as ctk

import infrastructure.config.defaults as df
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

class GoalPanel(ctk.CTkScrollableFrame):

    TITLE = "— Objetivos Trimestrales —"

    state_key  ="panels.goals"


    events = {"goal_changed", "day_changed"}

    def __init__(self, master, style_settings, complete_goal):
        super().__init__(master, corner_radius=df.CORNER_RADIUS)

        self.fonts = style_settings["fonts"]
        self.complete = complete_goal

        self.buttons = {}

        self._build_static()

    def _build_static(self):
        self.title_label = ctk.CTkLabel(
            self,
            text=self.TITLE,
            font=self.fonts["SMALL"],
            text_color=df.COLOR_BORDE,
        )
        self.title_label.pack(pady=5)

        self.period_label = ctk.CTkLabel(
            self,
            text="",
            font=self.fonts["SMALL"],
            text_color=df.COLOR_BORDE,
        )
        self.period_label.pack(pady=5)


    def refresh(self, panel_state):

        if not panel_state:
            return

        self.period_label.configure(
            text=f"Semana {panel_state.get('current_period', '')}"
        )

        goals = panel_state.get("goals", [])

        self._clear_buttons()

        if not goals:
            self._render_empty()
            return

        for goal in goals:
            goal_id = goal["id"]
            name = goal["goal_name"]

            btn = ctk.CTkButton(
                self,
                text=name,
                font=self.fonts["SUBTITLE"],
                command=lambda id=goal_id: self.complete(id),
            )
            btn.pack(fill="x", pady=1, padx=2)

            if goal["is_completed"]:
                btn.configure(
                    text=f"{name} - Completado!",
                    state="disabled"
                )

            self.buttons[goal_id] = btn


    def _clear_buttons(self):
        for btn in self.buttons.values():
            btn.destroy()
        self.buttons.clear()

    def _render_empty(self):
        ctk.CTkLabel(
            self,
            text="No hay objetivos registrados.",
            font=self.fonts["SMALL"],
            text_color=df.COLOR_BORDE,
        ).pack(pady=5)
