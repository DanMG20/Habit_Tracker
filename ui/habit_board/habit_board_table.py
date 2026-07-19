import customtkinter as ctk
from datetime import timedelta, date
from typing import Dict, Any, List, Optional, Tuple

# Assuming this module is part of your infrastructure
from infrastructure.config import defaults as df


class BoardConstants:
    """Constants to avoid magic strings and numbers in the board rendering."""
    SYMBOL_CREATION: str = "⭐"
    SYMBOL_INACTIVE: str = "➖"
    SYMBOL_DONE: str = "✔"
    SYMBOL_FAILED: str = "✖"
    SYMBOL_EMPTY: str = ""
    
    COLOR_WHITE: str = "white"
    COLOR_GREEN: str = "green"
    COLOR_RED: str = "red"
    COLOR_TRANSPARENT: str = "transparent"
    
    DAYS_IN_WEEK: int = 7


class HabitBoardTable(ctk.CTkScrollableFrame):
    """
    Renders the habit tracking board.
    It manages the visual representation of habits across a specified week.
    """

    def __init__(self, master: Any, style_settings: Dict[str, Any]) -> None:
        """
        Initializes the HabitBoardTable component.

        Args:
            master: The parent tkinter/customtkinter widget.
            style_settings: Dictionary containing 'fonts' and 'colors' configurations.
        """
        super().__init__(
            master=master,
            corner_radius=df.CORNER_RADIUS,
            fg_color=style_settings["colors"]["frame"]
        )

        self.fonts: Dict[str, Any] = style_settings["fonts"]
        self.theme_colors: Dict[str, str] = style_settings["colors"]

        self.labels_habit_states: Dict[Tuple[int, int], ctk.CTkLabel] = {}
        self.labels_habit_names: Dict[int, ctk.CTkLabel] = {}

        self._configure_grid()

    # =========================================================
    # ENTRY POINT
    # =========================================================

    def refresh(self, habit_board_state: Dict[str, Any]) -> None:
        """
        Refreshes the board UI with the current state.

        Args:
            habit_board_state: Dictionary containing habits, week_start, executions, and today's date.
        """
        habits: List[Dict[str, Any]] = habit_board_state.get("habits", [])
        week_start: date = habit_board_state["week_start"]
        executions: List[Dict[str, Any]] = habit_board_state.get("executions", [])
        today: date = habit_board_state["today"]
        
        execution_index: Dict[Tuple[int, date], Dict[str, Any]] = self._index_executions(executions)

        if not habits:
            self._render_empty_state()
            return

        self._remove_empty_state()
        self._sync_removed_habits(habits)
        self._render_habits(habits, week_start, execution_index, today)

    # =========================================================
    # INDEXING & BUSINESS RULES (OPTIMIZATION)
    # =========================================================

    def _index_executions(self, executions: List[Dict[str, Any]]) -> Dict[Tuple[int, date], Dict[str, Any]]:
        """
        Converts the executions list into a dictionary for O(1) lookup.

        Args:
            executions: List of execution records.

        Returns:
            A dictionary mapping (habit_id, execution_date) to the execution record.
        """
        return {
            (e["habit_id"], e["execution_date"]): e
            for e in executions
        }

    def _get_config_for_date(self, habit: Dict[str, Any], target_date: date) -> Optional[Dict[str, Any]]:
        """
        Finds the valid configuration for a specific habit on a given date.

        Args:
            habit: The habit dictionary containing the 'configs' array.
            target_date: The date to evaluate against the configuration lifespan.

        Returns:
            The valid configuration dictionary if found and active, None otherwise.
        """
        configs: List[Dict[str, Any]] = habit.get("configs", [])
        
        for config in configs:
            is_active: bool = bool(config.get("is_active", 0))
            valid_from: Optional[date] = config.get("valid_from")
            valid_until: Optional[date] = config.get("valid_until")

            if not is_active or not valid_from:
                continue

            if valid_from <= target_date:
                if valid_until is None or target_date <= valid_until:
                    return config
                    
        return None

    # =========================================================
    # EMPTY STATE
    # =========================================================

    def _render_empty_state(self) -> None:
        """Renders a message when there are no habits to display."""
        self._clear_all_labels()

        if not hasattr(self, "label_empty_state_message"):
            self.label_empty_state_message = ctk.CTkLabel(
                self,
                text="¡Crea un nuevo hábito para comenzar! 😏",
                font=self.fonts["SMALL"],
            )
            self.label_empty_state_message.pack(side="top")

    def _remove_empty_state(self) -> None:
        """Removes the empty state message from the UI."""
        if hasattr(self, "label_empty_state_message"):
            self.label_empty_state_message.destroy()
            del self.label_empty_state_message

    # =========================================================
    # CLEANUP
    # =========================================================

    def _clear_all_labels(self) -> None:
        """Destroys all active labels in the grid to free up memory."""
        for label in self.labels_habit_names.values():
            label.destroy()
        for label in self.labels_habit_states.values():
            label.destroy()

        self.labels_habit_names.clear()
        self.labels_habit_states.clear()

    def _sync_removed_habits(self, habits: List[Dict[str, Any]]) -> None:
        """
        Removes labels of habits that are no longer present in the state.

        Args:
            habits: The current list of active habits.
        """
        current_ids = {h["id"] for h in habits}

        for habit_id in list(self.labels_habit_names.keys()):
            if habit_id not in current_ids:
                self.labels_habit_names[habit_id].destroy()
                del self.labels_habit_names[habit_id]

        for key in list(self.labels_habit_states.keys()):
            habit_id, _ = key
            if habit_id not in current_ids:
                self.labels_habit_states[key].destroy()
                del self.labels_habit_states[key]

    # =========================================================
    # RENDERING
    # =========================================================

    def _render_habits(
        self, 
        habits: List[Dict[str, Any]], 
        week_start: date, 
        execution_index: Dict[Tuple[int, date], Dict[str, Any]], 
        today: date
    ) -> None:
        """
        Iterates over habits and days to render the entire grid.

        Args:
            habits: List of habits.
            week_start: Starting date of the week being viewed.
            execution_index: Indexed executions for O(1) lookup.
            today: The current real-world date.
        """
        for row_index, habit in enumerate(habits):
            habit_id: int = habit["id"]
            creation_date: date = habit["creation_date"]

            self._render_habit_name(habit, row_index)

            for day_index in range(BoardConstants.DAYS_IN_WEEK):
                current_date: date = week_start + timedelta(days=day_index)

                text, color, bg_color = self._resolve_cell_state(
                    habit=habit,
                    habit_id=habit_id,
                    creation_date=creation_date,
                    current_date=current_date,
                    day_index=day_index,
                    execution_index=execution_index,
                    today=today
                )

                self._render_cell(
                    habit_id=habit_id,
                    row_index=row_index,
                    day_index=day_index,
                    text=text,
                    color=color,
                    bg_color=bg_color
                )

    def _render_habit_name(self, habit: Dict[str, Any], row_index: int) -> None:
        """
        Renders the title column for a given habit.

        Args:
            habit: Habit data dictionary.
            row_index: Vertical position in the grid.
        """
        habit_id: int = habit["id"]

        if habit_id not in self.labels_habit_names:
            label = ctk.CTkLabel(
                self,
                text=habit["habit_name"],
                font=self.fonts["SMALL"],
                fg_color=self.theme_colors["top_frame"],
                width=df.COLUMN_HABIT_TABLE_WIDTH,
            )
            self.labels_habit_names[habit_id] = label

        self.labels_habit_names[habit_id].grid(
            column=0,
            row=row_index + 1,
            padx=2,
            pady=1,
            sticky="nsew"
        )

    # =========================================================
    # CELL LOGIC
    # =========================================================

    def _resolve_cell_state(
        self,
        habit: Dict[str, Any],
        habit_id: int,
        creation_date: date,
        current_date: date,
        day_index: int,
        execution_index: Dict[Tuple[int, date], Dict[str, Any]],
        today: date
    ) -> Tuple[str, str, str]:
        """
        Determines the display text and color for a specific grid cell based on temporal rules.

        Args:
            habit: The habit data.
            habit_id: The ID of the habit.
            creation_date: Date the habit was originally created.
            current_date: Date represented by the current cell.
            day_index: 0-6 representing Sunday-Saturday.
            execution_index: Execution lookups.
            today: The real-world today date.

        Returns:
            A tuple of (Text/Symbol to display, Hex color or color name).
        """
        execution = execution_index.get((habit_id, current_date))
        
        # 1. Evaluate configuration for the current date
        active_config = self._get_config_for_date(habit, current_date)
        
        # If there's no active configuration for this date, it's inactive
        if not active_config:
            return BoardConstants.SYMBOL_EMPTY, self.theme_colors["text"], BoardConstants.COLOR_TRANSPARENT
        bg_color = self.theme_colors["top_frame"]
        is_execution_day: bool = bool(active_config["execution_days"][day_index])

        if current_date == creation_date:
                    text, color = self._resolve_creation_day(
                        execution=execution,
                        current_date=current_date,
                        today=today,
                        is_execution_day=is_execution_day
                    )
                    return text, color, bg_color

        if current_date < creation_date or not is_execution_day:
            return BoardConstants.SYMBOL_INACTIVE, self.theme_colors["text"], bg_color

        text, color = self._resolve_normal_day(execution, current_date, today)
        return text, color, bg_color

    def _resolve_creation_day(
        self, 
        execution: Optional[Dict[str, Any]], 
        current_date: date, 
        today: date, 
        is_execution_day: bool
    ) -> Tuple[str, str]:
        """Resolves logic specifically for the day the habit was created."""
        if not is_execution_day:
            return BoardConstants.SYMBOL_CREATION, BoardConstants.COLOR_WHITE

        if execution:
            color = BoardConstants.COLOR_GREEN if execution.get("executed") else BoardConstants.COLOR_RED
            return BoardConstants.SYMBOL_CREATION, color

        if current_date < today:
            return BoardConstants.SYMBOL_CREATION, BoardConstants.COLOR_RED

        return BoardConstants.SYMBOL_CREATION, BoardConstants.COLOR_WHITE

    def _resolve_normal_day(
        self, 
        execution: Optional[Dict[str, Any]], 
        current_date: date, 
        today: date
    ) -> Tuple[str, str]:
        """Resolves logic for any standard configured execution day."""
        if execution:
            if execution.get("executed"):
                return BoardConstants.SYMBOL_DONE, BoardConstants.COLOR_GREEN
            return BoardConstants.SYMBOL_FAILED, BoardConstants.COLOR_RED

        if current_date >= today:
            return BoardConstants.SYMBOL_EMPTY, df.COLOR_DASH_DIVIDER 

        return BoardConstants.SYMBOL_FAILED, BoardConstants.COLOR_RED

    # =========================================================
    # CELL RENDER
    # =========================================================

