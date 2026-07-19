"""Module responsible for managing application configuration persistence and defaults."""

import json
from pathlib import Path
from typing import Any, Dict, Union

from infrastructure.logging.logger import get_logger
from .defaults import (
    DEFAULT_APPEARANCE_MODE,
    DEFAULT_FONT_FAMILY,
    DEFAULT_THEME,
)

logger = get_logger(__name__)


class ConfigManager:
    """Manages the loading, persisting, and defaulting of application configuration settings."""

    def __init__(self, config_file: Union[str, Path]) -> None:
        """Initializes the ConfigManager with a specified target configuration file path.

        Args:
            config_file: The file path pointing to the JSON configuration file.
        """
        self._config_file: Path = Path(config_file)

    def load(self) -> Dict[str, Any]:
        """Loads configuration options from disk, falling back to defaults if unreadable.

        Returns:
            A dictionary containing active application configuration parameters.
        """
        if not self._config_file.exists():
            logger.info("Configuration file not found. Initializing defaults.")
            default_config: Dict[str, Any] = self._get_default_config()
            self.save(default_config)
            return default_config

        try:
            with self._config_file.open("r", encoding="utf-8") as file:
                config_data: Any = json.load(file)
                if isinstance(config_data, dict):
                    return config_data
                
                logger.warning("Configuration file layout is invalid. Reverting to defaults.")
                
        except (OSError, json.JSONDecodeError) as error:
            logger.error(
                "Failed to read or parse configuration file. Overwriting with defaults.",
                exc_info=error,
            )

        fallback_config: Dict[str, Any] = self._get_default_config()
        self.save(fallback_config)
        return fallback_config

    def save(self, config: Dict[str, Any]) -> None:
        """Persists the provided configuration dictionary to disk as JSON.

        Args:
            config: A dictionary representing the configuration key-value state.
        """
        try:
            self._config_file.parent.mkdir(parents=True, exist_ok=True)
            with self._config_file.open("w", encoding="utf-8") as file:
                json.dump(config, file, indent=4, ensure_ascii=False)
        except OSError as error:
            logger.error("Failed to persist configuration file to disk.", exc_info=error)

    def _get_default_config(self) -> Dict[str, Any]:
        """Generates the initial fallback configuration structure.

        Returns:
            A dictionary containing default theme and typography settings.
        """
        return {
            "theme": DEFAULT_THEME,
            "appearance": DEFAULT_APPEARANCE_MODE,
            "font": DEFAULT_FONT_FAMILY,
        }