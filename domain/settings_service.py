import os
import customtkinter as ctk
from infrastructure.config.config_manager import ConfigManager
from utils.paths import resource_path

DEFAULT_THEMES = {"blue", "dark-blue", "green"}


class SettingsService:

    def __init__(self, config_manager: ConfigManager):
        self._config_manager = config_manager
        self._config = self._config_manager.load()

    # ==========================
    # GETTERS
    # ==========================

    def get_config(self):
        return self._config

    # ==========================
    # APPLY (🔥 aquí se aplica CTK)
    # ==========================

    def apply(self):
        """
        Aplica tema y apariencia actuales.
        Llamar esto al iniciar la app.
        """
        theme = self._config["theme"]
        appearance = self._config["appearance"]

        # Aplicar appearance primero
        ctk.set_appearance_mode(appearance)

        # Aplicar theme
        if theme in DEFAULT_THEMES:
            ctk.set_default_color_theme(theme)
        else:
            theme_path = resource_path(
                os.path.join("resources", "themes", f"{theme}.json")
            )
            ctk.set_default_color_theme(theme_path)

    # ==========================
    # UPDATE METHODS
    # ==========================

    def update_theme(self, new_theme: str):
        self._config["theme"] = new_theme
        self._config_manager.save(self._config)

        # Aplicar inmediatamente
        self.apply()

    def update_appearance(self, new_appearance: str):
        self._config["appearance"] = new_appearance
        self._config_manager.save(self._config)

        ctk.set_appearance_mode(new_appearance)

    def update_font(self, new_font: str):
        self._config["font"] = new_font
        self._config_manager.save(self._config)
