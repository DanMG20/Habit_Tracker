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
        )
        self.title_label.pack(pady=5)

        self.period_label = ctk.CTkLabel(
            self,
            text="",
            font=self.fonts["SMALL"],
            text_color= df.COLOR_AUTOR
        )
        self.period_label.pack(pady=5)


    def refresh(self, panel_state):
        if not panel_state:
            return

        self.period_label.configure(
            text=f"Perido de la semana {panel_state.get('current_period', '')}"
        )

        goals = panel_state.get("goals", [])

        if not goals:
            # Si antes había botones, los dejamos visibles o borramos solo si quieres
            self._clear_buttons()
            self._render_empty()
            return

        current_goal_ids = set(self.buttons.keys())
        incoming_goal_ids = set(goal["id"] for goal in goals)

        # 1️⃣ Actualizar botones existentes y deshabilitar/completar si cambió
        for goal in goals:
            goal_id = goal["id"]
            name = goal["goal_name"]
            is_completed = goal["is_completed"]

            if goal_id in self.buttons:
                btn = self.buttons[goal_id]
                # Solo actualizar si cambió algo
                new_text = f"{name} - Completado!" if is_completed else name
                if btn.cget("text") != new_text or btn.cget("state") != ("disabled" if is_completed else "normal"):
                    btn.configure(
                        text=new_text,
                        state="disabled" if is_completed else "normal"
                    )
            else:
                # 2️⃣ Crear botones nuevos que no existían
                btn = ctk.CTkButton(
                    self,
                    text=name,
                    font=self.fonts["SMALL"],
                    command=lambda id=goal_id: self.complete(id),
                )
                btn.pack(fill="x", pady=1, padx=df.PADX)

                if is_completed:
                    btn.configure(
                        text=f"{name} - Completado!",
                        state="disabled"
                    )
                self.buttons[goal_id] = btn

        # 3️⃣ Borrar botones que ya no existen en la lista
        for old_id in current_goal_ids - incoming_goal_ids:
            self.buttons[old_id].destroy()
            del self.buttons[old_id]


    def _clear_buttons(self):
        for btn in self.buttons.values():
            btn.destroy()
        self.buttons.clear()

    def _render_empty(self):
        ctk.CTkLabel(
            self,
            text="No hay objetivos registrados.",
            font=self.fonts["SMALL"],
        ).pack(pady=5)
