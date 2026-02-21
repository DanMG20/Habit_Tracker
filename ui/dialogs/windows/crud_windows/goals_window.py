import customtkinter as ctk
from infrastructure.config import defaults as df
from ui.dialogs.windows.crud_windows.base_crud_window import BaseCrudWindow


class GoalWindow(BaseCrudWindow):

    WIDTH = 1000
    HEIGHT = 500

    TABLE_HEADERS = ["Nombre", "Periodo", "Año"]
    PERIOD_VALUES = ["1-13", "14-26", "27-39", "40-52"]

    def __init__(
        self,
        master,
        styles,
        on_add,
        get_rows,
        on_delete,
        on_update,
        current_years=None,
    ):

        self.current_years = (
            [str(current_years["current_year"]),
             str(current_years["next_year"])]
            if current_years
            else []
        )

        super().__init__(
            master=master,
            styles=styles,
            title="Objetivos",
            width=self.WIDTH,
            height=self.HEIGHT,
            get_items=get_rows,
            on_add=on_add,
            on_update=on_update,
            on_delete=on_delete,
        )

    # =========================================================
    # TABLE
    # =========================================================

    def _draw_headers(self):
        for i, header in enumerate(self.TABLE_HEADERS):
            ctk.CTkLabel(
                self.table_frame,
                text=header,
                font=self.fonts["SMALL"],
                fg_color=self.theme_colors["top_frame"]
            ).grid(row=0, column=i, sticky="nsew", pady=2)

            self.table_frame.grid_columnconfigure(i, weight=1)


    def _draw_rows(self):
        for index, row in enumerate(self.get_items()):

            values = [
                row["goal_name"],
                row["period_quarter"],
                row["period_year"],
            ]

            for col, value in enumerate(values):

                state = "normal" if col == 0 else "disabled"

                btn = ctk.CTkButton(
                    self.table_frame,
                    text=self._shorten(str(value), max_length=30),
                    font=self.fonts["SMALL"],
                    state=state,
                    corner_radius=0,
                    fg_color=self.theme_colors["top_frame"]
                )

                btn.configure(
                    command=lambda r=row, b=btn: self._on_select(r, b)
                )

                btn.grid(row=index + 1, column=col, sticky="nsew", pady=2)

    # =========================================================
    # FORM
    # =========================================================

    def _draw_form_fields(self):

        # Nombre
        ctk.CTkLabel(
            self.edit_panel,
            text="Nombre del objetivo:",
            font=self.fonts["SMALL"]
        ).grid(row=0, column=0, pady=(15, 0))

        self.entry_nombre = ctk.CTkEntry(
            self.edit_panel,
            width=350,
            font=self.fonts["SMALL"]
        )
        self.entry_nombre.grid(row=1, column=0, pady=5, padx=df.PADX)

        # Periodo
        ctk.CTkLabel(
            self.edit_panel,
            text="Periodo:",
            font=self.fonts["SMALL"]
        ).grid(row=2, column=0, pady=(10, 0))

        self.entry_periodo = ctk.CTkComboBox(
            self.edit_panel,
            values=self.PERIOD_VALUES,
            width=350,
            font=self.fonts["SMALL"],
            state="readonly"
        )
        self.entry_periodo.grid(row=3, column=0, pady=5, padx=df.PADX)

        # Año
        ctk.CTkLabel(
            self.edit_panel,
            text="Año:",
            font=self.fonts["SMALL"]
        ).grid(row=4, column=0, pady=(10, 0))

        self.entry_anio = ctk.CTkComboBox(
            self.edit_panel,
            values=self.current_years,
            width=350,
            font=self.fonts["SMALL"],
            state="readonly"
        )
        self.entry_anio.grid(row=5, column=0, pady=5, padx=df.PADX)

        # valores por defecto
        self.entry_periodo.set(self.PERIOD_VALUES[0])
        if self.current_years:
            self.entry_anio.set(self.current_years[0])

    # =========================================================
    # SELECTION
    # =========================================================

    def _write_selected(self):
        self.entry_nombre.delete(0, "end")
        self.entry_nombre.insert(0, self.selected["goal_name"])

        self.entry_periodo.set(self.selected["period_quarter"])
        self.entry_anio.set(str(self.selected["period_year"]))

    # =========================================================
    # VALIDATIONS
    # =========================================================

    def _validate_add(self):
        name = self.entry_nombre.get().strip()

        if not name:
            self.label_required.configure(
                text="El nombre del objetivo es obligatorio*"
            )
            self.label_required.grid()
            return False

        return True


    def _validate_update(self):
        name = self.entry_nombre.get().strip()
        period = self.entry_periodo.get()
        year = self.entry_anio.get()

        if not name:
            self.label_required.configure(
                text="El nombre del objetivo es obligatorio*"
            )
            self.label_required.grid()
            return False

        if (
            name == self.selected["goal_name"] and
            period == self.selected["period_quarter"] and
            str(year) == str(self.selected["period_year"])
        ):
            self.label_no_changes.grid()
            return False

        return True

    # =========================================================
    # CRUD
    # =========================================================

    def _perform_add(self):
        data = {
            "name": self.entry_nombre.get().strip(),
            "period_quarter": self.entry_periodo.get(),
            "period_year": self.entry_anio.get(),
        }

        self.on_add(data)


    def _perform_update(self):
        self.on_update(
            self.selected["id"],
            self.entry_nombre.get().strip(),
            self.entry_periodo.get(),
            self.entry_anio.get(),
        )


    def _clean(self):
        self.entry_nombre.delete(0, "end")
        self.entry_periodo.set(self.PERIOD_VALUES[0])

        if self.current_years:
            self.entry_anio.set(self.current_years[0])

        self.selected = None
        self._update_buttons_state()
        self._hide_errors()
