import customtkinter as ctk
from infrastructure.config import defaults as df
from datetime import timedelta



class HabitBoardTable(ctk.CTkScrollableFrame):

    def __init__(self, master, style_settings):
        super().__init__(
            master=master,
            corner_radius=df.CORNER_RADIUS,
            fg_color=style_settings["colors"]["frame"]
        )

        self.fonts = style_settings["fonts"]
        self.theme_colors = style_settings["colors"]

        self.labels_estado_habitos = {}
        self.labels_nombres_habitos = {}

        self._configure_grid()

    # =========================================================
    # ENTRY POINT
    # =========================================================

    def refresh(self, habit_board_state):

        habits = habit_board_state["habits"]
        week_start = habit_board_state["week_start"]
        executions = habit_board_state["executions"]
        today = habit_board_state["today"]
        execution_index = self._index_executions(executions)

        if not habits:
            self._render_empty_state()
            return

        self._remove_empty_state()
        self._sync_removed_habits(habits)
        self._render_habits(habits, week_start, execution_index, today)

    # =========================================================
    # INDEXING (OPTIMIZATION)
    # =========================================================

    def _index_executions(self, executions):
        """
        Convierte lista en dict:
        {(habit_id, date): execution}
        O(1) lookup
        """
        return {
            (e["habit_id"], e["execution_date"]): e
            for e in executions
        }

    # =========================================================
    # EMPTY STATE
    # =========================================================

    def _render_empty_state(self):

        self._clear_all_labels()

        if not hasattr(self, "label_mensaje_sin_habitos"):
            self.label_mensaje_sin_habitos = ctk.CTkLabel(
                self,
                text="Crea un nuevo hábito para comenzar! 😏",
                font=self.fonts["SMALL"],
            )
            self.label_mensaje_sin_habitos.pack(side="top")

    def _remove_empty_state(self):
        if hasattr(self, "label_mensaje_sin_habitos"):
            self.label_mensaje_sin_habitos.destroy()
            del self.label_mensaje_sin_habitos

    # =========================================================
    # CLEANUP
    # =========================================================

    def _clear_all_labels(self):
        for label in self.labels_nombres_habitos.values():
            label.destroy()
        for label in self.labels_estado_habitos.values():
            label.destroy()

        self.labels_nombres_habitos.clear()
        self.labels_estado_habitos.clear()

    def _sync_removed_habits(self, habits):

        current_ids = {h["id"] for h in habits}

        # Remove deleted names
        for habit_id in list(self.labels_nombres_habitos.keys()):
            if habit_id not in current_ids:
                self.labels_nombres_habitos[habit_id].destroy()
                del self.labels_nombres_habitos[habit_id]

        # Remove deleted cells
        for key in list(self.labels_estado_habitos.keys()):
            habit_id, _ = key
            if habit_id not in current_ids:
                self.labels_estado_habitos[key].destroy()
                del self.labels_estado_habitos[key]

    # =========================================================
    # RENDERING
    # =========================================================

    def _render_habits(self, habits, week_start, execution_index, today):

        for row_index, habit in enumerate(habits):

            habit_id = habit["id"]
            creation_date = habit["creation_date"]

            self._render_habit_name(habit, row_index)

            for day_index in range(7):

                date = week_start + timedelta(days=day_index)

                text, color = self._resolve_cell_state(
                    habit,
                    habit_id,
                    creation_date,
                    date,
                    day_index,
                    execution_index,
                    today
                )

                self._render_cell(
                    habit_id,
                    row_index,
                    day_index,
                    text,
                    color
                )

    def _render_habit_name(self, habit, row_index):

        habit_id = habit["id"]

        if habit_id not in self.labels_nombres_habitos:
            label = ctk.CTkLabel(
                self,
                text=habit["habit_name"],
                font=self.fonts["SMALL"],
                fg_color=self.theme_colors["top_frame"],
                width=df.COLUMN_HABIT_TABLE_WIDTH,
            )
            self.labels_nombres_habitos[habit_id] = label

        self.labels_nombres_habitos[habit_id].grid(
            column=0,
            row=row_index + 1,
            padx=2,
            pady=1,
            sticky="nsew"
        )

    # =========================================================
    # CELL LOGIC (SEPARATED CLEANLY)
    # =========================================================

    def _resolve_cell_state(
        self,
        habit,
        habit_id,
        creation_date,
        date,
        day_index,
        execution_index,
        today
    ):

        execution = execution_index.get((habit_id, date))
        is_execution_day = habit["execution_days"][day_index]

        if date == creation_date:
            return self._resolve_creation_day(
                execution,
                date,
                today,
                is_execution_day
            )

        if date < creation_date:
            return "➖", self.theme_colors["text"]

        if not is_execution_day:
            return "➖", self.theme_colors["text"]

        return self._resolve_normal_day(execution, date, today)

    def _resolve_creation_day(self, execution, date, today, is_execution_day):


        if not is_execution_day:
            return "⭐", "white"


        if execution:
            return "⭐", "green" if execution["executed"] else "red"


        if date < today:
            return "⭐", "red"

 
        return "⭐", "white"

    def _resolve_normal_day(self, execution, date, today):

        if execution:
            return ("✔", "green") if execution["executed"] else ("✖", "red")

        if date >= today:
            return "", df.COLOR_GUION 

        return "✖", "red"

    # =========================================================
    # CELL RENDER
    # =========================================================

    def _render_cell(self, habit_id, row_index, day_index, text, color):

        key = (habit_id, day_index)

        if key not in self.labels_estado_habitos:
            label = ctk.CTkLabel(
                self,
                font=self.fonts["SMALL"],
                fg_color=self.theme_colors["top_frame"],
            )
            self.labels_estado_habitos[key] = label

        label = self.labels_estado_habitos[key]

        label.configure(text=text, text_color=color)

        label.grid(
            column=day_index + 1,
            row=row_index + 1,
            padx=2,
            pady=1,
            sticky="nsew"
        )

    # =========================================================
    # GRID CONFIG
    # =========================================================

    def _configure_grid(self):
        for column in range(1, 8):
            self.columnconfigure(column, weight=1, uniform="col")
