import customtkinter as ctk

from infrastructure.config import defaults as df
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class BottomNavBar(ctk.CTkFrame):
    def __init__(self, master, fonts, show_goals_panel):
        super().__init__(master, corner_radius=df.CORNER_RADIUS)
        self.master = master
        self.fonts = fonts
        self.show_goals_panel = show_goals_panel

        self._build()
        logger.info("Navigation BOTTOM Bar succesfully built")

    def _build(self):
        self._load_button_configuration()
        self._draw_buttons()



    def _load_button_configuration(self):
        self.buttons = [{
             "name" :"+ Agregar hábito",
             "command": self.master.add_habit_button_event
        },
        {
             "name" :"- Eliminar hábito",
             "command": self.master.delete_habit_button_event
        },
        {
             "name" :"✏ Editar hábito",
             "command": self.master.goals_button_event
        },
        {
             "name" :"🥈 Objetivos",
             "command": self.show_goals_panel
        },
        {
             "name" :"📈 Gráfica Mensual",
             "command": self.master.monthly_graph_event
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


    