import customtkinter as ctk
from typing import Dict, Any, List, Callable, Optional
import infrastructure.config.defaults as df
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class HabitFormView:
    """
    View responsible for rendering and managing the Habit creation and edition form.
    """

    DEFAULT_NAME_PLACEHOLDER: str = "Levantarse temprano, Regar las plantas, etc..."
    DEFAULT_CATEGORY_PLACEHOLDER: str = "Tareas, Estudio, Cuidado personal, Proyectos..."
    DEFAULT_DESCRIPTION_PLACEHOLDER: str = "Levantarse a las 7 am, Caminar 15 min, etc..."

    VIEW_TITLES: Dict[str, str] = {
        "add": "AGREGAR HÁBITO",
        "edit": "EDITAR HÁBITO"
    }

    FILLER_HEIGHT: int = 50

    def __init__(
        self,
        master: Any,
        styles: Dict[str, Any],
        go_to_main_view: Callable[[], None],
        create_habit_callback: Callable[[Dict[str, Any]], None],
        update_habit_callback: Callable[[Dict[str, Any]], None],
        get_categories_callback: Callable[[], List[str]],
    ) -> None:

        self.master = master
        self.fonts: Dict[str, Any] = styles["fonts"]
        self.colors: Dict[str, str] = styles["colors"]

        self.view_mode: str = "add"
        self.go_to_main_view = go_to_main_view
        self.create_habit_callback = create_habit_callback
        self.update_habit_callback = update_habit_callback
        self.get_categories_callback = get_categories_callback

        self.command_map: Dict[str, Callable[[], None]] = {
            "add": self._handle_create_habit,
            "edit": self._handle_update_habit,
        }

        self.loaded_habit_id: Optional[int] = None
        self.select_all_var = ctk.BooleanVar(value=False)
        self.habit_state_var = ctk.BooleanVar(value=True)
        self.selected_icon: Optional[str] = None
        self.selected_color: Optional[str] = None
        self._last_selected_color_button: Optional[ctk.CTkButton] = None 
        self.day_buttons: Dict[int, ctk.CTkButton] = {}
        self.day_button_states: Dict[int, bool] = {}

        self._build_layout()

    # =========================================================
    # PUBLIC API
    # =========================================================

    def set_view_mode(self, mode: str) -> None:
        """Changes the form's mode between creation and edition."""
        if self.view_mode == mode:
            return
        self.view_mode = mode
        self._apply_view_mode()

    def load_habit(self, habit: Dict[str, Any]) -> None:
        """
        Loads an existing habit's data into the form for editing.
        Uses direct key access to enforce the 'Fail Fast' principle 
        on mandatory fields.
        
        Args:
            habit: Dictionary representing the habit data structure.
        """
        self.loaded_habit_id = habit["id"]

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, habit["habit_name"])

        self.category_combobox.set(habit["category"])

        self.description_textbox.delete("1.0", "end")
        self.description_textbox.insert("1.0", habit.get("description", ""))

        self._select_color(habit["habit_color"])

        days_config,state = self._get_latest_execution_days(habit)

        logger.info(f"state { state}")

        for (key, button), days_state in zip(self.day_buttons.items(), days_config):
            self._set_day_button_state(button, key, bool(days_state))

        self._sync_select_all_switch()
        self._sync_habit_state_switch(state)

        self._original_habit_snapshot: Dict[str, Any] = {
            "name": habit["habit_name"],
            "execution_days": days_config,
            "color": habit["habit_color"],
            "category": habit["category"],
            "description": habit.get("description", ""),
            "is_active": state, 
        }

    # =========================================================
    # BUSINESS LOGIC ADAPTERS
    # =========================================================

    def _get_latest_execution_days(self, habit: Dict[str, Any]) -> List[int]:
        """
        Extracts the execution days from the latest configuration.
        The latest configuration is defined as the one without a valid_until date.

        Args:
            habit: Habit dictionary containing the 'configs' list.

        Returns:
            List of integers representing execution days.
            
        Raises:
            ValueError: If no configuration with valid_until=None is found.
        """
        configs: List[Dict[str, Any]] = habit["configs"]
        
        for config in configs:
            if config.get("valid_until") is None:
                return config["execution_days"],config["is_active"]
                
        raise ValueError(f"Data corruption: Habit ID {habit['id']} has no open configuration (valid_until=None).")

    # =========================================================
    # LAYOUT BUILDERS
    # =========================================================

    def _build_layout(self) -> None:
        self._build_header()
        self._build_left_panel()
        self._build_right_panel()

    # ---------------- HEADER ----------------

    def _build_header(self) -> None:
        self.header_frame = ctk.CTkFrame(self.master, corner_radius=df.CORNER_RADIUS)

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=self.VIEW_TITLES["add"],
            font=self.fonts["SUBTITLE"],
            anchor="center",
        )
        self.title_label.pack(fill="both", expand=True, padx=df.PAD_X, pady=df.PAD_Y)

    def _apply_view_mode(self) -> None:
        self.title_label.configure(text=self.VIEW_TITLES[self.view_mode])
        self.save_button.configure(
            text=self.VIEW_TITLES[self.view_mode],
            command=self.command_map[self.view_mode],
        )

    # ---------------- LEFT PANEL ----------------

    def _build_left_panel(self) -> None:
        self.left_panel = ctk.CTkScrollableFrame(self.master)
        self._build_name_section()
        self._build_category_section()
        self._build_category_icon_section()
        self._build_description_section()
        
        self.left_panel.columnconfigure(0, weight=1)
        self.left_panel.rowconfigure(3, weight=1)

    def _build_name_section(self) -> None:
        name_frame = ctk.CTkFrame(self.left_panel, fg_color=self.colors["top_frame"])
        name_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=df.PAD_X,
            pady=df.PAD_Y,
        )

        name_frame.columnconfigure(0, weight=1)
        ctk.CTkLabel(
            name_frame,
            text="INGRESA EL NOMBRE DE TU HÁBITO",
            font=self.fonts["SMALL"],
        ).grid(row=0, column=0, sticky="nsew", padx=2*df.PAD_X, pady=df.LABEL_FORM_PAD_Y)

        self.name_entry = ctk.CTkEntry(name_frame, font=self.fonts["SMALL"])
        self.name_entry.grid(row=1, column=0, sticky="nsew", padx=df.PAD_X, pady=df.PAD_Y)

        self._set_entry_placeholder(self.name_entry, self.DEFAULT_NAME_PLACEHOLDER)

    def _build_category_section(self) -> None:
        categories = self.get_categories_callback() or ["Crea una nueva categoría"]

        category_frame = ctk.CTkFrame(self.left_panel,fg_color=self.colors["top_frame"])
        category_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=df.PAD_X,
            pady=df.PAD_Y,
        )

        category_frame.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            category_frame,
            text="SELECCIONA O CREA UNA CATEGORÍA",
            font=self.fonts["SMALL"],
        ).grid(row=2, column=0, sticky="nsew", padx=2*df.PAD_X, pady=df.LABEL_FORM_PAD_Y)

        self.category_combobox = ctk.CTkComboBox(
            category_frame,
            values=categories,
            font=self.fonts["SMALL"],
        )
        self.category_combobox.grid(row=3, column=0, sticky="ew", padx=df.PAD_X, pady=df.PAD_Y)

    def _build_category_icon_section(self) -> None:
        category_icon_frame = ctk.CTkFrame(self.left_panel, fg_color=self.colors["top_frame"])
        category_icon_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=df.PAD_X,
            pady=df.PAD_Y,
        )

        category_icon_frame.columnconfigure(0, weight=1)
        ctk.CTkLabel(
            category_icon_frame,
            text="ELIGE UN ICONO PARA TU CATEGORIA",
            font=self.fonts["SMALL"],
        ).grid(row=0, column=0, sticky="nsew", padx=2*df.PAD_X, pady=df.LABEL_FORM_PAD_Y)

        icon_frame = ctk.CTkFrame(category_icon_frame)
        icon_frame.grid(row=1, column=0, padx=df.PAD_X, pady=df.PAD_Y)
        self.icon_buttons: Dict[str, ctk.CTkButton] = {}
        column = 0 
        row = 0 
        
        for index, icon in enumerate(df.CATEGORY_ICONS):
            if index % 8 == 0 and index != 0: 
                row += 1
                column = 0
                
            button = ctk.CTkButton(
                icon_frame,
                height=46,
                width=46,
                text=icon,
                fg_color="transparent",
                font=self.fonts["ICON"],
                command=lambda c=icon: self._select_icon(c),
            )
            button.grid(
                column=column,
                row=row,
                padx=4,
                pady=5,
            )
            self.icon_buttons[icon] = button
            column += 1

    def _build_description_section(self) -> None:
        description_frame = ctk.CTkFrame(self.left_panel,fg_color=self.colors["top_frame"])
        description_frame.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=df.PAD_X,
            pady=df.PAD_Y,
        )

        description_frame.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            description_frame,
            text="AGREGA UNA DESCRIPCIÓN",
            font=self.fonts["SMALL"],
        ).grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=df.PAD_X,
            pady=df.LABEL_FORM_PAD_Y,
        )

        self.description_textbox = ctk.CTkTextbox(
            description_frame,
            height=100,
            font=self.fonts["SMALL"],
            border_width=2,
        )

        self.description_textbox.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=2*df.PAD_X,
            pady=df.PAD_Y,
        )

        self._set_textbox_placeholder(
            self.description_textbox,
            self.DEFAULT_DESCRIPTION_PLACEHOLDER,
        )

    # ---------------- RIGHT PANEL ----------------

    def _build_right_panel(self) -> None:
        self.right_panel = ctk.CTkScrollableFrame(
            self.master,
            corner_radius=df.CORNER_RADIUS
        )

        self.right_panel.columnconfigure(0, weight=1)
        self.right_panel.rowconfigure(0, weight=0)  
        self.right_panel.rowconfigure(1, weight=0)  
        self.right_panel.rowconfigure(2, weight=1)  

        self._build_weekday_section()
        self._build_color_section()
        self._build_navigation_buttons()

    def _build_weekday_section(self) -> None:
        week_frame = ctk.CTkFrame(self.right_panel, fg_color=self.colors["top_frame"])
        week_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=df.PAD_X,
            pady=df.PAD_Y,
        )

        week_frame.columnconfigure(0, weight=1)
        week_frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(
            week_frame,
            text="DÍAS DE LA SEMANA",
            font=self.fonts["SMALL"],
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="nsew",
            padx=df.PAD_X,
            pady=df.LABEL_FORM_PAD_Y,
        )

        days_frame = ctk.CTkFrame(week_frame)
        days_frame.grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="nsew",
            padx=df.PAD_X,
            pady=df.PAD_Y,
        )

        days = ["D", "L", "M", "M", "J", "V", "S"]

        for index, label in enumerate(days):
            button = ctk.CTkButton(
                days_frame,
                text=label,
                font=self.fonts["SMALL"],
                width=60,
                height=60,
                command=lambda i=index: self._toggle_day(i),
            )
            button.pack(side="left", expand=True, padx=13, pady=df.PAD_Y_HABIT_FORM_BUTTONS)

            self.day_buttons[index] = button
            self.day_button_states[index] = False

        self.select_all_switch = ctk.CTkSwitch(
            week_frame,
            text="SELECCIONAR TODOS",
            variable=self.select_all_var,
            command=self._handle_select_all,
            font=self.fonts["SMALL"],
        )

        self.select_all_switch.grid(
            row=2,
            column=1,
            sticky="e",
            padx=40,
            pady=30,
        )

        self.habit_state_switch = ctk.CTkSwitch(
            week_frame,
            text="ACTIVAR/DESACTIVAR HÁBITO",
            variable=self.habit_state_var,
            font=self.fonts["SMALL"],
        )

        self.habit_state_switch.grid(
            row=2,
            column=2,
            sticky="e",
            padx=40,
            pady=30,
        )

        self.feedback_label = ctk.CTkLabel(
            week_frame,
            text="",
            font=self.fonts["SMALL"],
            text_color="red",
            anchor="w",
        )

        self.feedback_label.grid(
            row=2,
            column=0,
            sticky="w",
            padx=40,
            pady=30,
        )

    def _build_color_section(self) -> None: 
        color_frame = ctk.CTkFrame(self.right_panel,fg_color=self.colors["top_frame"])
        color_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=df.PAD_X,
            pady=df.PAD_Y,
        )

        color_frame.columnconfigure(0, weight=1)
        color_frame.columnconfigure(1, weight=1)

        ctk.CTkLabel(
            color_frame,
            text="COLOR DEL HÁBITO",
            font=self.fonts["SMALL"],
        ).grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=df.PAD_X,
            pady=df.LABEL_FORM_PAD_Y,
        )

        color_panel = ctk.CTkFrame(color_frame)
        color_panel.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=df.PAD_X,
            pady=df.PAD_Y,
        )
        
        self.color_buttons: Dict[str, ctk.CTkButton] = {}
        row = 0 
        column = 0
        
        for index, color in enumerate(df.HEX_COLOR_PALETTE):
            if index % 23 == 0 and index != 0: 
                row += 1
                column = 0
                
            button = ctk.CTkButton(
                color_panel,
                fg_color=color,
                height=48,
                font=self.fonts["SUBTITLE"],
                border_width=3,
                text="",
                command=lambda c=color: self._select_color(c),
            )
    
            button.grid(
                column=column,
                row=row,
                sticky="nsew",
                padx=5,
                pady=5,
            )
            self.color_buttons[color] = button
            column += 1
            
        self.config_grid(color_panel)

    def config_grid(self, frame: ctk.CTkFrame) -> None: 
        for row in range(4): 
            frame.grid_rowconfigure(row, weight=1)
        for column in range(23):
            frame.grid_columnconfigure(column, weight=1, uniform="col")

    def _build_navigation_buttons(self) -> None:
        nav_frame = ctk.CTkFrame(self.right_panel, fg_color=self.colors["top_frame"])
        nav_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=df.PAD_X,
            pady=df.PAD_Y,
        )

        nav_frame.columnconfigure(0, weight=1)
        nav_frame.columnconfigure(1, weight=1)

        cancel_btn = ctk.CTkButton(
            nav_frame,
            text="CANCELAR",
            command=self._go_to_main_view_event,
            font=self.fonts["SUBTITLE"],
        )
        cancel_btn.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=df.PAD_X,
            pady=df.PAD_Y,
        )

        self.save_button = ctk.CTkButton(
            nav_frame,
            text="AGREGAR HÁBITO",
            command=self._handle_create_habit,
            font=self.fonts["SUBTITLE"],
        )
        self.save_button.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=df.PAD_X,
            pady=df.PAD_Y,
        )

    # =========================================================
    # STATE LOGIC
    # =========================================================
    
    def _go_to_main_view_event(self) -> None:
        self.go_to_main_view()
        self._hide_feedback()
        self._clean_selection()

    def _has_changes(self) -> bool:
        current_data = {
            "name": self.name_entry.get().strip(),
            "execution_days": list(self.day_button_states.values()),
            "color": self.selected_color,
            "category": self.build_category(),
            "description": self.description_textbox.get("0.0", "end-1c").strip(),
            "is_active": self.habit_state_var.get()
        }

        return current_data != getattr(self, "_original_habit_snapshot", {})

    def _toggle_day(self, index: int) -> None:
        current = self.day_button_states[index]
        new_state = not current
        self._set_day_button_state(self.day_buttons[index], index, new_state)
        self._sync_select_all_switch()

    def _sync_select_all_switch(self) -> None:
        all_selected = all(self.day_button_states.values())
        if self.select_all_var.get() != all_selected:
            self.select_all_var.set(all_selected)

    def _sync_habit_state_switch(self, current_state: bool) -> None:
        self.habit_state_var.set(current_state)

    def _set_day_button_state(self, button: ctk.CTkButton, index: int, state: bool) -> None:
        self.day_button_states[index] = state
        if state:
            button.configure(border_width=4, border_color=self.colors["text"])
        else:
            button.configure(border_width=0)

    def _handle_select_all(self) -> None:
        state = self.select_all_var.get()
        for index, button in self.day_buttons.items():
            self._set_day_button_state(button, index, state)

    def _select_color(self, color: str) -> None:
        if self.selected_color == color:
            return
            
        if self._last_selected_color_button:
            self._last_selected_color_button.configure(text="")

        current_button = self.color_buttons.get(color)
        if current_button:
            current_button.configure(text="✓")
            self._last_selected_color_button = current_button
            
        self.selected_color = color

    def _select_icon(self, icon: str) -> None:
        for btn in self.icon_buttons.values():
            btn.configure(border_width=0)
        
        if icon in self.icon_buttons:
            self.icon_buttons[icon].configure(border_width=3)
            self.selected_icon = icon

    def _show_error(self, message: str) -> None:
        self.feedback_label.configure(
            text=message,
            text_color="red",
        )

    def _show_warning(self, message: str) -> None:
        self.feedback_label.configure(
            text=message,
            text_color="orange",
        )

    def _hide_feedback(self) -> None:
        self.feedback_label.configure(text="")

    # =========================================================
    # ACTIONS
    # =========================================================

    def _handle_create_habit(self) -> None:
        self._submit_habit(self.create_habit_callback)

    def _handle_update_habit(self) -> None:
        self._submit_habit(self.update_habit_callback, include_id=True)

    def _clean_selection(self) -> None:
        self.selected_icon = None
        self.selected_color = None

        for btn in self.icon_buttons.values():
            btn.configure(border_width=0)

        for btn in self.color_buttons.values():
            btn.configure(text="")

        self._last_selected_color_button = None

        for index, button in self.day_buttons.items():
            self._set_day_button_state(button, index, False)

        self.select_all_var.set(False)

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, self.DEFAULT_NAME_PLACEHOLDER)
        self.name_entry.configure(text_color="gray")

        self.description_textbox.delete("0.0", "end")
        self.description_textbox.insert("0.0", self.DEFAULT_DESCRIPTION_PLACEHOLDER)
        self.description_textbox.configure(text_color="gray")

        categories = self.get_categories_callback() or ["Crea una nueva categoría"]
        self.category_combobox.configure(values=categories)
        self.category_combobox.set("")

        self.save_button.focus_set()
        
    def build_category(self) -> str:
        category_icon = self.selected_icon
        category_name = self.category_combobox.get()
        if category_icon is None: 
            return category_name
        
        return f"{category_icon} {category_name}"

    def _validate_form(self) -> bool:
        name = self.name_entry.get().strip()
        if not name or name == self.DEFAULT_NAME_PLACEHOLDER:
            self._show_error("Debes ingresar un nombre para el hábito*")
            return False

        if not any(self.day_button_states.values()):
            self._show_error("Debes seleccionar al menos un día*")
            return False

        if not self.selected_color:
            self._show_error("Debes seleccionar un color*")
            return False

        return True

    def _submit_habit(self, callback: Callable[[Dict[str, Any]], None], include_id: bool = False) -> None:
        self._hide_feedback()

        if not self._validate_form():
            return

        if self.view_mode == "edit" and not self._has_changes():
            self._show_warning("No has realizado ningún cambio*")
            return

        name = self.name_entry.get().strip()
        description = self.description_textbox.get("0.0", "end-1c").strip()

        if name == self.DEFAULT_NAME_PLACEHOLDER:
            name = ""

        if description == self.DEFAULT_DESCRIPTION_PLACEHOLDER:
            description = ""
        



        logger.info(self.habit_state_var.get())
        data: Dict[str, Any] = {
            "name": name,
            "execution_days": list(self.day_button_states.values()),
            "is_active": self.habit_state_var.get(),
            "color": self.selected_color,
            "category": self.build_category(),
            "description": description,
        }

        if include_id:
            data["id"] = self.loaded_habit_id

        callback(data)

        self.go_to_main_view()
        self._hide_feedback()
        self._clean_selection()
        
    # =========================================================
    # PLACEHOLDER HELPERS
    # =========================================================

    def _set_entry_placeholder(self, entry: ctk.CTkEntry, text: str) -> None:
        entry.insert(0, text)
        entry.configure(text_color="gray")

        def on_focus_in(_: Any) -> None:
            if entry.get() == text:
                entry.delete(0, "end")
                entry.configure(text_color=self.colors["text"])

        def on_focus_out(_: Any) -> None:
            if entry.get() == "":
                entry.insert(0, text)
                entry.configure(text_color="gray")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def _set_textbox_placeholder(self, textbox: ctk.CTkTextbox, text: str) -> None:
        textbox.insert("0.0", text)
        textbox.configure(text_color="gray")

        def on_focus_in(_: Any) -> None:
            if textbox.get("0.0", "end").strip() == text:
                textbox.delete("0.0", "end")
                textbox.configure(text_color=self.colors["text"])

        def on_focus_out(_: Any) -> None:
            if textbox.get("0.0", "end").strip() == "":
                textbox.insert("0.0", text)
                textbox.configure(text_color="gray")

        textbox.bind("<FocusIn>", on_focus_in)
        textbox.bind("<FocusOut>", on_focus_out)