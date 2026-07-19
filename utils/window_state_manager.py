"""Module responsible for persisting and restoring UI window state configuration."""

import json
from pathlib import Path
from typing import Any, Dict, Final, Optional
import customtkinter as ctk
from infrastructure.logging.logger import get_logger
from utils.paths import data_path

logger = get_logger(__name__)

# File System and Window Geometry Constants
WINDOW_POSITION_FILE: Final[Path] = data_path("window_position.json")
DEFAULT_WIDTH: Final[int] = 800
DEFAULT_HEIGHT: Final[int] = 600
DEFAULT_X: Final[int] = 100
DEFAULT_Y: Final[int] = 100


class WindowStateManager:
    """Manages the persistence, calculation, and restoration of the application window geometry."""

    def __init__(self, window: ctk.CTk) -> None:
        """Initializes the manager linked to a specific CustomTkinter window instance.

        Args:
            window: The target CustomTkinter window instance to manage.
        """
        self._window: ctk.CTk = window

    def save_state(self) -> None:
        """Persists the current window dimensions and position coordinates to disk."""
        try:
            WINDOW_POSITION_FILE.parent.mkdir(parents=True, exist_ok=True)

            payload: Dict[str, Any] = {
                "width": self._window.winfo_width(),
                "height": self._window.winfo_height(),
                "position": {
                    "x": self._window.winfo_x(),
                    "y": self._window.winfo_y(),
                },
            }

            with WINDOW_POSITION_FILE.open("w", encoding="utf-8") as file:
                json.dump(payload, file, indent=4)
                
        except (OSError, TypeError) as error:
            logger.error("Failed to save window layout configuration.", exc_info=error)

    def load_state(self) -> None:
        """Loads the archived geometry state or falls back to centering the window."""
        state: Optional[Dict[str, Any]] = self._read_saved_state()

        if state and "position" in state:
            width: int = state.get("width", DEFAULT_WIDTH)
            height: int = state.get("height", DEFAULT_HEIGHT)
            pos_x: int = state["position"].get("x", DEFAULT_X)
            pos_y: int = state["position"].get("y", DEFAULT_Y)
            
            self._window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        else:
            self.center_window()

    def center_window(self) -> None:
        """Centers the linked window on the user's primary desktop monitor screen."""
        self._window.update_idletasks()

        screen_width: int = self._window.winfo_screenwidth()
        screen_height: int = self._window.winfo_screenheight()

        pos_x: int = (screen_width - DEFAULT_WIDTH) // 2
        pos_y: int = (screen_height - DEFAULT_HEIGHT) // 2

        self._window.geometry(f"{DEFAULT_WIDTH}x{DEFAULT_HEIGHT}+{pos_x}+{pos_y}")

    def _read_saved_state(self) -> Optional[Dict[str, Any]]:
        """Reads and parses the geometry state file from the storage directory.

        Returns:
            A dictionary containing the parsed layout state, or None if reading fails.
        """
        if not WINDOW_POSITION_FILE.exists():
            return None

        try:
            with WINDOW_POSITION_FILE.open("r", encoding="utf-8") as file:
                data: Any = json.load(file)
                if isinstance(data, dict):
                    return data
            return None
        except (OSError, json.JSONDecodeError) as error:
            logger.warning(
                "Invalid or corrupted window position file. Reverting to default geometry.",
                exc_info=error
            )
            return None