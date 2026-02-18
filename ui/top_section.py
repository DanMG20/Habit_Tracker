import customtkinter as ctk
from PIL import Image
import infrastructure.config.defaults as df
from utils.paths import icon_path


class TopSection:

    events = {"day_changed"}
    def __init__(self, master, style_settings):
        self.master = master
        self.fonts = style_settings["fonts"]

        self.current_quote = ""
        self.current_author = ""

        self._build()

    # ================= BUILD =================

    def _build(self):
        self._draw_title_frame()
        self._draw_icon()
        self._draw_title()
        self._draw_quote_frame()

    # ================= STATIC UI =================

    def _draw_title_frame(self):
        self.title_frame = ctk.CTkFrame(
            self.master, corner_radius=df.CORNER_RADIUS
        )
        self.title_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=df.PADX,
            pady=(df.PADY * 2, df.PADY),
        )

    def _draw_icon(self):
        img_icono = ctk.CTkImage(
            light_image=Image.open(icon_path()),
            dark_image=Image.open(icon_path()),
            size=(100, 100),
        )

        icono_label = ctk.CTkLabel(
            self.title_frame, image=img_icono, text=""
        )
        icono_label.pack(side="left", fill="x", padx=5, pady=10)

    def _draw_title(self):
        tituloapp_label = ctk.CTkLabel(
            self.title_frame,
            font=self.fonts["TITLE"],
            text="HABIT TRACKER",
        )
        tituloapp_label.pack(side="right", fill="x", padx=(0, 30), pady=10)

    def _draw_quote_frame(self):
        self.frame_quote = ctk.CTkFrame(
            self.master, corner_radius=df.CORNER_RADIUS
        )
        self.frame_quote.grid(
            row=1,
            column=1,
            columnspan=3,
            sticky="nsew",
            padx=df.PADX,
            pady=(df.PADY * 2, df.PADY),
        )

        self.frame_quote.grid_rowconfigure(0, weight=1)
        self.frame_quote.grid_columnconfigure(0, weight=1)

        # Labels vacíos al inicio
        self.label_quote = ctk.CTkLabel(
            self.frame_quote,
            text="",
            justify="center",
            wraplength=850,
            font=self.fonts["PHRASE"],
        )
        self.label_quote.grid(row=0, column=0, padx=28, pady=(16, 2), sticky="n")

        self.label_author = ctk.CTkLabel(
            self.frame_quote,
            text="",
            font=self.fonts["AUTHOR"],
            text_color=df.COLOR_AUTOR,
        )
        self.label_author.grid(row=1, column=0, padx=18, pady=(0, 16), sticky="n")

    def refresh(self, view_state, app_mode=None, current_view=None):
        quote_data = view_state.get("quote")

        if not quote_data:
            return

        new_quote = quote_data["quote"]
        new_author = quote_data["author"]

        # Solo actualiza si cambió
        if new_quote != self.current_quote:
            self.current_quote = new_quote
            self.current_author = new_author

            self.label_quote.configure(text=f"“{new_quote}”")
            self.label_author.configure(text=f"— {new_author}")
