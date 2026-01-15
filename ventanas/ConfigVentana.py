import json
import os
from pathlib import Path
from utils.paths import resource_path

# Carpeta de usuario para archivos modificables
APPDATA_DIR = os.path.join(os.environ['APPDATA'], 'Habit Tracker')
os.makedirs(APPDATA_DIR, exist_ok=True)

# Archivo de posición de ventana en APPDATA
POSICION_VENTANA_FILE = os.path.join(APPDATA_DIR, 'posicion_ventana.json')


def guardar_posicion_ventana(ventana):
    archivo_real = Path(POSICION_VENTANA_FILE)
    archivo_real.parent.mkdir(parents=True, exist_ok=True)

    x = ventana.winfo_x()
    y = ventana.winfo_y()
    datos = {"posicion": {"x": x, "y": y}}

    with archivo_real.open("w") as f:
        json.dump(datos, f)


def cargar_posicion_ventana(ventana):
    archivo_real = Path(POSICION_VENTANA_FILE)

    if archivo_real.exists():
        with archivo_real.open("r") as f:
            datos = json.load(f)
            posicion = datos.get("posicion", {"x": 100, "y": 100})
            ventana.geometry(f"+{posicion['x']}+{posicion['y']}")
    else:
        ventana.update_idletasks()
        screen_width = ventana.winfo_screenwidth()
        screen_height = ventana.winfo_screenheight()
        ventana.geometry(
            f"800x600+{(screen_width - 800) // 2}+{(screen_height - 600) // 2}"
        )
