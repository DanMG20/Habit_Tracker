import json
import os
import customtkinter as ctk
from utils.paths import resource_path

from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)



DEFAULT_THEMES = {"blue", "dark-blue", "green"}


def load_theme_file(config: dict) -> dict:
    theme_name = config["theme"]

    if theme_name in DEFAULT_THEMES:
        theme_path = os.path.join(
            os.path.dirname(ctk.__file__),
            "assets",
            "themes",
            f"{theme_name}.json"
        )
        logger.info(theme_path)
        with open(theme_path, "r", encoding="utf-8") as f:
            return json.load(f)

    theme_path = resource_path(
        os.path.join("resources", "themes", f"{theme_name}.json")
    )
    logger.info(theme_path)
    with open(theme_path, "r", encoding="utf-8") as f:
        return json.load(f)
