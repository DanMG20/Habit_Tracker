import customtkinter as ctk

from infrastructure.config import defaults as df
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class BottomNavBar(ctk.CTkFrame):
    def __init__(self,
                 master, 
                 style_settings, 
                 show_goals_panel,
                 show_edit_panel,
                 show_delete_panel,
                 go_to_add_habit_view,
                 go_to_graph_view, 
                 ):
        super().__init__(master, corner_radius=df.CORNER_RADIUS)
        self.master = master
        self.fonts = style_settings["fonts"]
        self.show_goals_panel = show_goals_panel
        self.show_edit_panel = show_edit_panel
        self.show_delete_panel = show_delete_panel
        self.go_to_add_habit_view = go_to_add_habit_view
        self.go_to_graph_view = go_to_graph_view


        self._build()


    def _build(self):
        self._load_button_configuration()
        self._draw_buttons()



    def _load_button_configuration(self):
        self.buttons = [{
             "name" :"+ Agregar hábito",
             "command": self.go_to_add_habit_view
        },
        {
             "name" :"- Eliminar hábito",
             "command": self.show_delete_panel
        },
        {
             "name" :"✏ Editar hábito",
             "command": self.show_edit_panel
        },
        {
             "name" :"🥈 Objetivos",
             "command": self.show_goals_panel
        },
        {
             "name" :"📈 Gráfica Mensual",
             "command": self.go_to_graph_view
        },
        ]

    def _draw_buttons(self): 
         
         for button in self.buttons:
              self._draw_button(button["name"],button["command"])
         
    def _draw_button(self,name, command):
            ctk.CTkButton(
            self,
            text=name,
            command=command,
            font=self.fonts["SUBTITLE"],
        ).pack(
            side="left",
            fill="both",
            expand=True,
            padx=df.PADX,
            pady=df.PADY,
        )


    