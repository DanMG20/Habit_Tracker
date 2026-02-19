import customtkinter as ctk
from infrastructure.config import defaults as df


class QuoteWindow(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        style_settings,
        on_add_quote,
        get_quotes,
        on_delete_quote,
        on_update_quote
    ):
        super().__init__(master)

        self.on_add_quote = on_add_quote
        self.get_quotes = get_quotes
        self.on_delete_quote = on_delete_quote
        self.on_update_quote = on_update_quote

        self.fonts = style_settings["fonts"]
        self.theme_colors = style_settings["colors"]

        self.selected_quote = None

        self.resizable(False, False)
        self._build()


    # =========================================================
    # BUILD
    # =========================================================

    def _build(self):
        self._draw_window()
        self._configure_grid()
        self._draw_table()
        self._draw_edit_panel()
        self._draw_buttons()
        self._update_buttons_state()


    # =========================================================
    # WINDOW
    # =========================================================

    def _draw_window(self):
        self.grab_set()

        width = 900
        height = 450  # 🔥 más alta para que nada se comprima

        x = (self.winfo_screenwidth() // 2) - (width // 2) + 143
        y = (self.winfo_screenheight() // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.title("Frases")


    def _configure_grid(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.rowconfigure(0, weight=1)


    # =========================================================
    # TABLE
    # =========================================================

    def _draw_table(self):
        self.quote_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=df.CORNER_RADIUS
        )
        self.quote_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        ctk.CTkLabel(
            self.quote_frame,
            text="Frases guardadas",
            font=self.fonts["SMALL"]
        ).grid(row=0, column=0, columnspan=2, pady=10)

        self._draw_headers()
        self._draw_quotes()

        self.quote_frame.grid_columnconfigure(0, weight=3)
        self.quote_frame.grid_columnconfigure(1, weight=1)


    def _draw_headers(self):
        headers = ["Frase", "Autor"]
        for i, header in enumerate(headers):
            ctk.CTkLabel(
                self.quote_frame,
                text=header,
                font=self.fonts["SMALL"],
                fg_color=self.theme_colors["top_frame"],
                corner_radius=0
            ).grid(row=1, column=i, sticky="nsew", pady=2)


    def _draw_quotes(self):
        quotes = self.get_quotes()

        for index, quote in enumerate(quotes):
            for col in range(2):

                state = "normal" if col == 0 else "disabled"

                btn = ctk.CTkButton(
                    self.quote_frame,
                    text=self._shorten(quote[col + 1]),
                    font=self.fonts["SMALL"],
                    state=state,
                    corner_radius=0,
                    fg_color=self.theme_colors["top_frame"]
                )

                btn.configure(
                    command=lambda q=quote, b=btn: self._on_select(q, b)
                )

                btn.grid(row=index + 2, column=col, sticky="nsew", pady=2)


    def _refresh_table(self):
        for child in self.quote_frame.winfo_children():
            info = child.grid_info()
            if info.get("row") and info["row"] >= 2:
                child.destroy()

        self._draw_quotes()


    # =========================================================
    # EDIT PANEL
    # =========================================================

    def _draw_edit_panel(self):
        self.edit_panel = ctk.CTkFrame(
            self,
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

        # Frase
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

        # Autor
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
        self.entry_author.grid(row=3, column=0, pady=5, padx=df.PADX)

        # 🔥 Frame fijo para errores
        self.error_frame = ctk.CTkFrame(
            self.edit_panel,
            fg_color="transparent",
            height=40
        )
        self.error_frame.grid(row=4, column=0)
        self.error_frame.grid_propagate(False)
        
        self.edit_panel.grid_rowconfigure(5, weight=1)

        self.label_required = ctk.CTkLabel(
            self.error_frame,
            text="Ambos campos son obligatorios*",
            text_color="red",
            font=self.fonts["SMALL"]
        )

        self.label_no_changes = ctk.CTkLabel(
            self.error_frame,
            text="No realizaste ningún cambio*",
            text_color="orange",
            font=self.fonts["SMALL"]
        )
        


    # =========================================================
    # BUTTONS
    # =========================================================

    def _draw_buttons(self):
        self.button_panel = ctk.CTkFrame(
            self.edit_panel,
            corner_radius=df.CORNER_RADIUS
        )
        self.button_panel.grid(
            row=5,
            column=0,
            sticky="nsew",
            pady=df.PADY,
            padx=df.PADX
        )

        self.btn_add = ctk.CTkButton(
            self.button_panel,
            text="Agregar frase",
            font=self.fonts["SMALL"],
            command=self._add_quote
        )
        self.btn_add.pack(fill="both", pady=5, expand=True)

        self.btn_update = ctk.CTkButton(
            self.button_panel,
            text="Editar frase",
            font=self.fonts["SMALL"],
            command=self._update_quote
        )
        self.btn_update.pack(fill="both", pady=5, expand=True)

        self.btn_delete = ctk.CTkButton(
            self.button_panel,
            text="Eliminar frase",
            font=self.fonts["SMALL"],
            command=self._delete_quote
        )
        self.btn_delete.pack(fill="both", pady=5, expand=True)

        self.btn_clean = ctk.CTkButton(
            self.button_panel,
            text="Limpiar selección",
            font=self.fonts["SMALL"],
            command=self._clean_selection
        )
        self.btn_clean.pack(fill="both", pady=5, expand=True)


    def _update_buttons_state(self):
        has_selection = self.selected_quote is not None

        self.btn_add.configure(state="disabled" if has_selection else "normal")
        self.btn_update.configure(state="normal" if has_selection else "disabled")
        self.btn_delete.configure(state="normal" if has_selection else "disabled")
        self.btn_clean.configure(state="normal" if has_selection else "disabled")


    # =========================================================
    # EVENTS
    # =========================================================

    def _on_select(self, quote, button):
        self.selected_quote = quote
        self._write_quote()

        for child in self.quote_frame.winfo_children():
            child.configure(fg_color=self.theme_colors["top_frame"])

        button.configure(fg_color=self.theme_colors["progressbar"])

        self._update_buttons_state()


    def _clean_selection(self):
        self.entry_quote.delete(0, "end")
        self.entry_author.delete(0, "end")
        self.selected_quote = None
        self._refresh_table()
        self._update_buttons_state()


    def _hide_errors(self):
        for widget in self.error_frame.winfo_children():
            widget.pack_forget()


    def _add_quote(self):
        quote = self.entry_quote.get().strip()
        author = self.entry_author.get().strip()

        self._hide_errors()

        if not quote or not author:
            self.label_required.pack()
            return

        self.on_add_quote([(quote, author)])
        self._refresh_table()
        self._clean_selection()


    def _update_quote(self):
        quote = self.entry_quote.get().strip()
        author = self.entry_author.get().strip()

        self._hide_errors()

        if not quote or not author:
            self.label_required.pack()
            return

        if (
            quote == self.selected_quote[1] and
            author == self.selected_quote[2]
        ):
            self.label_no_changes.pack()
            return

        self.on_update_quote(
            self.selected_quote[0],
            quote,
            author
        )

        self._refresh_table()
        self._clean_selection()


    def _delete_quote(self):
        self.on_delete_quote(self.selected_quote[0])
        self._refresh_table()
        self._clean_selection()


    # =========================================================
    # HELPERS
    # =========================================================

    def _write_quote(self):
        self.entry_quote.delete(0, "end")
        self.entry_quote.insert(0, self.selected_quote[1])

        self.entry_author.delete(0, "end")
        self.entry_author.insert(0, self.selected_quote[2])


    def _shorten(self, text):
        return text if len(text) <= 35 else text[:32] + "..."
