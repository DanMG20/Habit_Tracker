import customtkinter as ctk
from infrastructure.config import defaults as df
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class CheckPanelBase(ctk.CTkScrollableFrame):

    SUBTITLE =""
    TITLE= ""

    def __init__(
        self,
        master,
        style_settings,
        complete=None,
        on_delete=None,
    ):
        super().__init__(
            master,
            corner_radius=df.CORNER_RADIUS,
            fg_color=style_settings["colors"]["frame"]
        )

        self.fonts = style_settings["fonts"]
        self.theme_colors = style_settings["colors"]

        self.on_check = complete
        self.on_delete = on_delete

        self.buttons = {}  # {habit_id: button}

        self._build_static()

    # =========================================================
    # STATIC UI (se construye una vez)
    # =========================================================

    def _build_static(self):
        self._draw_titles()

    def _draw_titles(self):

        self.title_label = ctk.CTkLabel(
            self,
            text=self.TITLE,
            font=self.fonts["SMALL"],
            text_color=df.COLOR_BORDE,
        )
        self.title_label.pack(pady=5)

        if self.SUBTITLE:
            self.subtitle_label = ctk.CTkLabel(
                self,
                text=self.SUBTITLE,
                font=self.fonts["SMALL"],
                text_color=df.COLOR_AUTOR,
            )
            self.subtitle_label.pack(pady=2)

    # =========================================================
    # ENTRY POINT
    # =========================================================

    def refresh(self, panel_state):
        if not panel_state:
            self._render_empty()
            return

        habits = panel_state.get("habits", [])
        completed_ids = set(panel_state.get("completed", []))

        if not habits:
            self._render_empty()
            return

        self._remove_empty()
        self._sync_removed_buttons(habits)
        self._render_buttons(habits, completed_ids)

    # =========================================================
    # EMPTY STATE
    # =========================================================

    def _render_empty(self):

        self._clear_buttons()

        if not hasattr(self, "empty_label"):
            self.empty_label = ctk.CTkLabel(
                self,
                text="No hay hábitos registrados.",
                font=self.fonts["SMALL"],
                text_color=df.COLOR_BORDE,
            )
            self.empty_label.pack(pady=5)

    def _remove_empty(self):
        if hasattr(self, "empty_label"):
            self.empty_label.destroy()
            del self.empty_label

    # =========================================================
    # BUTTON MANAGEMENT
    # =========================================================

    def _clear_buttons(self):
        for btn in self.buttons.values():
            btn.destroy()
        self.buttons.clear()

    def _sync_removed_buttons(self, habits):

        current_ids = {h["id"] for h in habits}

        for habit_id in list(self.buttons.keys()):
            if habit_id not in current_ids:
                self.buttons[habit_id].destroy()
                del self.buttons[habit_id]

    def _render_buttons(self, habits, completed_ids):

        command = self.on_check if self.on_check else self.on_delete

        for habit in habits:

            habit_id = habit["id"]
            name = habit["habit_name"]
            color = habit["habit_color"]

            if habit_id not in self.buttons:
                btn = ctk.CTkButton(
                    self,
                    text=name,
                    fg_color=color,
                    text_color=df.COLOR_BORDE,
                    font=self.fonts["SMALL"],
                    command=lambda id=habit_id: command(id),
                )
                btn.pack(fill="x", pady=1, padx=2)

                self.buttons[habit_id] = btn

            btn = self.buttons[habit_id]

            if habit_id in completed_ids:
                btn.configure(
                    text=f"{name} - Completado!",
                    state="disabled"
                )
            else:
                btn.configure(
                    text=name,
                    state="normal"
                )
