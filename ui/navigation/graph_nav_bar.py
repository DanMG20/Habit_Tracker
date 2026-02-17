import customtkinter as ctk
from infrastructure.config import defaults as df
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class GraphNavBar(ctk.CTkFrame):
    def __init__(self, 
                 master, 
                 style_settings,
                 go_to_main_view
                 ):
        super().__init__(master, corner_radius=df.CORNER_RADIUS)
        self.master = master
        self.fonts = style_settings["fonts"]
        self.go_to_main_view =  go_to_main_view
        
        self.state = "monthly"
        self.build()

    def build(self):
        self.draw_left_button()
        self.draw_right_button()

    def draw_left_button(self):
        self.boton_izq_control = ctk.CTkButton(
            self,
            text="Ventana principal",
            font=self.fonts["SUBTITLE"],
            corner_radius=df.CORNER_RADIUS,
            command=self.go_to_main_view
        )
        self.boton_izq_control.pack(
            side="left", fill="both", padx=df.PADX, pady=df.PADY
        )

    def draw_right_button(self):
        self.boton_der_control = ctk.CTkButton(
            self, text="Rendimiento Anual", font=self.fonts["SUBTITLE"], corner_radius=df.CORNER_RADIUS
        )
        self.boton_der_control.pack(
            side="left", fill="both", padx=df.PADX, pady=df.PADY
        )

    def change_mode(self,mode):
        if mode == "monthly": 
            self.boton_der_control.configure(text="Rendimiento Anual")
        elif mode == "yearly":
            self.boton_der_control.configure(text="Rendimiento Mensual")

    def bind_navigation(self, on_right,mode):
        self.change_mode(mode)
        logger.warning("Maybe we need to change this method")
        self.boton_der_control.configure(command=on_right)


    def refresh(self, header):
        self.header.configure(text=header)

