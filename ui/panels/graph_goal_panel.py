import customtkinter as ctk

import infrastructure.config.defaults as df
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

class GraphGoalPanel(ctk.CTkFrame):

    TITLE = "— Objetivos Completados este año —"

    state_key  ="panels.graph_goals"


    events = {"goal_changed","graph_changed", "day_changed"}

    def __init__(self, master, style_settings):
        super().__init__(master, corner_radius=df.CORNER_RADIUS)

        self.fonts = style_settings["fonts"]

        self.labels = {}

        self._build_static()

    def _build_static(self):



        self.title_label = ctk.CTkLabel(
            self,
            text=self.TITLE,
            font=self.fonts["SMALL"],
        )
        self.title_label.pack(pady=5)

        self.rate_label = ctk.CTkLabel(
            self,
            text="",
            font=self.fonts["SUBTITLE"],
        )
        self.rate_label.pack(pady=5)

        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)


    def refresh(self, panel_state):

        if not panel_state:
            return

        self.rate_label.configure(
            text=panel_state.get('rate', '')
        )

        goals = panel_state.get("goals_per_year", [])

        self._clear_labels()

        if not goals:
            self._render_empty()
            return

        for goal in goals:
            name = goal["goal_name"]

            label = ctk.CTkLabel(
                self.content_frame,
                text=name,
                font=self.fonts["SUBTITLE"],
            )
            label.pack(fill="x", pady=1, padx=2)

            if goal["is_completed"]:
                label.configure(
                    text=f"{name} - ✓"
                )
            self.labels[id] = label

    def _clear_labels(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def _render_empty(self):
        ctk.CTkLabel(
            self.content_frame,
            text="No hay objetivos en este año.",
            font=self.fonts["SMALL"],
        ).pack(pady=5)