# =========================================================
    # RENDERING
    # =========================================================

    def _render_habits(
        self, 
        habits: List[Dict[str, Any]], 
        week_start: date, 
        execution_index: Dict[Tuple[int, date], Dict[str, Any]], 
        today: date
    ) -> None:
        """
        Iterates over habits and days to render the entire grid.
        """
        for row_index, habit in enumerate(habits):
            habit_id: int = habit["id"]
            creation_date: date = habit["creation_date"]

            self._render_habit_name(habit, row_index)

            for day_index in range(BoardConstants.DAYS_IN_WEEK):
                current_date: date = week_start + timedelta(days=day_index)

                # AHORA RECIBIMOS 3 VALORES: text, text_color, bg_color
                text, text_color, bg_color = self._resolve_cell_state(
                    habit=habit,
                    habit_id=habit_id,
                    creation_date=creation_date,
                    current_date=current_date,
                    day_index=day_index,
                    execution_index=execution_index,
                    today=today
                )

                self._render_cell(
                    habit_id=habit_id,
                    row_index=row_index,
                    day_index=day_index,
                    text=text,
                    text_color=text_color,
                    bg_color=bg_color  # PASAMOS EL FONDO A LA CELDA
                )

    # ... (deja tu _render_habit_name como estaba) ...

    # =========================================================
    # CELL LOGIC
    # =========================================================

    def _resolve_cell_state(
        self,
        habit: Dict[str, Any],
        habit_id: int,
        creation_date: date,
        current_date: date,
        day_index: int,
        execution_index: Dict[Tuple[int, date], Dict[str, Any]],
        today: date
    ) -> Tuple[str, str, str]:  # <-- NOTA QUE AHORA DEVOLVEMOS 3 STRINGS
        """
        Determines the display text, text color, and background color for a specific grid cell.
        """
        execution = execution_index.get((habit_id, current_date))
        
        # 1. Evaluate configuration for the current date
        active_config = self._get_config_for_date(habit, current_date)
        
        # SI EL HÁBITO ESTÁ INACTIVO EN ESTA FECHA: Sin texto y fondo transparente
        if not active_config:
            return BoardConstants.SYMBOL_EMPTY, self.theme_colors["text"], BoardConstants.COLOR_TRANSPARENT

        # SI ESTÁ ACTIVO: Definimos su fondo normal
        bg_color = self.theme_colors["top_frame"]
        is_execution_day: bool = bool(active_config["execution_days"][day_index])

        if current_date == creation_date:
            text, color = self._resolve_creation_day(
                execution=execution,
                current_date=current_date,
                today=today,
                is_execution_day=is_execution_day
            )
            return text, color, bg_color

        if current_date < creation_date or not is_execution_day:
            return BoardConstants.SYMBOL_INACTIVE, self.theme_colors["text"], bg_color

        text, color = self._resolve_normal_day(execution, current_date, today)
        return text, color, bg_color

    # ... (deja tus helpers _resolve_creation_day y _resolve_normal_day como estaban) ...

    # =========================================================
    # CELL RENDER
    # =========================================================

    def _render_cell(self, habit_id: int, row_index: int, day_index: int, text: str, text_color: str, bg_color: str) -> None:
        """Draws the individual cell in the grid."""
        key: Tuple[int, int] = (habit_id, day_index)

        if key not in self.labels_habit_states:
            label = ctk.CTkLabel(
                self,
                font=self.fonts["SMALL"],
            )
            self.labels_habit_states[key] = label

        label = self.labels_habit_states[key]

        label.configure(text=text, text_color=text_color, fg_color=bg_color)

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

    def _configure_grid(self) -> None:
        """Configures the Tkinter grid column weights."""
        for column in range(1, 8):
            self.columnconfigure(column, weight=1, uniform="col")