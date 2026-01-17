import json 
import os
from .defaults import(
    DEFAULT_THEME,
    DEFAULT_APPEARENCE_MODE,
    DEFAULT_FONT,
)


def cargar_configuracion(self):

    if not os.path.exists(self.CONFIG_FILE):
        self.TEMA_SELECCIONADO = DEFAULT_THEME
        self.MODO_APARIENCIA = DEFAULT_APPEARENCE_MODE
        self.guardar_configuracion_tema(DEFAULT_THEME)
        self.guardar_configuracion_fondo(DEFAULT_APPEARENCE_MODE)
    else:
        with open(self.CONFIG_FILE, "r") as f:
            config = json.load(f)
            self.TEMA_SELECCIONADO = config.get("TEMA_SELECCIONADO", DEFAULT_THEME)
            self.MODO_APARIENCIA = config.get("MODO_APARIENCIA", DEFAULT_APPEARENCE_MODE)

    # ✅ Aplicar al GUI después de cargar
    if "\\" in self.TEMA_SELECCIONADO: 
        ctk.set_default_color_theme(resource_path(self.TEMA_SELECCIONADO))
        ctk.set_appearance_mode(self.MODO_APARIENCIA)
    else:
        ctk.set_default_color_theme(self.TEMA_SELECCIONADO)
        ctk.set_appearance_mode(self.MODO_APARIENCIA)

def guardar_configuracion_tema(self, nuevo_tema=None):
    """Guarda el tema y modo de apariencia en el archivo JSON y los aplica."""
    if nuevo_tema in styles.TEMAS_COLOR_DEFAULT:
        self.TEMA_SELECCIONADO = nuevo_tema
        ctk.set_default_color_theme(nuevo_tema)
    elif nuevo_tema in styles.TEMAS_PERSONALIZADOS:
        self.TEMA_SELECCIONADO = f"temas\\{nuevo_tema}.json"
        ctk.set_default_color_theme(resource_path(self.TEMA_SELECCIONADO))

    with open(self.CONFIG_FILE, "w") as f:
        json.dump({
            "TEMA_SELECCIONADO": self.TEMA_SELECCIONADO,
            "MODO_APARIENCIA": self.MODO_APARIENCIA,
            "FUENTE": styles.FUENTE_PRINCIPAL,
        }, f, indent=4)

def guardar_configuracion_fondo(self, nuevo_modo):
    """Guarda el modo de apariencia (dark/light) en el archivo JSON."""
    if nuevo_modo:
        self.MODO_APARIENCIA = nuevo_modo
        ctk.set_appearance_mode(nuevo_modo)

    with open(self.CONFIG_FILE, "w") as f:
        json.dump({
            "TEMA_SELECCIONADO": self.TEMA_SELECCIONADO,
            "MODO_APARIENCIA": self.MODO_APARIENCIA,
            "FUENTE": styles.FUENTE_PRINCIPAL,
        }, f, indent=4)

def guardar_configuracion_fuente(self, nueva_fuente):
    """Guarda la fuente seleccionada en el archivo JSON."""
    with open(self.CONFIG_FILE, "w") as f:
        json.dump({
            "TEMA_SELECCIONADO": self.TEMA_SELECCIONADO,
            "MODO_APARIENCIA": self.MODO_APARIENCIA,
            "FUENTE": nueva_fuente,
        }, f, indent=4)