import customtkinter as ctk
from infrastructure.config import defaults as df
from ui.dialogs.windows.crud_windows.base_crud_window import BaseCrudWindow


class QuoteWindow(BaseCrudWindow):

    WIDTH = 900
    HEIGHT = 450

    def __init__(
        self,
        master,
        styles,
        on_add_quote,
        get_quotes,
        on_delete_quote,
        on_update_quote
    ):
        super().__init__(
            master=master,
            styles=styles,
            title="Frases",
            width=self.WIDTH,
            height=self.HEIGHT,
            get_items=get_quotes,
            on_add=on_add_quote,
            on_update=on_update_quote,
            on_delete=on_delete_quote,
        )

    # =========================================================
    # TABLE
    # =========================================================

    def _draw_headers(self):
        ctk.CTkLabel(
            self.table_frame,
            text="Frase",
            font=self.fonts["SMALL"],
            fg_color=self.theme_colors["top_frame"]
        ).grid(row=0, column=0, sticky="nsew", pady=2)

        ctk.CTkLabel(
            self.table_frame,
            text="Autor",
            font=self.fonts["SMALL"],
            fg_color=self.theme_colors["top_frame"]
        ).grid(row=0, column=1, sticky="nsew", pady=2)

        self.table_frame.grid_columnconfigure(0, weight=3)
        self.table_frame.grid_columnconfigure(1, weight=1)


    def _draw_rows(self):
        quotes = self.get_items()

    

        for index, quote in enumerate(quotes):
            for col in range(2):

                state = "normal" if col == 0 else "disabled"

                btn = ctk.CTkButton(
                    self.table_frame,
                    text=self._shorten(quote[col + 1]),
                    font=self.fonts["SMALL"],
                    state=state,
                    corner_radius=0,
                    fg_color=self.theme_colors["top_frame"]
                )

                btn.configure(
                    command=lambda q=quote, b=btn: self._on_select(q, b)
                )

                btn.grid(row=index + 1, column=col, sticky="nsew", pady=2)

    # =========================================================
    # FORM
    # =========================================================

    def _draw_form_fields(self):

        ctk.CTkLabel(
            self.edit_panel,
            text="Frase:",
            font=self.fonts["SMALL"]
        ).grid(row=0, column=0, pady=(15, 0))

        self.entry_quote = ctk.CTkEntry(
            self.edit_panel,
            width=350,
            font=self.fonts["SMALL"]
        )
        self.entry_quote.grid(row=1, column=0, pady=5, padx=df.PADX)

        ctk.CTkLabel(
            self.edit_panel,
            text="Autor:",
            font=self.fonts["SMALL"]
        ).grid(row=2, column=0, pady=(10, 0))

        self.entry_author = ctk.CTkEntry(
            self.edit_panel,
            width=350,
            font=self.fonts["SMALL"]
        )
        self.entry_author.grid(row=3, column=0, pady=10, padx=df.PADX)

    # =========================================================
    # SELECTION
    # =========================================================

    def _write_selected(self):
        self.entry_quote.delete(0, "end")
        self.entry_quote.insert(0, self.selected[1])

        self.entry_author.delete(0, "end")
        self.entry_author.insert(0, self.selected[2])

    # =========================================================
    # VALIDATIONS
    # =========================================================

    def _validate_add(self):
        quote = self.entry_quote.get().strip()
        author = self.entry_author.get().strip()

        if not quote or not author:
            self.label_required.configure(
                text="Ambos campos son obligatorios*"
            )
            self.label_required.grid()
            return False

        return True


    def _validate_update(self):
        quote = self.entry_quote.get().strip()
        author = self.entry_author.get().strip()

        if not quote or not author:
            self.label_required.configure(
                text="Ambos campos son obligatorios*"
            )
            self.label_required.grid()
            return False

        if (
            quote == self.selected[1] and
            author == self.selected[2]
        ):
            self.label_no_changes.grid()
            return False

        return True

    # =========================================================
    # CRUD OPERATIONS
    # =========================================================

    def _perform_add(self):
        quote = self.entry_quote.get().strip()
        author = self.entry_author.get().strip()

        self.on_add([(quote, author)])


    def _perform_update(self):
        quote = self.entry_quote.get().strip()
        author = self.entry_author.get().strip()

        self.on_update(
            self.selected[0],
            quote,
            author
        )

    def _clean(self):
        self.entry_quote.delete(0, "end")
        self.entry_author.delete(0, "end")
        self.selected = None
        self._update_buttons_state()
