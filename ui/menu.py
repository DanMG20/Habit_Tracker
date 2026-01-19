from CTkMenuBarPlus import CustomDropdownMenu,CTkTitleMenu
from infrastructure.config import defaults as df
class MenuBar:
    def __init__(self,master):
        self.master = master
        
        self.build_menu_bar()
        
        
    def build_menu_bar(self):
        menu = CTkTitleMenu(master=self.master)
        button_1 = menu.add_cascade("Tema")
        button_4 = menu.add_cascade("Fuente",
                                    command=self.master.evento_ventana_fuente
                                    )
        button_2 = menu.add_cascade("Restaurar",
                                    command=self.master.reset_files_event
                                    )
        button_3 = menu.add_cascade("Frases")
        self.cascada_boton_3 = CustomDropdownMenu(widget=button_3)
        self.cascada_boton_3.add_option(
            "Agregar Frase", command=self.master.evento_agregar_frase)
        self.submenu_eliminar_frase = self.cascada_boton_3.add_submenu(
            "Eliminar Frase")
        self.generar_menu_frases()

        button_f = menu.add_cascade("Acerca de",
                                    command=self.master.evento_acerca_de_ventana)
        dropdown = CustomDropdownMenu(widget=button_1)

        # -------------------------------------CAMBIAR- TEMA ------------------
        submenu_1 = dropdown.add_submenu("Apariencia")
        submenu_2 = dropdown.add_submenu("Tema")
        for appearance in df.APPEARANCE_MODES:
            submenu_1.add_option(
                option=appearance,
                command=lambda t=appearance: self.master.controller.change_appearance(t))
        for color in df.DEFAULT_THEMES:
            submenu_2.add_option(
                option=color,
                command=lambda c=color: self.master.evento_cambiar_tema(c))
        for tema_per in df.CUSTOM_THEMES:
            submenu_2.add_option(
                option=tema_per,
                command=lambda t_p=tema_per: self.master.evento_cambiar_tema(t_p))
            

    def generar_menu_frases(self):

        self.set_frases = set()  # Crear set vacío
        for frase in self.master.controller.get_phrases():
            self.set_frases.add(frase)  # Agrega solo frases únicas

        # Limpiar menú antes de agregar para evitar duplicados al regenerar
        self.submenu_eliminar_frase.clean()

        # Agregar opciones únicas al menú
        for frase_unica in self.set_frases:
            self.submenu_eliminar_frase.add_option(
                option=frase_unica,
                command=lambda f=frase_unica: self.delete_phrase_event(f))