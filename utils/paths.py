import os
import sys
from pathlib import Path
# ---------------------- RUTAS DE RECURSOS FIJOS ----------------------


APP_NAME = "Habit Tracker"
APPDATA_DIR = Path(os.getenv("APPDATA")) / APP_NAME
APPDATA_DIR.mkdir(parents=True, exist_ok=True)

def icon_path() -> str:
    """Ruta al icono principal (solo lectura, incluido en la app)."""       
    return resource_path( "resources/main_icon.ico")

def logo__light_path() -> str:
    """Ruta al icono principal (solo lectura, incluido en la app)."""       
    return resource_path( "resources/V2_light.png")

def logo_dark_icon_path() -> str:
    """Ruta al icono principal (solo lectura, incluido en la app)."""       
    return resource_path( "resources/V2_dark.png")


def data_path(relative_path: str) -> Path:
    """
    Returns a path inside the application data directory.
    Used for user data (config, DB, window position, etc).
    """
    return APPDATA_DIR / relative_path



def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, funciona para dev y PyInstaller."""
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = Path(__file__).parent.parent
  
    return os.path.join(base_path, relative_path)
