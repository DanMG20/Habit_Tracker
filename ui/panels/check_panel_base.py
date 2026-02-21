import customtkinter as ctk
from infrastructure.config import defaults as df
from collections import defaultdict

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
        self.content_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.content_frame.pack(fill="both", expand=True)

        

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
        date = panel_state.get("date", None)
        if not habits:
            self._render_empty()
            return

        self._remove_empty()
        self._sync_removed_buttons(habits, date)
        self._render_buttons(habits, completed_ids, date)
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
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.buttons.clear()


    def _sync_removed_buttons(self, habits, panel_date=None):
        """Elimina botones que ya no están presentes en los datos"""
        current_ids = set(self.buttons.keys())
        incoming_ids = {h["id"] for h in habits if not panel_date or h.get("creation_date", panel_date) <= panel_date}

        for old_id in current_ids - incoming_ids:
            self.buttons[old_id].destroy()
            del self.buttons[old_id]


    def _render_buttons(self, habits, completed_ids, panel_date = None):

        command = self.on_check if self.on_check else self.on_delete

        grouped = defaultdict(list)
        for habit in habits:
            creation_date = habit.get("creation_date", panel_date)
            if panel_date and creation_date > panel_date:
                continue
            grouped[habit["category"]].append(habit)

        for category, category_habits in grouped.items():
            # Crear etiqueta de categoría solo si no existe
            cat_label_name = f"cat_label_{category}"
            if not hasattr(self, cat_label_name):
                category_label = ctk.CTkLabel(
                    self.content_frame,
                    text=f"— {category} —",
                    font=self.fonts["SMALL"],
                    text_color=df.COLOR_AUTOR,
                )
                category_label.pack(fill="x", pady=(10, 2), padx=5)
                setattr(self, cat_label_name, category_label)

            # Crear o actualizar botones
            for habit in category_habits:
                habit_id = habit["id"]
                name = habit["habit_name"]
                color = habit["habit_color"]
                is_completed = habit_id in completed_ids

                if habit_id in self.buttons:
                    # Solo actualizar si cambió algo
                    btn = self.buttons[habit_id]
                    new_text = f"{name} - Completado!" if is_completed else name
                    new_state = "disabled" if is_completed else "normal"
                    if btn.cget("text") != new_text or btn.cget("state") != new_state:
                        btn.configure(text=new_text, state=new_state, fg_color=color)
                else:
                    # Crear nuevo botón
                    btn = ctk.CTkButton(
                        self.content_frame,
                        text=f"{name} - Completado!" if is_completed else name,
                        fg_color=color,
                        font=self.fonts["SMALL"],
                        command=lambda id=habit_id: command(id),
                        state="disabled" if is_completed else "normal",
                    )
                    btn.pack(fill="x", pady=1, padx=df.PADX)
                    self.buttons[habit_id] = btn