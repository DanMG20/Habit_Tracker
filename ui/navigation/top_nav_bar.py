import customtkinter as ctk

from infrastructure.config import defaults as df
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

events = {"week_changed", "graph_changed", "day_changed"}
class TopNavBar(ctk.CTkFrame):
    def __init__(self, 
                 master, 
                 style_settings,
                 ):
        super().__init__(master, corner_radius=df.CORNER_RADIUS)
        self.fonts = style_settings["fonts"]
        
   
        self.build()

    def build(self):
        self.draw_left_button()
        self.draw_header()
        self.draw_right_button()

    def draw_left_button(self):
        self.boton_izq_control = ctk.CTkButton(
            self,
            text="<",
            font=self.fonts["SUBTITLE"],
            corner_radius=df.CORNER_RADIUS,
        )
        self.boton_izq_control.pack(
            side="left", fill="both", padx=df.PADX, pady=df.PADY
        )

    def draw_header(self):
        self.header = ctk.CTkLabel(
            self,
            text="",
            font=self.fonts["SUBTITLE"],
            anchor="center",
            corner_radius=df.CORNER_RADIUS,
        )
        self.header.pack(side="left", fill="both", padx=df.PADX, pady=df.PADY)

    def draw_right_button(self):
        self.boton_der_control = ctk.CTkButton(
            self, text=">", font=self.fonts["SUBTITLE"], corner_radius=df.CORNER_RADIUS
        )
        self.boton_der_control.pack(
            side="left", fill="both", padx=df.PADX, pady=df.PADY
        )

    def bind_navigation(self, on_left, on_right):
        logger.warning("Maybe we need to change this method")
        self.boton_der_control.configure(command=on_right)
        self.boton_izq_control.configure(command=on_left)

    def refresh(self, view_state):

        headers = view_state.get("headers", {})


        active_header = headers.get("active")

        if active_header:
            self.header.configure(text=active_header)

