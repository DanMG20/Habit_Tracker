from infrastructure.config.config_manager import load_config, load_theme_file
from tkinter import ttk
import customtkinter as ctk
class StyleService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_theme_colors()
        return cls._instance
    


    def _load_theme_colors(self):
        config = load_config()
        theme_file = load_theme_file(config)
        return {
            "button": theme_file["CTkButton"]["fg_color"],
            "frame": theme_file["CTkFrame"]["fg_color"],
            "top_frame": theme_file["CTkFrame"]["top_fg_color"],
            "progressbar": theme_file["CTkProgressBar"]["fg_color"],
        }

        

    def build_fonts(self):
        config = load_config()
        font = config["font"]
        # -------------------FUENTES------------------------
        return {
            "TITLE": (font, 40, "bold"),
            "SUBTITLE": (font, 25),
            "SMALL": (font, 15, "bold"),
            "PHRASE": (font, 18),
            "AUTHOR": (font, 14),
        }

    def reload_theme_colors(self):
        self._load_theme_colors()

    def get_font(self):
        config = load_config()
        return config["font"]


