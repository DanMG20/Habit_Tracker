from pathlib import Path
import sys
import os

# ---------------------- RUTAS DE RECURSOS FIJOS ----------------------
def obtener_direccion_icono():
    """Ruta al icono principal (solo lectura, incluido en la app)."""
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent.parent
    return str(base_path / "resources" / "icono_principal.ico")

def obtener_direccion_icono_top():
    """Ruta al icono secundario (solo lectura, incluido en la app)."""
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).parent
    return str(base_path / "sources" / "icono_principal_copy.ico")

def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, funciona para dev y PyInstaller."""
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ---------------------- RUTAS DE DATOS MODIFICABLES ----------------------
APPDATA_DIR = Path(os.environ['APPDATA']) / "Habit Tracker"
APPDATA_DIR.mkdir(parents=True, exist_ok=True)

def obtener_ruta_json(nombre_archivo):
    """Devuelve la ruta en APPDATA para archivos JSON modificables."""
    return str(APPDATA_DIR / nombre_archivo)

# Ejemplos:
# Base de datos de hábitos: obtener_ruta_json("Base_de_datos_habitos.json")
# Registro de hábitos: obtener_ruta_json("registro_habitos.json")
# Configuración: obtener_ruta_json("configuracion.json")
# Frases: obtener_ruta_json("frases.json")
