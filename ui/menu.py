from CTkMenuBarPlus import CTkTitleMenu, CustomDropdownMenu
from infrastructure.config import defaults as df
import customtkinter as ctk
from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)

class MenuBar(CTkTitleMenu):
    def __init__(self, 
                 master,
                 actions,
                 styles
                 ):
        super().__init__(master=master)
        self.actions = actions 
        self.styles = styles
        self.appearance = styles["appearance"]
        self.theme = styles["theme"]

        self.dropdown = None
        self.build()
        
        

    def build(self):
        self.build_menu_bar()
        self.build_theme_submenu()

    def build_menu_bar(self):
        self.button_1 = self.add_cascade("Tema")
        self.add_cascade("Fuente", command=self.actions.open_font)
        self.add_cascade("Restaurar", command=self.actions.reset_files)
        self.add_cascade("Frases", postcommand=self.actions.open_add_quote)
        self.add_cascade("Objetivos", postcommand=self.actions.open_add_goal)
        self.add_cascade("Acerca de", command=self.actions.open_about)

    def build_theme_submenu(self):


        # Si ya existe, destruirlo
        if self.dropdown:
            self.dropdown.destroy()

        self.dropdown = CustomDropdownMenu(widget=self.button_1)

        submenu_1 = self.dropdown.add_submenu("Apariencia")
        submenu_2 = self.dropdown.add_submenu("Tema")

        current_mode = ctk.get_appearance_mode()
    
        for appearance in df.APPEARANCE_MODES:
            label = f"{appearance} ⬅" if appearance == self.appearance else appearance
            submenu_1.add_option(
                option=label,
                command=lambda t=appearance: self.actions.change_appearance(t)
            )
        for color in df.DEFAULT_THEMES:
            label = f"{color} ⬅" if color == self.theme else color
            submenu_2.add_option(
                option=label, command=lambda c=color: self.actions.change_theme(c)
            )
        for tema_per in df.CUSTOM_THEMES:
            label = f"{tema_per} ⬅" if tema_per == self.theme else tema_per
            submenu_2.add_option(
                option=label,
                command=lambda t_p=tema_per: self.actions.change_theme(t_p),
            )


