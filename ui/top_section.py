import customtkinter as ctk
from PIL import Image

import infrastructure.config.defaults as df
from utils.paths import icon_path


class TopSection(ctk.CTkFrame):
    def __init__(self, master, phrase, author, fonts):
        self.master = master
        self.phrase = phrase
        self.author = author
        self.fonts = fonts

        self._build()

    def _build(self):
        self._draw_title_frame()
        self._draw_icon()
        self._draw_title()
        self._draw_quote_frame()

    def _draw_title_frame(self):
        self.frame_titulo_icono_0_0 = ctk.CTkFrame(
            self.master, corner_radius=df.CORNER_RADIUS
        )
        self.frame_titulo_icono_0_0.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=df.PADX,
            pady=(df.PADY * 2, df.PADY),
        )
        # -----------------------------------------ICONO---------------------------------------------------------------

    def _draw_icon(self):
        img_icono = ctk.CTkImage(
            light_image=Image.open(icon_path()),
            dark_image=Image.open(icon_path()),
            size=(100, 100),
        )

        icono_label = ctk.CTkLabel(
            self.frame_titulo_icono_0_0, image=img_icono, text=""
        )
        icono_label.pack(side="left", fill="x", padx=5, pady=10)

    def _draw_title(self):
        tituloapp_label = ctk.CTkLabel(
            self.frame_titulo_icono_0_0, font=self.fonts["TITLE"], text="HABIT TRACKER"
        )
        tituloapp_label.pack(side="right", fill="x", padx=(0, 30), pady=10)

    def _draw_quote_frame(self):
        self.frame_frase_0_1 = ctk.CTkFrame(self.master, corner_radius=df.CORNER_RADIUS)
        self.frame_frase_0_1.grid(
            row=1,
            column=1,
            columnspan=3,
            sticky="nsew",
            padx=df.PADX,
            pady=(df.PADY * 2, df.PADY),
        )

        self.frame_frase_0_1.grid_rowconfigure(0, weight=1)
        self.frame_frase_0_1.grid_columnconfigure(0, weight=1)
        self._draw_phrase()

    def _draw_phrase(self):
        self.label_frase = ctk.CTkLabel(
            self.frame_frase_0_1,
            text=f"“{self.phrase}”",
            justify="center",
            wraplength=850,  # ajusta el ancho del texto
            font=self.fonts["PHRASE"],
        )
        self.label_frase.grid(row=0, column=0, padx=28, pady=(16, 2), sticky="n")

        self.label_autor = ctk.CTkLabel(
            self.frame_frase_0_1,
            text=f"— {self.author}",
            font=self.fonts["AUTHOR"],
            text_color=df.COLOR_AUTOR,
        )
        self.label_autor.grid(row=1, column=0, padx=18, pady=(0, 16), sticky="n")
