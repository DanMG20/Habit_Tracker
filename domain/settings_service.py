"""
Module providing settings management and direct CustomTkinter appearance applications.
"""

import os
import customtkinter as ctk
from typing import Dict, Any, Set
from infrastructure.config.config_manager import ConfigManager
from utils.paths import resource_path

DEFAULT_THEMES: Set[str] = {"blue", "dark-blue", "green"}


class SettingsService:
    """
    Service responsible for managing configuration states and applying UI visual styles.
    """

    def __init__(self, config_manager: ConfigManager) -> None:
        """
        Initializes the SettingsService with a concrete configuration manager.

        Args:
            config_manager (ConfigManager): The manager handler to load and save settings.
        """
        self._config_manager: ConfigManager = config_manager
        self._config: Dict[str, Any] = self._config_manager.load()

    def get_config(self) -> Dict[str, Any]:
        return self._config

    def apply(self) -> None:
        theme: str = self._config["theme"]
        appearance: str = self._config["appearance"]

        ctk.set_appearance_mode(appearance)

        if theme in DEFAULT_THEMES:
            ctk.set_default_color_theme(theme)
        else:
            theme_path: str = resource_path(f"resources/themes/{theme}.json")
            ctk.set_default_color_theme(theme_path)

    def update_theme(self, new_theme: str) -> None:
        self._config["theme"] = new_theme
        self._config_manager.save(self._config)
        self.apply()

    def update_appearance(self, new_appearance: str) -> None:
        self._config["appearance"] = new_appearance
        self._config_manager.save(self._config)
        ctk.set_appearance_mode(new_appearance)

    def update_font(self, new_font: str) -> None:
        self._config["font"] = new_font
        self._config_manager.save(self._config)