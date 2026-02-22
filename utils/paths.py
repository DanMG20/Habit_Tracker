import os
import sys
from pathlib import Path
import json
from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)
# ---------------------- RUTAS DE RECURSOS FIJOS ----------------------


def icon_path() -> str:
    """Ruta al icono principal (solo lectura, incluido en la app)."""       
    return resource_path( "resources/icono.ico")

def logo__light_path() -> str:
    """Ruta al icono principal (solo lectura, incluido en la app)."""       
    return resource_path( "resources/V2_light.png")

def logo_dark_icon_path() -> str:
    """Ruta al icono principal (solo lectura, incluido en la app)."""       
    return resource_path( "resources/V2_dark.png")


def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, funciona para dev y PyInstaller."""
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
    else:
        base_path = Path(__file__).parent.parent
  
    return os.path.join(base_path, relative_path)



def load_theme_file(config: dict) -> dict:
    theme_path = config["theme"]

    if theme_path.endswith(".json"):
        with open(resource_path(theme_path), "r", encoding="utf-8") as f:
            return json.load(f)

    ruta_tema = os.path.join(
        os.path.dirname(ctk.__file__),
        "assets",
        "themes",
        f"{theme_path}.json"
    )

    with open(ruta_tema, "r", encoding="utf-8") as f:
        return json.load(f)