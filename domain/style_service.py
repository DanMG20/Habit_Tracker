from typing import Dict, Any
from pathlib import Path



class StyleService:
    """
    Servicio encargado de construir configuraciones visuales
    (fuentes, colores y estado actual de tema).

    No depende de infrastructure.
    No carga archivos.
    Solo trabaja con datos ya cargados.
    """

    def __init__(self, config: Dict[str, Any], theme_file: Dict[str, Any]):
        self._config = config
        self._theme_file = theme_file

    def extract_theme_name(self,theme_value: str) -> str:
        """
        Normaliza el valor del tema y devuelve solo el nombre.
        
        Ejemplos:
            "marsh" -> "marsh"
            "temas\\marsh.json" -> "marsh"
            "themes/marsh.json" -> "marsh"
        """
        path = Path(theme_value)

        # Si tiene extensión (.json), quitarla
        if path.suffix:
            return path.stem

        # Si no tiene extensión, asumir que ya es el nombre
        return path.name


    def get_style_settings(self) -> Dict[str, Any]:
        """
        Devuelve todas las configuraciones necesarias
        para que la UI renderice correctamente.
        """
        return {
            "fonts": self._build_fonts(),
            "colors": self._build_theme_colors(),
            "current_font": self._config["font"],
            "appearance": self._config["appearance"],
            "theme": self.extract_theme_name(self._config["theme"]),
        }

    def get_font(self) -> str:
        return self._config["font"]

    # ==============================
    # PRIVATE BUILDERS
    # ==============================

    def _build_fonts(self) -> Dict[str, tuple]:
        font = self._config["font"]

        return {
            "TITLE": (font, 40, "bold"),
            "SUBTITLE": (font, 25),
            "ICON": (font,30),
            "SMALL": (font, 15, "bold"),
            "PHRASE": (font, 18),
            "AUTHOR": (font, 14),
        }

    def _build_theme_colors(self) -> Dict[str, Any]:
        return {
            "button": self._theme_file["CTkButton"]["fg_color"],
            "frame": self._theme_file["CTkFrame"]["fg_color"],
            "top_frame": self._theme_file["CTkFrame"].get("top_fg_color"),
            "progressbar": self._theme_file["CTkProgressBar"]["fg_color"],
            "title": self._to_windows_hex_color(self._theme_file["CTkFrame"]["fg_color"]),
            "text": self._theme_file["CTkLabel"]["text_color"],
        }

    def _to_windows_hex_color(self, color_value: Any) -> int:
        if not color_value:
            return 0x303030

        # Si viene como lista [light, dark]
        if isinstance(color_value, list):
            appearance = self._config["appearance"]
            color_value = color_value[0] if appearance == "Light" else color_value[1]

        if not isinstance(color_value, str):
            return 0x303030

        color_value = color_value.strip().lower()

        # Caso 1: Hex
        if color_value.startswith("#"):
            return int(color_value[1:], 16)

        # Caso 2: grayXX
        if color_value.startswith("gray"):
            try:
                percentage = int(color_value.replace("gray", ""))
                percentage = max(0, min(percentage, 100))
                value = int(255 * (percentage / 100))
                return (value << 16) + (value << 8) + value
            except ValueError:
                return 0x303030

        # Caso 3: white / black básicos
        if color_value == "white":
            return 0xFFFFFF
        if color_value == "black":
            return 0x000000

        # Fallback
        return 0x303030
