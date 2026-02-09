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
        logger.info("CURRENT DATA LOADED ON JSON DIR PROYECT")
    return os.path.join(base_path, relative_path)



# ---------------------- RUTAS DE DATOS MODIFICABLES ----------------------
APPDATA_DIR = Path(os.environ["APPDATA"]) / "Habit Tracker"
APPDATA_DIR.mkdir(parents=True, exist_ok=True)


def resource_json_path(file_name: str) -> str:
    """Returns file path for JSON default files"""
    return resource_path(f"resources/{file_name}")
