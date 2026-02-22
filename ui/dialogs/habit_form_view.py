import customtkinter as ctk
import infrastructure.config.defaults as df
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class HabitFormView:

    DEFAULT_NAME_PLACEHOLDER = "Levantarse temprano, Regar las plantas, etc..."
    DEFAULT_CATEGORY_PLACEHOLDER = "Tareas, Estudio, Cuidado personal, Proyectos..."
    DEFAULT_DESCRIPTION_PLACEHOLDER = "Levantarse a las 7 am, Caminar 15 min, etc..."

    VIEW_TITLES = {
        "add": "AGREGAR HÁBITO",
        "edit": "EDITAR HÁBITO"
    }

    FILLER_HEIGHT = 50

    def __init__(
        self,
        master,
        styles,
        go_to_main_view,
        create_habit_callback,
        update_habit_callback,
        get_categories_callback,
    ):

        self.master = master
        self.fonts = styles["fonts"]
        self.colors = styles["colors"]

        self.view_mode = "add"
        self.go_to_main_view = go_to_main_view
        self.create_habit_callback = create_habit_callback
        self.update_habit_callback = update_habit_callback
        self.get_categories_callback = get_categories_callback

        self.command_map = {
            "add": self._handle_create_habit,
            "edit": self._handle_update_habit,
        }

        self.loaded_habit_id = None
        self.select_all_var = ctk.BooleanVar(value=False)
        self.selected_icon = None
        self.selected_color = None
        self._last_selected_color_button = None 
        self.day_buttons = {}
        self.day_button_states = {}

        self._build_layout()

    # =========================================================
    # PUBLIC API
    # =========================================================

    def set_view_mode(self, mode: str):
        if self.view_mode == mode:
            return
        self.view_mode = mode
        self._apply_view_mode()

    def load_habit(self, habit: dict):
        self.loaded_habit_id = habit["id"]

        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, habit["habit_name"])

        self.category_combobox.set(habit["category"])

        self.description_textbox.delete("1.0", "end")
        self.description_textbox.insert("1.0", habit["description"])

        self._select_color(habit["habit_color"])

        for (key, button), state in zip(self.day_buttons.items(), habit["execution_days"]):
            self._set_day_button_state(button, key, state)

        self._sync_select_all_switch()

        self._original_habit_snapshot = {
            "name": habit["habit_name"],
            "execution_days": habit["execution_days"],
            "color": habit["habit_color"],
            "category": habit["category"],
            "description": habit["description"],
        }

    def _build_layout(self):
        self._build_header()
        self._build_left_panel()
        self._build_right_panel()

    # ---------------- HEADER ----------------

    def _build_header(self):
        self.header_frame = ctk.CTkFrame(self.master, corner_radius=df.CORNER_RADIUS)

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=self.VIEW_TITLES["add"],
            font=self.fonts["SUBTITLE"],
            anchor="center",
        )
        self.title_label.pack(fill="both", expand=True, padx=df.PADX, pady=df.PADY)

    def _apply_view_mode(self):
        self.title_label.configure(text=self.VIEW_TITLES[self.view_mode])
        self.save_button.configure(
            text=self.VIEW_TITLES[self.view_mode],
            command=self.command_map[self.view_mode],
        )

    # ---------------- LEFT PANEL ----------------

    def _build_left_panel(self):
        self.left_panel = ctk.CTkFrame(self.master)
        self._build_name_section()
        self._build_category_section()
        self._build_category_icon_section()
        self._build_description_section()
        

        self.left_panel.columnconfigure(0, weight=1)
        self.left_panel.rowconfigure(3, weight=1)



    def _build_name_section(self):

        name_frame = ctk.CTkFrame(self.left_panel)
        name_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY,
        )

        name_frame.columnconfigure(0, weight=1)
        ctk.CTkLabel(
            name_frame,
            text="INGRESA EL NOMBRE DE TU HÁBITO",
            font=self.fonts["SMALL"],
        ).grid(row=0, column=0, sticky="nsew", padx=2*df.PADX, pady=df.LABEL_FORM_PADY)

        self.name_entry = ctk.CTkEntry(name_frame, font=self.fonts["SMALL"])
        self.name_entry.grid(row=1, column=0, sticky="nsew", padx=df.PADX, pady=df.PADY)

        self._set_entry_placeholder(self.name_entry, self.DEFAULT_NAME_PLACEHOLDER)

 
    def _build_category_section(self):
        categories = self.get_categories_callback() or ["Crea una nueva categoría"]


        category_frame = ctk.CTkFrame(self.left_panel)
        category_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY,
        )

        category_frame.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            category_frame,
            text="SELECCIONA O CREA UNA CATEGORÍA",
            font=self.fonts["SMALL"],
        ).grid(row=2, column=0, sticky="nsew", padx=2*df.PADX, pady=df.LABEL_FORM_PADY)

        self.category_combobox = ctk.CTkComboBox(
            category_frame,
            values=categories,
            font=self.fonts["SMALL"],
        )
        self.category_combobox.grid(row=3, column=0, sticky="ew", padx=df.PADX, pady=df.PADY)

    def _build_category_icon_section(self):

        category_icon_frame = ctk.CTkFrame(self.left_panel)
        category_icon_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY,
        )

        category_icon_frame.columnconfigure(0, weight=1)
        ctk.CTkLabel(
            category_icon_frame,
            text="ELIGE UN ICONO PARA TU CATEGORIA",
            font=self.fonts["SMALL"],
        ).grid(row=0, column=0, sticky="nsew", padx=2*df.PADX, pady=df.LABEL_FORM_PADY)


        icon_frame = ctk.CTkFrame(category_icon_frame)
        icon_frame.grid(row=1, column=0, padx=df.PADX, pady=df.PADY,)
        self.icon_buttons = {}
        column=0 
        row=0 
        for index,icon in enumerate(df.CATEGORY_ICONS):
            if index%8 ==0 and index!=0: 
                row+=1
                column=0
            button = ctk.CTkButton(
                icon_frame,
                width=46,
                height=46,
                text=icon,
                fg_color="transparent",
                font = self.fonts["ICON"],
                command=lambda c=icon: self._select_icon(c),
            )
            button.grid(
                column= column,
                row = row,
                  padx=4,
                  pady=5,
                  )
            self.icon_buttons[icon] = button

            column +=1


    def _build_description_section(self):
            
        description_frame = ctk.CTkFrame(self.left_panel)
        description_frame.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY,
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
            padx=df.PADX,
            pady=df.LABEL_FORM_PADY,
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
            padx=2* df.PADX,
            pady=df.PADY,
        )

        self._set_textbox_placeholder(
            self.description_textbox,
            self.DEFAULT_DESCRIPTION_PLACEHOLDER,
        )


    # ---------------- RIGHT PANEL ----------------

    def _build_right_panel(self):
        self.right_panel = ctk.CTkFrame(
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



    def _build_weekday_section(self):

        week_frame = ctk.CTkFrame(self.right_panel)
        week_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY,
        )

        week_frame.columnconfigure(0, weight=1)
        week_frame.columnconfigure(1, weight=1)

        # ======================================================
        # DÍAS DE LA SEMANA
        # ======================================================

        ctk.CTkLabel(
            week_frame,
            text="DÍAS DE LA SEMANA",
            font=self.fonts["SMALL"],
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=df.PADX,
            pady=df.LABEL_FORM_PADY,
        )

        days_frame = ctk.CTkFrame(week_frame)
        days_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY,
        )

        days = ["D", "L", "M", "M", "J", "V", "S"]

        for index, label in enumerate(days):
            button = ctk.CTkButton(
                days_frame,
                text=label,
                font = self.fonts["SMALL"],
                width=60,
                height=60,
                command=lambda i=index: self._toggle_day(i),
            )
            button.pack(side="left", expand=True, padx=13,pady = df.PADY_BUTTONS_HABIT_FORM)

            self.day_buttons[index] = button
            self.day_button_states[index] = False

        # ======================================================
        # SWITCH SELECCIONAR TODOS
        # ======================================================

        select_all_switch = ctk.CTkSwitch(
            week_frame,
            text="SELECCIONAR TODOS",
            variable=self.select_all_var,
            command=self._handle_select_all,
            font=self.fonts["SMALL"],
        )

        select_all_switch.grid(
            row=2,
            column=1,
            sticky="e",
            padx=40,
            pady=30,
        )

        # ======================================================
        # ERROR / WARNING LABEL
        # ======================================================

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

        self.feedback_label.grid_remove()  # 👈 inicia oculto


    def _build_color_section(self): 
        color_frame = ctk.CTkFrame(self.right_panel)
        color_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY,
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
            padx=df.PADX,
            pady=df.LABEL_FORM_PADY,
        )

        color_frame = ctk.CTkFrame(color_frame)
        color_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY,
        )

        self.color_buttons = {}
        row=0 
        column=0
        for index,color in enumerate(df.COLORES):
            if index%23 ==0 and index!=0: 
                row+=1
                column=0
            button = ctk.CTkButton(
                color_frame,
                fg_color=color,
                width=49,
                height=50,
                font = self.fonts["SUBTITLE"],
                border_width=3,
                text="",
                command=lambda c=color: self._select_color(c),
            )
            button.grid(
                column= column,
                row = row,
                sticky = "nsew",
                  padx=5,
                  pady=5,
                  )
            self.color_buttons[color] = button

            column +=1

    def _build_navigation_buttons(self):

        nav_frame = ctk.CTkFrame(self.right_panel)
        nav_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY,
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
            padx=df.PADX,
            pady=df.PADY,
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
            padx=df.PADX,
            pady=df.PADY,
        )

    # =========================================================
    # STATE LOGIC
    # =========================================================
    def _go_to_main_view_event(self):
        self.go_to_main_view()
        self._hide_feedback()
        self._clean_selection()
    def _has_changes(self):

        current_data = {
            "name": self.name_entry.get().strip(),
            "execution_days": list(self.day_button_states.values()),
            "color": self.selected_color,
            "category": self.build_category(),
            "description": self.description_textbox.get("0.0", "end-1c").strip(),
        }

        return current_data != self._original_habit_snapshot

    def _toggle_day(self, index: int):
        current = self.day_button_states[index]
        new_state = not current
        self._set_day_button_state(self.day_buttons[index], index, new_state)

        # 👇 sincronizar switch después del cambio
        self._sync_select_all_switch()

    def _sync_select_all_switch(self):
        all_selected = all(self.day_button_states.values())

        if self.select_all_var.get() != all_selected:
            self.select_all_var.set(all_selected)
    def _set_day_button_state(self, button, index, state: bool):
        self.day_button_states[index] = state

        if state:
            button.configure(border_width=4, border_color=self.colors["text"])
        else:
            button.configure(border_width=0)

    def _handle_select_all(self):
        state = self.select_all_var.get()

        for index, button in self.day_buttons.items():
            self._set_day_button_state(button, index, state)

    def _select_color(self, color: str):
        
        if self.selected_color == color:
            return
        # Si ya hay uno seleccionado, quitarle el check
        if self._last_selected_color_button:
            self._last_selected_color_button.configure(text="")

        # Seleccionar el nuevo
        current_button = self.color_buttons[color]
        current_button.configure(text="✓")

        # Guardar referencia
        self._last_selected_color_button = current_button
        self.selected_color = color
    def _select_icon(self, icon: str):
        for btn in self.icon_buttons.values():
            btn.configure(border_width = 0)
        
        self.icon_buttons[icon].configure(
            border_width =3,
        )
        self.selected_icon = icon

    def _show_error(self, message: str):
        self.feedback_label.configure(
            text=message,
            text_color="red",
        )
        self.feedback_label.grid()


    def _show_warning(self, message: str):
        self.feedback_label.configure(
            text=message,
            text_color="orange",
        )
        self.feedback_label.grid()


    def _hide_feedback(self):
        self.feedback_label.grid_remove()


    # =========================================================
    # ACTIONS
    # =========================================================

    def _handle_create_habit(self):
        self._submit_habit(self.create_habit_callback)

    def _handle_update_habit(self):
        self._submit_habit(self.update_habit_callback, include_id=True)

    def _clean_selection(self):

        # ==========================
        # Reset icon & color
        # ==========================
        self.selected_icon = None
        self.selected_color = None

        for btn in self.icon_buttons.values():
            btn.configure(border_width=0)

        for btn in self.color_buttons.values():
            btn.configure(text="")

        self._last_selected_color_button = None
        # ==========================
        # Reset days
        # ==========================
        for index, button in self.day_buttons.items():
            self._set_day_button_state(button, index, False)

        self.select_all_var.set(False)

        # ==========================
        # Reset name entry
        # ==========================
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, self.DEFAULT_NAME_PLACEHOLDER)
        self.name_entry.configure(text_color="gray")

        # ==========================
        # Reset description textbox
        # ==========================
        self.description_textbox.delete("0.0", "end")
        self.description_textbox.insert("0.0", self.DEFAULT_DESCRIPTION_PLACEHOLDER)
        self.description_textbox.configure(text_color="gray")

        # ==========================
        # Reset category
        # ==========================
        categories = self.get_categories_callback() or ["Crea una nueva categoría"]
        self.category_combobox.configure(values=categories)
        self.category_combobox.set("")

        self.save_button.focus_set()
        

    def build_category(self):
        category_icon = self.selected_icon
        category_name = self.category_combobox.get()
        if category_icon == None: 
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


    def _submit_habit(self, callback, include_id=False):

        self._hide_feedback()

        if not self._validate_form():
            return

        if self.view_mode == "edit" and not self._has_changes():
            self._show_warning("No has realizado ningún cambio.")
            return

        name = self.name_entry.get().strip()
        description = self.description_textbox.get("0.0", "end-1c").strip()

        if name == self.DEFAULT_NAME_PLACEHOLDER:
            name = ""

        if description == self.DEFAULT_DESCRIPTION_PLACEHOLDER:
            description = ""

        data = {
            "name": name,
            "execution_days": list(self.day_button_states.values()),
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

    def _set_entry_placeholder(self, entry, text):
        entry.insert(0, text)
        entry.configure(text_color="gray")

        def on_focus_in(_):
            if entry.get() == text:
                entry.delete(0, "end")
                entry.configure(text_color=self.colors["text"])

        def on_focus_out(_):
            if entry.get() == "":
                entry.insert(0, text)
                entry.configure(text_color="gray")

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def _set_textbox_placeholder(self, textbox, text):
        textbox.insert("0.0", text)
        textbox.configure(text_color="gray")

        def on_focus_in(_):
            if textbox.get("0.0", "end").strip() == text:
                textbox.delete("0.0", "end")
                textbox.configure(text_color=self.colors["text"])

        def on_focus_out(_):
            if textbox.get("0.0", "end").strip() == "":
                textbox.insert("0.0", text)
                textbox.configure(text_color="gray")

        textbox.bind("<FocusIn>", on_focus_in)
        textbox.bind("<FocusOut>", on_focus_out)
