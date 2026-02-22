import json
from pathlib import Path
from utils.paths import data_path
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

WINDOW_POSITION_FILE: Path = data_path("window_position.json")

DEFAULT_WIDTH = 800
DEFAULT_HEIGHT = 600
DEFAULT_POSITION = {"x": 100, "y": 100}




def save_window_position(window) -> None:
    """Persist current window position."""
    WINDOW_POSITION_FILE.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "position": {
            "x": window.winfo_x(),
            "y": window.winfo_y(),
        }
    }

    try:
        with WINDOW_POSITION_FILE.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error("Failed to save window position", exc_info=e)


def load_window_position(window) -> None:
    """Load saved window position or center window."""
    position = _read_saved_position()

    if position:
        window.geometry(f"+{position['x']}+{position['y']}")
    else:
        _center_window(window)

def _read_saved_position() -> dict | None:
    if not WINDOW_POSITION_FILE.exists():
        return None

    try:
        with WINDOW_POSITION_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("position")
    except Exception as e:
        logger.warning("Invalid window position file. Using default.", exc_info=e)
        return None
    

def _center_window(window) -> None:
    window.update_idletasks()

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - DEFAULT_WIDTH) // 2
    y = (screen_height - DEFAULT_HEIGHT) // 2

    window.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}+{x}+{y}")

