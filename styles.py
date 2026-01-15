import json
import os
import customtkinter as ctk
from utils.paths import resource_path
from pathlib import Path
import shutil

#------------------CONFIGURACIÓN------------------
# Carpeta de usuario para archivos modificables
APPDATA_DIR = os.path.join(os.environ['APPDATA'], 'Habit Tracker')
os.makedirs(APPDATA_DIR, exist_ok=True)

# Archivo de configuración
configuracion_file = os.path.join(APPDATA_DIR, 'configuracion.json')

# Valores por defecto
config_por_defecto = {
    "TEMA_SELECCIONADO": "blue",
    "MODO_APARIENCIA": "dark",
    "FUENTE": "Comic Sans MS"
}

# Copiar archivo por defecto desde _internal si no existe
def copiar_config_por_defecto():
    if not os.path.exists(configuracion_file):
        internal_config = resource_path('json/configuracion.json')
        if os.path.exists(internal_config):
            shutil.copy(internal_config, configuracion_file)
        else:
            with open(configuracion_file, 'w') as f:
                json.dump(config_por_defecto, f, indent=4)
                print("configuracion.json creado con valores por defecto.")

copiar_config_por_defecto()

# Cargar configuración
with open(configuracion_file, 'r') as f:
    data = json.load(f)
    tema_ruta = data["TEMA_SELECCIONADO"]
    FUENTE_PRINCIPAL = data["FUENTE"]

#------------------TEMA---------------------------
# Cargar tema
if "\\" in tema_ruta:
    ruta = tema_ruta
    with open(resource_path(ruta), "r") as file:
        tema_data = json.load(file)
else:
    ruta_tema = os.path.join(
        os.path.dirname(ctk.__file__),
        "assets\\themes",
        f"{tema_ruta}.json"
    )
    with open(resource_path(ruta_tema), "r") as f:
        tema_data = json.load(f)

# Extraer colores del tema
tema_botones_color = tema_data["CTkButton"]["fg_color"]
tema_frame_color = tema_data["CTkFrame"]["fg_color"]
tema_top_frame_color = tema_data["CTkFrame"]["top_fg_color"]
tema_progressbar_fondo = tema_data["CTkProgressBar"]["fg_color"]

#-------------------FUENTES------------------------
FUENTE_TITULO = (FUENTE_PRINCIPAL, 40, "bold")
FUENTE_SUBTITULOS = (FUENTE_PRINCIPAL, 25)
FUENTE_PEQUEÑA = (FUENTE_PRINCIPAL, 15, "bold")
FUENTE_FRASE = (FUENTE_PRINCIPAL, 18)
FUENTE_AUTOR = (FUENTE_PRINCIPAL, 14)

#-------------------PADINGS------------------------
PADX = 5
PADY = 5
CORNER_RADIUS = 5

#---------------------TEMAS------------------------
FONDOS = ["light", "dark", "system"]
TEMAS_PERSONALIZADOS = [
    "autumn", "breeze", "carrot", "cherry", "coffee", "lavender", "marsh",
    "metal", "midnight", "orange", "patina", "pink", "red", "rime", "rose",
    "sky", "violet"
]
TEMAS_COLOR_DEFAULT = ["dark-blue", "green", "blue"]

#-------------------COLORES------------------------
COLOR_AUTOR = ("gray20", "gray70")
COLOR_BARRA_PRINCIPAL = "#303030"
COLOR_CONTRASTE = "#0fa987"
COLOR_FRENTE = "#333333"
COLOR_FONDO = "#2b2b2b"
COLOR_BORDE = "#D1D1D1"

COLORES = [
    "#B23A48",  # Rojo mate
    "#3B6BA5",  # Azul mate
    "#4F8A77",  # Verde mate
    "#CC7722",  # Naranja quemado
    "#7E5A9B"   # Morado suave
]
