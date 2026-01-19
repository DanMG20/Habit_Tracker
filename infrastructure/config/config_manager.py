import json 
import os
import customtkinter as ctk

from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)
from utils.paths import obtener_ruta_json,resource_path
from .defaults import(
    DEFAULT_THEME,
    DEFAULT_APPEARENCE_MODE,
    DEFAULT_FONT,
    DEFAULT_THEMES,
    CUSTOM_THEMES,
    APPEARANCE_MODES
)

CONFIG_FILE = obtener_ruta_json("configuracion.json")

def create_default_config(): 
    return ({
            "theme" : DEFAULT_THEME,
            "appearance" : DEFAULT_APPEARENCE_MODE,
            "font" : DEFAULT_FONT
    })

def load_config():

    if not os.path.exists(CONFIG_FILE):
        config = create_default_config()
        save_config(config)
        change_theme(config)
        change_appearance(config)
        return config

    try: 
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            selected_theme = config.get("TEMA_SELECCIONADO", DEFAULT_THEME)
            selected_appearance = config.get("MODO_APARIENCIA", DEFAULT_APPEARENCE_MODE)
            selected_font = config.get("FUENTE")
    except json.JSONDecodeError:
        config = create_default_config()
        save_config(config)
        change_theme(config)
        change_appearance(config)
    return({
        "appearance":selected_appearance,
        "theme":selected_theme,
        "font":selected_font
        }
    )

def save_config(config):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=4, ensure_ascii=False)

def apply_config(config):
        # ✅ Aplicar al GUI después de cargar
    logger.info(f"TIPO CONFIG: {type(config)}")
    if "\\" in config["theme"]: 
        ctk.set_default_color_theme(resource_path(config["theme"]))
        ctk.set_appearance_mode(config["appearance"])
    else:
        ctk.set_default_color_theme(config["theme"])
        ctk.set_appearance_mode(config["appearance"])

    logger.info(f"Configuración aplicada tema:{config['theme']},apariencia: {config['appearance']}")

def change_theme(config, new_theme=None):
    """Guarda el tema y modo de apariencia en el archivo JSON y los aplica."""
    if new_theme in DEFAULT_THEMES:
        selected_theme = new_theme
        ctk.set_default_color_theme(new_theme)
    elif new_theme in CUSTOM_THEMES:
        selected_theme = f"temas\\{new_theme}.json"
        ctk.set_default_color_theme(resource_path(selected_theme))
    elif new_theme == None:
        logger.info(f"Archivo config :{config}")
        selected_theme = DEFAULT_THEME
        
    logger.info(f"Tema seleccionado :{selected_theme}")
    with open(CONFIG_FILE, "w") as f:
        json.dump({
            "TEMA_SELECCIONADO": selected_theme,
            "MODO_APARIENCIA": config["appearance"],
            "FUENTE": config["font"],
        }, f, indent=4)
    
    logger.info("Theme succesfully changed")

def change_appearance(config,new_appearance = None):
    """Guarda el modo de apariencia (dark/light) en el archivo JSON."""
    if new_appearance:
        selected_appearance = new_appearance
        ctk.set_appearance_mode(new_appearance)

        with open(CONFIG_FILE, "w") as f:
            json.dump({
                "TEMA_SELECCIONADO": config["theme"],
                "MODO_APARIENCIA": selected_appearance,
                "FUENTE": config["font"],
            }, f, indent=4)

        logger.info("Appearance succesfully changed")

    elif new_appearance == None: 
        ctk.set_appearance_mode(config["appearance"])


def change_font(config, new_font):
    """Guarda la fuente seleccionada en el archivo JSON."""
    with open(CONFIG_FILE, "w") as f:
        json.dump({
            "TEMA_SELECCIONADO": config["theme"],
            "MODO_APARIENCIA": config["appearance"],
            "FUENTE": new_font,
        }, f, indent=4)

def load_theme_file(config):

    theme_path = config["theme"]

    if "\\" in theme_path:
        ruta = theme_path
        with open(resource_path(ruta), "r") as file:
            theme_file = json.load(file)
    else:
        ruta_tema = os.path.join(
            os.path.dirname(ctk.__file__),
            "assets\\themes",
            f"{theme_path}.json"
    )
        
        with open(resource_path(ruta_tema), "r") as f:
            theme_file = json.load(f)
    return theme_file





    