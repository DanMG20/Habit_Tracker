import customtkinter as ctk
from infrastructure.config import defaults as df
from ui.dialogs.windows.base_window import BaseModalWindow
from CTkMessagebox import CTkMessagebox


class BaseCrudWindow(BaseModalWindow):

    def __init__(
        self,
        master,
        styles,
        title,
        width,
        height,
        get_items,
        on_add,
        on_update,
        on_delete,
    ):
        super().__init__(
            master=master,
            styles=styles,
            title=title,
            width=width,
            height=height,
        )

        self.get_items = get_items
        self.on_add = on_add
        self.on_update = on_update
        self.on_delete = on_delete

        self.fonts = styles["fonts"]
        self.theme_colors = styles["colors"]

        self.selected = None
        self.selected_button = None

        self._build()


    # =========================================================
    # BUILD TEMPLATE
    # =========================================================

    def _build(self):
        self._configure_grid()
        self._draw_table()
        self._draw_edit_panel()
        self._draw_buttons()
        self._update_buttons_state()


    def _configure_grid(self):
        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_columnconfigure(1, weight=0)
        self.body.grid_rowconfigure(0, weight=1)


    # =========================================================
    # TABLE
    # =========================================================

    def _draw_table(self):
        self.table_frame = ctk.CTkScrollableFrame(
            self.body,
            corner_radius=df.CORNER_RADIUS
        )
        self.table_frame.grid(
            row=0,
            column=0,
            padx=df.PADX,
            pady=df.PADY,
            sticky="nsew"
        )

        self._draw_headers()
        self._draw_rows()


    def _refresh_table(self):
        for child in self.table_frame.winfo_children():
            info = child.grid_info()
            if info.get("row") and info["row"] >= 1:
                child.destroy()

        self._draw_rows()


    # =========================================================
    # EDIT PANEL
    # =========================================================

    def _draw_edit_panel(self):
        self.edit_panel = ctk.CTkFrame(
            self.body,
            corner_radius=df.CORNER_RADIUS
        )
        self.edit_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY
        )

        self.edit_panel.grid_columnconfigure(0, weight=1)

        self._draw_form_fields()
        self._draw_error_frame()

        self.edit_panel.grid_rowconfigure(100, weight=1)


    def _draw_error_frame(self):
        self.error_frame = ctk.CTkFrame(
            self.edit_panel,
            fg_color="transparent",
            height=40
        )
        self.error_frame.grid(row=97, column=0, sticky="nsew")
        self.error_frame.grid_propagate(False)

        self.error_frame.grid_columnconfigure(0, weight=1)

        self.label_required = ctk.CTkLabel(
            self.error_frame,
            text="Campos obligatorios*",
            text_color="red",
            font=self.fonts["SMALL"]
        )
        self.label_required.grid(row=0, column=0, sticky="nsew")
        self.label_required.grid_remove()

        self.label_no_changes = ctk.CTkLabel(
            self.error_frame,
            text="No realizaste ningún cambio*",
            text_color="orange",
            font=self.fonts["SMALL"]
        )
        self.label_no_changes.grid(row=0, column=0, sticky="nsew")
        self.label_no_changes.grid_remove()



    def _hide_errors(self):
        self.label_required.grid_remove()
        self.label_no_changes.grid_remove()


    # =========================================================
    # BUTTONS
    # =========================================================

    def _draw_buttons(self):
        self.button_panel = ctk.CTkFrame(
            self.edit_panel,
            corner_radius=df.CORNER_RADIUS
        )
        self.button_panel.grid(
            row=100,
            column=0,
            sticky="nsew",
            pady=df.PADY,
            padx=df.PADX
        )

        self.button_panel.grid_columnconfigure(0, weight=1)

        self.btn_add = ctk.CTkButton(
            self.button_panel,
            text="Agregar",
            font=self.fonts["SMALL"],
            command=self._add
        )
        self.btn_add.pack(fill="both", pady=5, expand=True)

        self.btn_update = ctk.CTkButton(
            self.button_panel,
            text="Editar",
            font=self.fonts["SMALL"],
            command=self._update
        )
        self.btn_update.pack(fill="both", pady=5, expand=True)

        self.btn_delete = ctk.CTkButton(
            self.button_panel,
            text="Eliminar",
            font=self.fonts["SMALL"],
            command=self._delete
        )
        self.btn_delete.pack(fill="both", pady=5, expand=True)

        self.btn_clean = ctk.CTkButton(
            self.button_panel,
            text="Limpiar selección",
            font=self.fonts["SMALL"],
            command=self._clean_wrapper
        )
        self.btn_clean.pack(fill="both", pady=5, expand=True)


    def _update_buttons_state(self):
        has_selection = self.selected is not None

        self.btn_add.configure(state="disabled" if has_selection else "normal")
        self.btn_update.configure(state="normal" if has_selection else "disabled")
        self.btn_delete.configure(state="normal" if has_selection else "disabled")
        self.btn_clean.configure(state="normal" if has_selection else "disabled")


    # =========================================================
    # GENERIC EVENTS
    # =========================================================

    def _on_select(self, item, button):

        # 🔥 Resetear botón anterior si existe
        if self.selected_button:
            self.selected_button.configure(
                fg_color=self.theme_colors["top_frame"]
            )

        self.selected = item
        self.selected_button = button
        self._write_selected()

        # Pintar el nuevo seleccionado
        button.configure(
            fg_color=self.theme_colors["progressbar"]
        )

        self._update_buttons_state()


    def _add(self):
        self._hide_errors()
        if not self._validate_add():
            return

        self._perform_add()
        self._refresh_table()
        self._clean_wrapper()


    def _update(self):
        if not self.selected:
            return

        self._hide_errors()

        if not self._validate_update():
            return
        
        self._perform_update()
        self._clean_wrapper()
        self._refresh_table()
        


    def _delete(self):

        if not self.selected:
            return


        msg = CTkMessagebox(
            master=self,
            title="Confirmación",
            message="¿Eliminar la selección?",
            font=self.fonts["SMALL"],
            icon="question",
            option_1="No",
            option_2="Sí",
        )
        if msg.get() == "Sí":
        
            self.on_delete(self.selected["id"])
            self._clean_wrapper()
            self._refresh_table()
        



    def _clean_wrapper(self):

        # 🔥 Restaurar color visual
        if self.selected_button:
            self.selected_button.configure(
                fg_color=self.theme_colors["top_frame"]
            )

        self.selected = None
        self.selected_button = None

        self._clean()  # esto llama al método hijo
        self._update_buttons_state()


    # =========================================================
    # ABSTRACT METHODS (OVERRIDE)
    # =========================================================

    def _draw_headers(self): pass
    def _draw_rows(self): pass
    def _draw_form_fields(self): pass
    def _write_selected(self): pass
    def _validate_add(self): return True
    def _validate_update(self): return True
    def _perform_add(self): pass
    def _perform_update(self): pass
    def _clean(self): pass
    # =========================================================
    # HELPERS
    # =========================================================

    def _shorten(self, text, max_length=35):
        if not text:
            return ""
        return text if len(text) <= max_length else text[:max_length - 3] + "..."
