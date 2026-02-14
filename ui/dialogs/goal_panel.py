import customtkinter as ctk

import infrastructure.config.defaults as df
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

class GoalPanel(ctk.CTkScrollableFrame): 
    def __init__(self, master ,
                 current_period,
                 get_goals,
                 complete_goal, 
                 style_settings
                 ):
        super().__init__(master, corner_radius=df.CORNER_RADIUS)
        self.static_header = "— Objetivos Trimestrales —"
        self.current_period = current_period
        self.get_goals = get_goals
        self.complete_goal = complete_goal
        self.fonts = style_settings["fonts"]

        self.build()


    def build(self):
        self.draw_static_header()
        self.draw_dinamic_header()
        self.draw_goals()
    def clear_widgets(self):
        pass


    def draw_goals(self):
        goals = self.get_goals()
        if not goals:
            ctk.CTkLabel(
                self,
                text="No hay objetivos registrados.",
                font=self.fonts["SMALL"],
                text_color=df.COLOR_BORDE,
            ).pack(pady=5)
            return
        
        for goal in goals:
            name = goal["goal_name"]
            id = goal["id"]
            btn = ctk.CTkButton(
                self,
                text=name,
                #text_color=df.COLOR_BORDE,
                font=self.fonts["SMALL"],
                command=lambda id=id: self.complete_goal(id),
            )
            btn.pack(fill="x", pady=1, padx=2)
            logger.info(goal["is_completed"])
            if goal["is_completed"]:
                btn.configure(text=f"{name} - Completado!", state="disabled")


    def draw_static_header(self):
        ctk.CTkLabel(
            self,
            text=self.static_header,
            font=self.fonts["SMALL"],
            text_color=df.COLOR_BORDE,
        ).pack(pady=5, fill = "x", expand = True)

    def draw_dinamic_header(self): 
                ctk.CTkLabel(
            self,
            text="Semana "+ self.current_period,
            font=self.fonts["SMALL"],
            text_color=df.COLOR_BORDE,
        ).pack(pady=5, fill="x", expand = True)
