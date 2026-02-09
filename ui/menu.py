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
        button_3 = menu.add_cascade("Frases")
        self.cascada_boton_3 = CustomDropdownMenu(widget=button_3)
        self.cascada_boton_3.add_option(
            "Agregar Frase", command=self.master.add_quote_window
        )
        self.submenu_eliminar_frase = self.cascada_boton_3.add_submenu("Eliminar Frase")
        self.gen_menu_quote()

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

    def gen_menu_quote(self):

        self.set_quotes = set()  # Crear set vacío
        for quote in self.master.controller.get_quotes():
           self.set_quotes.add(quote)  # Agrega solo frases únicas

        # Limpiar menú antes de agregar para evitar duplicados al regenerar
        self.submenu_eliminar_frase.clean()

        # Agregar opciones únicas al menú
        for unique_quote in self.set_quotes:
            self.submenu_eliminar_frase.add_option(
                option=unique_quote[1]+ " -- " + unique_quote[2],
                command=lambda f=unique_quote[1]: self.delete_phrase_event(f),
            )
