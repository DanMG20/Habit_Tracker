import os
import sys
from pathlib import Path
from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)
# ---------------------- RUTAS DE RECURSOS FIJOS ----------------------
def icon_path() -> str:
    """Ruta al icono principal (solo lectura, incluido en la app)."""       
    return resource_path( "resources/icono_principal.ico")


def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, funciona para dev y PyInstaller."""
    if getattr(sys, "frozen", False):
        base_path = sys._MEIPASS
        logger.info("CURRENT DATA LOADED ON APP DATA ")
    else:
        base_path = Path(__file__).parent.parent
  
    return os.path.join(base_path, relative_path)


def get_default_settings_file():
    return resource_path("resources\\json\\default_settings.json")