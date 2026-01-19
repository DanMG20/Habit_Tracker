import customtkinter as ctk
from infrastructure.config import defaults as df
from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)


class BottomNavBar(ctk.CTkFrame):
    def __init__(self, master , fonts):
        self.master = master
        self.fonts = fonts

        self.build()
        logger.info("Navigation BOTTOM Bar succesfully built")


    def build(self):
        self.draw_frame()
        self.draw_add_habit_button()
        self.draw_delete_habit_button()
        self.draw_monthly_graph_button()

    def draw_frame(self):
     # --------------------------------------------FRAME-------------------
        self.frame_nav = ctk.CTkFrame(self.master, corner_radius=df.CORNER_RADIUS)
        self.frame_nav.grid(
            row=5,
            column=1,
            columnspan=2,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY
        )

    def draw_add_habit_button(self):
        # -------------------------------------------BOTONES-------------------
        self.boton_agregar_hab = ctk.CTkButton(self.frame_nav,
                                               # fg_color=estilos.COLOR_CONTRASTE,
                                               text="+ Agregar hábito",
                                               command=self.master.evento_btn_agregar_habito,
                                               font=self.fonts["SUBTITLE"],
                                               )
        self.boton_agregar_hab.pack(
            side="left",
            fill="x",
            expand=True,
            padx=df.PADX,
            pady=df.PADY,
        )
    def draw_delete_habit_button(self):
        self.boton_eliminar_hab = ctk.CTkButton(self.frame_nav,
                                                # fg_color=estilos.COLOR_CONTRASTE,
                                                text="- Eliminar hábito",
                                                command=self.master.evento_btn_eliminar_habito,
                                                font=self.fonts["SUBTITLE"],
                                                )
        self.boton_eliminar_hab.pack(
            side="left",
            fill="x",
            expand=True,
            padx=df.PADX,
            pady=df.PADY,
        )

    def draw_monthly_graph_button(self):
        self.boton_rend_mens = ctk.CTkButton(self.frame_nav,
                                             command=self.master.evento_grafica_mensual,
                                             text="Rendimiento Mensual",
                                             font=self.fonts["SUBTITLE"],
                                             )
        self.boton_rend_mens.pack(
            side="left",
            fill="x",
            expand=True,
            padx=df.PADX,
            pady=df.PADY,
        )