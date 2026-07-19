import os
import sys
from pathlib import Path
from typing import Final

# Global configuration constants
APP_NAME: Final[str] = "Habit Tracker"

# Retrieve APPDATA safely, fallback to current user home if environment variable is missing
APPDATA_ENV: Final[str] = os.getenv("APPDATA", str(Path.home()))
APPDATA_DIR: Final[Path] = Path(APPDATA_ENV) / APP_NAME
APPDATA_DIR.mkdir(parents=True, exist_ok=True)


def resource_path(relative_path: str) -> Path:
    """Resolves the absolute path to a resource, supporting development and PyInstaller environments.

    Args:
        relative_path: The relative path string to the target resource.

    Returns:
        A Path object representing the absolute location of the resource.
    """
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        # PyInstaller extraction directory runtime path
        base_path = Path(sys._MEIPASS)
    else:
        # Standard development mode base path (two levels up from this file)
        base_path = Path(__file__).resolve().parent.parent

    return base_path / relative_path


def data_path(relative_path: str) -> Path:
    """Returns a path inside the writable application data directory.

    Used exclusively for dynamic user data such as databases, configurations, and state.

    Args:
        relative_path: The relative path within the app data storage.

    Returns:
        A Path object targeting the user data location.
    """
    return APPDATA_DIR / relative_path


def icon_path() -> Path:
    """Provides the absolute path to the main application icon.

    Returns:
        A Path object pointing to the main icon asset.
    """
    return resource_path("resources/main_icon.ico")


def logo_light_path() -> Path:
    """Provides the absolute path to the light theme logo asset.

    Returns:
        A Path object pointing to the light logo image.
    """
    return resource_path("resources/V2_light.png")


def logo_dark_icon_path() -> Path:
    """Provides the absolute path to the dark theme logo asset.

    Returns:
        A Path object pointing to the dark logo image.
    """
    return resource_path("resources/V2_dark.png")