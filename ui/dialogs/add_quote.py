import json
import os
import shutil

import customtkinter as ctk

from domain.style_service import StyleService
from infrastructure.logging.logger import get_logger
from utils.paths import resource_path

logger = get_logger(__name__)

# Carpeta de usuario para archivos modificables
APPDATA_DIR = os.path.join(os.environ["APPDATA"], "Habit Tracker")
os.makedirs(APPDATA_DIR, exist_ok=True)

# Ruta del archivo de frases
FRASES_FILE = os.path.join(APPDATA_DIR, "frases.json")


# Copiar archivo por defecto desde _internal si no existe
def copiar_frases_por_defecto():
    if not os.path.exists(FRASES_FILE):
        internal_frases = resource_path("json/frases.json")
        if os.path.exists(internal_frases):
            shutil.copy(internal_frases, FRASES_FILE)
        else:
            # Crear archivo con frase por defecto
            frase_default = [
                {
                    "frase": "Somos lo que hacemos repetidamente. La excelencia, entonces, no es un acto, sino un hábito.",
                    "autor": "Aristóteles",
                    "indice": 1,
                }
            ]
            with open(FRASES_FILE, "w") as f:
                json.dump(frase_default, f, indent=4)


copiar_frases_por_defecto()


class AddQuoteWindow(ctk.CTkToplevel):
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.load_style_settings()
        self.crear_ventana_crear_frase()

    def load_style_settings(self):
        style_service = StyleService()
        self.theme_colors = style_service._load_theme_colors()
        self.fonts = style_service.build_fonts()

    def crear_ventana_crear_frase(self):
        self.grab_set()
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        ancho = 500
        alto = 250
        x = (pantalla_ancho // 2) - (ancho // 2) + 143
        y = (pantalla_alto // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.title("Agregar nueva frase")

        ctk.CTkLabel(self, font=self.fonts["SMALL"], text="Frase:").pack(pady=(10, 0))
        self.entry_frase = ctk.CTkEntry(self, font=self.fonts["SMALL"], width=350)
        self.entry_frase.pack(pady=5)

        ctk.CTkLabel(self, font=self.fonts["SMALL"], text="Autor:").pack(pady=(10, 0))
        self.entry_autor = ctk.CTkEntry(self, width=350)
        self.entry_autor.pack(pady=5)

        self.label_error = ctk.CTkLabel(
            self, text="", font=self.fonts["SMALL"], text_color="red"
        )
        self.label_error.pack(pady=5)

        btn_guardar = ctk.CTkButton(
            self,
            text="Guardar frase",
            font=self.fonts["SMALL"],
            command=self.guardar_frase,
        )
        btn_guardar.pack(pady=10)
        self.update_idletasks()

    def guardar_frase(self):
        frase_texto = self.entry_frase.get().strip()
        autor_texto = self.entry_autor.get().strip()

        if not frase_texto or not autor_texto:
            self.label_error.configure(text="Ambos campos son obligatorios")
            return

        # Cargar frases existentes
        if os.path.exists(FRASES_FILE):
            with open(FRASES_FILE, "r") as f:
                frases = json.load(f)
        else:
            frases = []

        # Asignar índice secuencial
        if frases:
            ultimo_indice = max(f.get("indice", 0) for f in frases)
        else:
            ultimo_indice = 0
        nuevo_indice = ultimo_indice + 1

        # Crear nuevo objeto frase
        nueva_frase = {
            "frase": frase_texto,
            "autor": autor_texto,
            "indice": nuevo_indice,
        }

        frases.append(nueva_frase)

        # Guardar en JSON
        with open(FRASES_FILE, "w") as f:
            json.dump(frases, f, indent=4)

        self.destroy()  # Cerrar ventana
        self.controller.load_phrase()
        self.master.generar_menu_frases()
        logger.info("New phrase addded successfully")
