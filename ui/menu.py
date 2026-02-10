from CTkMenuBarPlus import CTkTitleMenu, CustomDropdownMenu

from infrastructure.config import defaults as df


class MenuBar:
    def __init__(self, master):
        self.master = master

        self.build_menu_bar()

    def build_menu_bar(self):
        menu = CTkTitleMenu(master=self.master)
        button_1 = menu.add_cascade("Tema")
        button_4 = menu.add_cascade("Fuente", command=self.master.font_window_event)
        button_2 = menu.add_cascade("Restaurar", command=self.master.reset_files_event)
        button_3 = menu.add_cascade("Frases", postcommand=self.master.add_quote_window )
   
        button_f = menu.add_cascade("Acerca de", command=self.master.about_window_event)
        dropdown = CustomDropdownMenu(widget=button_1)

        # -------------------------------------CAMBIAR- TEMA ------------------
        submenu_1 = dropdown.add_submenu("Apariencia")
        submenu_2 = dropdown.add_submenu("Tema")
        for appearance in df.APPEARANCE_MODES:
            submenu_1.add_option(
                option=appearance,
                command=lambda t=appearance: self.master.controller.change_appearance(
                    t
                ),
            )
        for color in df.DEFAULT_THEMES:
            submenu_2.add_option(
                option=color, command=lambda c=color: self.master.change_theme_event(c)
            )
        for tema_per in df.CUSTOM_THEMES:
            submenu_2.add_option(
                option=tema_per,
                command=lambda t_p=tema_per: self.master.change_theme_event(t_p),
            )

