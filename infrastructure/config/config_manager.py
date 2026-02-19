import json
import os

from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


from .defaults import (
    DEFAULT_APPEARENCE_MODE,
    DEFAULT_FONT,
    DEFAULT_THEME,
)



class ConfigManager:

    def __init__(self, config_file: str):
        self._config_file = config_file

    def load(self) -> dict:
        if not os.path.exists(self._config_file):
            config = self._default_config()
            self.save(config)
            return config

        try:
            with open(self._config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            config = self._default_config()
            self.save(config)
            return config

    def save(self, config: dict):
        with open(self._config_file, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)

    def _default_config(self):
        return {
            "theme": DEFAULT_THEME,
            "appearance": DEFAULT_APPEARENCE_MODE,
            "font": DEFAULT_FONT,
        }
