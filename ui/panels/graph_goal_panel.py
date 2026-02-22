import customtkinter as ctk

import infrastructure.config.defaults as df
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

class GraphGoalPanel(ctk.CTkFrame):

    TITLE = "— Objetivos Completados este año —"
    state_key = "panels.graph_goals"

    TABLE_HEADERS = ("Objetivo", "Periodo", "Completado")

    events = {"goal_changed", "graph_changed", "day_changed"}

    def __init__(self, master, style_settings):
        super().__init__(master, corner_radius=df.CORNER_RADIUS)

        self.fonts = style_settings["fonts"]
        self.theme_colors = style_settings["colors"]

        self._build_static()

    # =====================================================
    # STATIC UI
    # =====================================================

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

    # =====================================================
    # ENTRY POINT
    # =====================================================

    def refresh(self, panel_state):

        if not panel_state:
            return

        self.rate_label.configure(
            text=panel_state.get("rate", "")
        )

        goals = panel_state.get("goals_per_year", [])

        self._render_table(goals)

    # =====================================================
    # TABLE RENDER
    # =====================================================

    def _render_table(self, goals):

        # Limpiar tabla anterior
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if not goals:
            ctk.CTkLabel(
                self.content_frame,
                text="No hay objetivos en este año.",
                font=self.fonts["SMALL"],
            ).pack(pady=10)
            return

        table_frame = ctk.CTkFrame(
            self.content_frame,
            corner_radius=df.CORNER_RADIUS
        )
        table_frame.pack(fill="both", expand=True)

        # ========================
        # HEADERS
        # ========================
        for col, header in enumerate(self.TABLE_HEADERS):
            ctk.CTkLabel(
                table_frame,
                text=header,
                font=self.fonts["SMALL"],
            ).grid(row=0, column=col, sticky="nsew", pady=2)

            table_frame.grid_columnconfigure(col, weight=1)

        # ========================
        # ROWS
        # ========================
        for row_index, goal in enumerate(goals, start=1):

            values = (
                goal["goal_name"],
                goal.get("period_quarter", ""),
                "✓" if goal.get("is_completed") else ""
            )

            for col, value in enumerate(values):

                ctk.CTkLabel(
                    table_frame,
                    text=str(value),
                    font=self.fonts["SMALL"],
                    fg_color=self.theme_colors["top_frame"]
                ).grid(
                    row=row_index,
                    column=col,
                    sticky="nsew",
                    pady=2,
                    padx=2
                )