"""Module responsible for locating and loading UI theme configurations."""

import json
from pathlib import Path
from typing import Any, Dict, Final, Set
import customtkinter as ctk
from infrastructure.logging.logger import get_logger
from utils.paths import resource_path

logger = get_logger(__name__)

# Built-in CustomTkinter themes
DEFAULT_THEMES: Final[Set[str]] = {"blue", "dark-blue", "green"}


def load_theme_file(config: Dict[str, Any]) -> Dict[str, Any]:
    """Loads and parses the JSON theme configuration file based on app settings.

    Args:
        config: Dictionary containing application configuration settings,
            expected to have a "theme" key.

    Returns:
        A dictionary containing the parsed theme JSON attributes, or an empty
        dictionary if the file fails to load.
    """
    theme_name: str = config.get("theme", "blue")
    theme_path: Path = _resolve_theme_path(theme_name)

    if not theme_path.exists():
        logger.error(f"Theme file does not exist at path: {theme_path}")
        return {}

    try:
        with theme_path.open("r", encoding="utf-8") as file:
            theme_data: Any = json.load(file)
            if isinstance(theme_data, dict):
                return theme_data
            logger.error(f"Theme file content at {theme_path} is not a valid JSON object.")
            return {}
    except (OSError, json.JSONDecodeError) as error:
        logger.error(f"Failed to read or parse theme file: {theme_path}", exc_info=error)
        return {}


def _resolve_theme_path(theme_name: str) -> Path:
    """Resolves the absolute file system path for a given theme name.

    Args:
        theme_name: The target theme identifier string.

    Returns:
        A Path object pointing to the target theme JSON location.
    """
    if theme_name in DEFAULT_THEMES:
        ctk_base_dir = Path(ctk.__file__).resolve().parent
        return ctk_base_dir / "assets" / "themes" / f"{theme_name}.json"

    relative_resource = Path("resources") / "themes" / f"{theme_name}.json"
    return resource_path(str(relative_resource))