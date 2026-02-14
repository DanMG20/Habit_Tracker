import customtkinter as ctk
from infrastructure.config import defaults as df
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

class GoalWindow(ctk.CTkToplevel):
    # ---------- CONFIG POR CLASE ----------
    WINDOW_TITLE = "Objetivos"
    TABLE_TITLE = {"main_title": "Objetivos guardados"}
    TABLE_HEADERS = ["Nombre", "Periodo", "Año"]

    ADD_TEXT = "Agregar"
    UPDATE_TEXT = "Editar"
    DELETE_TEXT = "Eliminar"
    MAX_TEXT_LEN = 30

    PERIOD_VALUES = ["1-13", "14-26", "27-39", "40-52"]  # Combobox periodo

    def __init__(self, 
                 master, 
                 style_settings, 
                 on_add, get_rows, 
                 on_delete, on_update, 
                 current_years=None):
        super().__init__(master)

        self.fonts = style_settings["fonts"]
        self.theme_colors = style_settings["colors"]

        self.on_add = on_add
        self.get_rows = get_rows
        self.on_delete = on_delete
        self.on_update = on_update

        self.current_years = [str(current_years["current_year"]), str(current_years["next_year"])] if current_years else ["", ""]
        self.selected = None
        self.resizable(False, False)

        self._build()

    # ---------- BUILD ----------
    def _build(self):
        self._draw_window()
        self._config_layout()
        self._draw_edit_panel()
        self._draw_entries()
        self._draw_table()
        self._draw_buttons()

    # ---------- WINDOW ----------
    def _draw_window(self):
        self.grab_set()
        w, h = 1000, 430
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")
        self.title(self.WINDOW_TITLE)

    def _config_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure(0, weight=1)

    # ---------- TABLE ----------
    def _draw_table(self):
        self.table = ctk.CTkScrollableFrame(self, corner_radius=df.CORNER_RADIUS)
        self.table.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        ctk.CTkLabel(
            self.table,
            font=self.fonts["SMALL"],
            text=self.TABLE_TITLE["main_title"],
        ).grid(row=0, column=0, columnspan=3, pady=10)

        self._draw_table_headers()
        self._draw_rows()
        self._config_table()

    def _draw_table_headers(self):
        for i, header in enumerate(self.TABLE_HEADERS):
            ctk.CTkLabel(
                self.table,
                text=header,
                font=self.fonts["SMALL"],
                fg_color=self.theme_colors["top_frame"],
            ).grid(row=1, column=i, sticky="nsew", pady=2)

    def _draw_rows(self):
        for row_i, row in enumerate(self.get_rows()):
            values = [
                row["goal_name"],
                row["period_quarter"],
                row["period_year"],
            ]

            for col, value in enumerate(values):
                btn = ctk.CTkButton(
                    self.table,
                    text=self._shorten(str(value)),
                    font=self.fonts["SMALL"],
                    corner_radius=0,
                    state="normal" if col == 0 else "disabled",
                    fg_color=self.theme_colors["top_frame"],
                )
                btn.configure(
                    command=lambda r=row, b=btn: self._on_row_selected(r, b)
                )
                btn.grid(row=row_i + 2, column=col, sticky="nsew", pady=2)


    def _config_table(self):
        for i in range(3):
            self.table.grid_columnconfigure(i, weight=1)

    # ---------- EDIT PANEL ----------
    def _draw_edit_panel(self):
        self.edit_panel = ctk.CTkFrame(self, corner_radius=df.CORNER_RADIUS)
        self.edit_panel.grid(row=0, column=1, padx=df.PADX, pady=df.PADY, sticky="nsew")

    # ---------- ENTRIES ----------
    def _draw_entries(self):
        # Nombre del objetivo (entry)
        ctk.CTkLabel(self.edit_panel, text="Nombre del objetivo", font=self.fonts["SMALL"]).pack(pady=(10, 0), padx=df.PADX)
        self.entry_nombre = ctk.CTkEntry(self.edit_panel, width=350, font=self.fonts["SMALL"])
        self.entry_nombre.pack(pady=5, padx=df.PADX)

        # Periodo (combobox)
        ctk.CTkLabel(self.edit_panel, text="Periodo", font=self.fonts["SMALL"]).pack(pady=(10, 0), padx=df.PADX)
        self.entry_periodo = ctk.CTkComboBox(self.edit_panel, width=350, values=self.PERIOD_VALUES, font=self.fonts["SMALL"])
        self.entry_periodo.pack(pady=5, padx=df.PADX)

        # Año (combobox)
        ctk.CTkLabel(self.edit_panel, text="Año", font=self.fonts["SMALL"]).pack(pady=(10, 0), padx=df.PADX)
        self.entry_ano = ctk.CTkComboBox(self.edit_panel, width=350, values=self.current_years, font=self.fonts["SMALL"])
        self.entry_ano.pack(pady=5, padx=df.PADX)

    # ---------- BUTTONS ----------
    def _draw_buttons(self):
        panel = ctk.CTkFrame(self.edit_panel, corner_radius=df.CORNER_RADIUS)
        panel.pack(fill="both", expand=True, pady=df.PADY, padx=df.PADX)

        for text, cmd in (
            (self.ADD_TEXT, self._add),
            (self.UPDATE_TEXT, self._update),
            (self.DELETE_TEXT, self._delete),
            ("Limpiar selección", self._clean),
        ):
            ctk.CTkButton(panel, text=text, font=self.fonts["SMALL"], command=cmd).pack(fill="both", pady=df.PADY, expand=True)

    # ---------- CRUD ----------
    def _on_row_selected(self, row, button):
        self.selected = row

        self.entry_nombre.delete(0, "end")
        self.entry_nombre.insert(0, row["goal_name"])

        self.entry_periodo.set(row["period_quarter"])
        self.entry_ano.set(str(row["period_year"]))

        self._deselect_rows()
        button.configure(fg_color=self.theme_colors["progressbar"])

    def _add(self):
        values = [
            self.entry_nombre.get(),
            self.entry_periodo.get(),
            self.entry_ano.get(),
        ]
        self.on_add([tuple(values)])

    def _update(self):
        if not self.selected:
            return

        self.on_update(
            self.selected["id"],
            self.entry_nombre.get(),
            self.entry_periodo.get(),
            self.entry_ano.get(),
        )

    def _delete(self):
        if self.selected:
            self.on_delete(self.selected["id"])


    def _clean(self):
        self.entry_nombre.delete(0, "end")
        self.entry_periodo.set("")
        self.entry_ano.set("")
        self._deselect_rows()
        self.selected = None

    # ---------- UTIL ----------
    def _deselect_rows(self):
        for child in self.table.winfo_children():
            if isinstance(child, ctk.CTkButton):
                child.configure(fg_color=self.theme_colors["top_frame"])

    def _shorten(self, text):
        return text if len(text) <= self.MAX_TEXT_LEN else text[: self.MAX_TEXT_LEN - 3] + "..."
