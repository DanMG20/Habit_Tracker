import webbrowser
import customtkinter as ctk
from PIL import Image
from .windows.base_window import BaseModalWindow
from utils.paths import resource_path


class AboutWindow(BaseModalWindow):

    WIDTH = 400
    HEIGHT = 800

    SOCIAL_LINKS = [
        ("Donar", "resources/icons/paypal.png",
         "https://www.paypal.com/donate/?hosted_button_id=KT2LZ7N5WGW2C"),
        ("GitHub", "resources/icons/github.png",
         "https://github.com/DanMG20"),
        ("Twitch", "resources/icons/twitch.png",
         "https://www.twitch.tv/elchilakas1"),
        ("TikTok", "resources/icons/tiktok.png",
         "https://www.tiktok.com/@elchilakasof"),
        ("Instagram", "resources/icons/instagram.png",
         "https://www.instagram.com/el_chilakas_oficial/"),
        ("YouTube", "resources/icons/youtube.png",
         "https://www.youtube.com/@elchilakas"),
    ]

    def __init__(self, master, styles, version):
        super().__init__(
            master=master,
            width=self.WIDTH,
            height=self.HEIGHT,
            title="Acerca de",
            styles=styles
        )

        self.version = version
        self.fonts = styles["fonts"]

        self._build()


    # =========================================================
    # BUILD
    # =========================================================

    def _build(self):
        self._draw_header_info()
        self._draw_logo()
        self._draw_social_section()
        self._draw_credits_section()
        self._draw_close_button()


    # =========================================================
    # HEADER INFO
    # =========================================================

    def _draw_header_info(self):

        ctk.CTkLabel(
            self.body,
            text=f"Habit Tracker v{self.version}",
            font=self.fonts["SUBTITLE"]
        ).pack(pady=(20, 5))

        ctk.CTkLabel(
            self.body,
            text="Desarrollado en Python con CustomTkinter",
            font=self.fonts["SMALL"],
            justify="center",
        ).pack(pady=(0, 10))

        ctk.CTkLabel(
            self.body,
            text="Desarrollado por:\nEdgar Daniel Molina Gómez a.k.a (El chilakas)",
            font=self.fonts["SMALL"],
            justify="center",
        ).pack(pady=(0, 10))


    # =========================================================
    # LOGO
    # =========================================================

    def _draw_logo(self):
        try:
            logo = ctk.CTkImage(
                light_image=Image.open(
                    resource_path("resources/chilakas_shorts.png")
                ),
                size=(80, 80),
            )
            ctk.CTkLabel(self.body, image=logo, text="").pack(pady=(0, 10))
        except FileNotFoundError:
            pass


    # =========================================================
    # SOCIAL SECTION
    # =========================================================

    def _draw_social_section(self):

        frame = ctk.CTkFrame(self.body, fg_color=self.colors["top_frame"])
        frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            frame,
            text="📱 Redes Sociales",
            font=self.fonts["SMALL"],
        ).pack(pady=5)

        for name, icon_path, url in self.SOCIAL_LINKS:
            icon = self._load_icon(icon_path)

            ctk.CTkButton(
                frame,
                text=name,
                image=icon,
                compound="left",
                font=self.fonts["SMALL"],
                fg_color= self.colors["top_frame"],
                width=200,
                command=lambda link=url: self._open_link(link),
            ).pack(pady=3)

        ctk.CTkLabel(
            frame,
            text="",
            font=self.fonts["SMALL"],
        ).pack(pady=5)


    # =========================================================
    # CREDITS
    # =========================================================

    def _draw_credits_section(self):

        frame = ctk.CTkFrame(self.body,fg_color=self.colors["top_frame"])
        frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            frame,
            text="📜 Créditos",
            font=self.fonts["SMALL"],
        ).pack(pady=5)

        credits_text = (
            "• CTkMenuBar - por Akascape\n"
            "• CTkThemesPack - por a13xe\n"
        )

        ctk.CTkLabel(
            frame,
            text=credits_text,
            justify="left",
            font=self.fonts["SMALL"]
        ).pack(pady=5, padx=10)


    # =========================================================
    # CLOSE BUTTON
    # =========================================================

    def _draw_close_button(self):

        ctk.CTkButton(
            self.body,
            text="Cerrar",
            height=15,
            font=self.fonts["SMALL"],
            fg_color= self.colors["top_frame"],
            command=self.destroy,
        ).pack(pady=15)


    # =========================================================
    # HELPERS
    # =========================================================

    def _load_icon(self, path):
        try:
            return ctk.CTkImage(
                light_image=Image.open(resource_path(path)),
                size=(20, 20)
            )
        except FileNotFoundError:
            return None


    def _open_link(self, url):
        webbrowser.open(url)
