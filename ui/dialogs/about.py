import webbrowser

import customtkinter as ctk
from PIL import Image

from utils.paths import resource_path


class AboutWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        # Tamaño y centrado
        ancho = 400
        alto = 700
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2) + 150
        y = (pantalla_alto // 2) - (alto // 2)

        self.title("Acerca de")
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.resizable(False, False)
        self.grab_set()  # Modal


        # ===== Título =====
        ctk.CTkLabel(self, text="Habit Tracker v1.0", font=("Arial", 20, "bold")).pack(
            pady=(20, 5)
        )

        # ===== Autor =====
        ctk.CTkLabel(
            self,
            text="Desarrollado en Python con CustomTkinter",
            font=("Arial", 14),
            justify="center",
        ).pack(pady=(0, 10))

        # ===== Autor =====
        ctk.CTkLabel(
            self,
            text="Desarrollado por:\nEdgar Daniel Molina Gómez a.k.a (El chilakas)",
            font=("Arial", 14),
            justify="center",
        ).pack(pady=(0, 10))

        # ===== Logo =====
        try:
            logo_img = ctk.CTkImage(
                light_image=Image.open(resource_path("sources/chilakas_shorts.png")),
                size=(80, 80),
            )
            ctk.CTkLabel(self, image=logo_img, text="").pack(pady=(0, 10))
        except FileNotFoundError:
            pass

        # ===== Redes sociales =====
        redes_frame = ctk.CTkFrame(self, fg_color="#252525")
        redes_frame.pack(pady=10, padx=20, fill="x")
        ctk.CTkLabel(
            redes_frame, text="📱 Redes Sociales", font=("Arial", 14, "bold")
        ).pack(pady=5)

        redes = [
            (
                "Donar",
                resource_path("sources/icons/paypal.png"),
                "https://www.paypal.com/donate/?hosted_button_id=KT2LZ7N5WGW2C",
            ),
            (
                "GitHub",
                resource_path("sources/icons/github.png"),
                "https://github.com/DanMG20",
            ),
            (
                "Twitch",
                resource_path("sources/icons/twitch.png"),
                "https://www.twitch.tv/elchilakas1",
            ),
            (
                "TikTok",
                resource_path("sources/icons/tiktok.png"),
                "https://www.tiktok.com/@elchilakasof",
            ),
            (
                "Instagram",
                resource_path("sources/icons/instagram.png"),
                "https://www.instagram.com/el_chilakas_oficial/",
            ),
            (
                "YouTube",
                resource_path("sources/icons/youtube.png"),
                "https://www.youtube.com/@elchilakas",
            ),
        ]

        for nombre, icono_path, url in redes:
            try:
                icono = ctk.CTkImage(light_image=Image.open(icono_path), size=(20, 20))
            except FileNotFoundError:
                icono = None

            btn = ctk.CTkButton(
                redes_frame,
                text=nombre,
                image=icono,
                compound="left",
                width=200,
                fg_color="#3A3A3A",
                hover_color="#555555",
                command=lambda link=url: self.abrir_link(link),
            )
            btn.pack(pady=3)

        # ===== Créditos =====
        creditos_frame = ctk.CTkFrame(self, fg_color="#252525")
        creditos_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(
            creditos_frame, text="📜 Créditos", font=("Arial", 14, "bold")
        ).pack(pady=5)

        creditos_texto = "• CTkMenuBar - por Akascape\n" "• CTkThemesPack - por a13xe\n"

        ctk.CTkLabel(
            creditos_frame, text=creditos_texto, font=("Arial", 12), justify="left"
        ).pack(pady=5, padx=10)

        # ===== Botón cerrar =====
        ctk.CTkButton(
            self,
            text="Cerrar",
            fg_color="#444444",
            hover_color="#666666",
            command=self.destroy,
        ).pack(pady=15)

    def abrir_link(self, url):
        webbrowser.open(url)
