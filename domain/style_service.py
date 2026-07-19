"""
Module providing UI style component generation, font sizing matrices, and color transformations.
"""

from typing import Dict, Any, Tuple
from pathlib import Path


class StyleService:
    """
    Domain service responsible for parsing configurations into layout-ready styling settings.
    """

    # Font sizing constants
    SIZE_TITLE: int = 40
    SIZE_SUBTITLE: int = 25
    SIZE_ICON: int = 30
    SIZE_SMALL: int = 15
    SIZE_PHRASE: int = 18
    SIZE_AUTHOR: int = 14
    SIZE_GIANT: int = 300

    # Color hexadecimal bitwise masks and fallbacks
    DEFAULT_HEX_FALLBACK: int = 0x303030
    HEX_WHITE: int = 0xFFFFFF
    HEX_BLACK: int = 0x000000

    def __init__(self, config: Dict[str, Any], theme_file: Dict[str, Any]) -> None:
        """
        Initializes the StyleService injecting active runtime properties.

        Args:
            config (Dict[str, Any]): General app configuration dataset.
            theme_file (Dict[str, Any]): Loaded CustomTkinter theme definition mapping.
        """
        self._config: Dict[str, Any] = config
        self._theme_file: Dict[str, Any] = theme_file

    def extract_theme_name(self, theme_value: str) -> str:
        """
        Normalizes variations of theme identifiers down to simple names.

        Args:
            theme_value (str): Raw path or name of the target theme.

        Returns:
            str: The clean base name of the theme.
        """
        path = Path(theme_value)
        if path.suffix:
            return path.stem
        return path.name

    def get_style_settings(self) -> Dict[str, Any]:
        """
        Compiles consolidated settings required for rendering UI pipelines.

        Returns:
            Dict[str, Any]: Combined layout presentation metrics.
        """
        return {
            "fonts": self._build_fonts(),
            "colors": self._build_theme_colors(),
            "current_font": self._config.get("font", "Arial"),
            "appearance": self._config.get("appearance", "Dark"),
            "theme": self.extract_theme_name(self._config.get("theme", "blue")),
        }

    def get_font(self) -> str:
        """
        Retrieves the global font family identifier token.

        Returns:
            str: Active font family name.
        """
        return self._config.get("font", "Arial")

    def _build_fonts(self) -> Dict[str, Tuple[Any, ...]]:
        """
        Compiles the font token resolution grid map layout matrix.
        """
        font: str = self._config.get("font", "Arial")

        return {
            "TITLE": (font, self.SIZE_TITLE, "bold"),
            "SUBTITLE": (font, self.SIZE_SUBTITLE),
            "ICON": (font, self.SIZE_ICON),
            "SMALL": (font, self.SIZE_SMALL, "bold"),
            "PHRASE": (font, self.SIZE_PHRASE),
            "AUTHOR": (font, self.SIZE_AUTHOR),
            "GIANT": (font, self.SIZE_GIANT),
        }

    def _build_theme_colors(self) -> Dict[str, Any]:
        """
        Safely extracts interface color guidelines from theme dictionaries.
        """
        btn_cfg: Dict[str, Any] = self._theme_file.get("CTkButton", {})
        frm_cfg: Dict[str, Any] = self._theme_file.get("CTkFrame", {})
        bar_cfg: Dict[str, Any] = self._theme_file.get("CTkProgressBar", {})
        lbl_cfg: Dict[str, Any] = self._theme_file.get("CTkLabel", {})

        frame_color: Any = frm_cfg.get("fg_color")

        return {
            "button": btn_cfg.get("fg_color"),
            "frame": frame_color,
            "top_frame": frm_cfg.get("top_fg_color"),
            "progressbar": bar_cfg.get("fg_color"),
            "title": self._to_windows_hex_color(frame_color),
            "text": lbl_cfg.get("text_color"),
        }

    def _to_windows_hex_color(self, color_value: Any) -> int:
        """
        Transforms CustomTkinter colors into structural integer representations.
        """
        if not color_value:
            return self.DEFAULT_HEX_FALLBACK

        if isinstance(color_value, list):
            appearance: str = self._config.get("appearance", "Dark")
            color_value = color_value[0] if appearance == "Light" else color_value[1]

        if not isinstance(color_value, str):
            return self.DEFAULT_HEX_FALLBACK

        color_value = color_value.strip().lower()

        if color_value.startswith("#"):
            return int(color_value[1:], 16)

        if color_value.startswith("gray"):
            try:
                percentage_str: str = color_value.replace("gray", "")
                percentage: int = int(percentage_str)
                percentage = max(0, min(percentage, 100))
                value: int = int(255 * (percentage / 100))
                return (value << 16) + (value << 8) + value
            except ValueError:
                return self.DEFAULT_HEX_FALLBACK

        if color_value == "white":
            return self.HEX_WHITE
        if color_value == "black":
            return self.HEX_BLACK

        return self.DEFAULT_HEX_FALLBACK