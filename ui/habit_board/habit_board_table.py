import customtkinter as ctk
from infrastructure.config import defaults as df
from datetime import timedelta
from ui.dialogs.view_settings import (
    COLUMN_HABIT_TABLE_WIDTH
)
from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)
 

class HabitBoardTable(ctk.CTkScrollableFrame):
    def __init__(self, master, fonts , theme_colors,state,date):
        super().__init__(master=master, corner_radius= df.CORNER_RADIUS)
        self.master = master 
        self.fonts = fonts
        self.theme_colors = theme_colors 
        self.state = state
        self.date = date
        self.habits = self.state["habits"]
        self.week_start = self.state["week_start"]
        self.habit_executions = self.state["executions"]


        self.build()
        logger.info("Succesfully built")


    def build(self):
        self.draw_table()
        self.habit_board_grid_config()

    def draw_table(self):


        if not self.habits:

            if hasattr(self, "labels_nombres_habitos"):
                for label in self.labels_nombres_habitos.values():
                    label.destroy()
                self.labels_nombres_habitos.clear()

            if hasattr(self, "labels_estado_habitos"):
                for label in self.labels_estado_habitos.values():
                    label.destroy()
                self.labels_estado_habitos.clear()

            if not hasattr(self, "label_mensaje_sin_habitos"):
                self.label_mensaje_sin_habitos = ctk.CTkLabel(
                    self,
                    text="Crea un nuevo hábito para comenzar! 😏",
                    font=self.fonts["SMALL"],
                )
                self.label_mensaje_sin_habitos.pack(side="top")
            return
        else:
            if hasattr(self, "label_mensaje_sin_habitos"):
                self.label_mensaje_sin_habitos.destroy()
                del self.label_mensaje_sin_habitos

        # --- Inicializar diccionarios si no existen ---
        if not hasattr(self, "labels_estado_habitos"):
            self.labels_estado_habitos = {}  # {(nombre, dia_indic): etiqueta}
        if not hasattr(self, "labels_nombres_habitos"):
            self.labels_nombres_habitos = {}  # {nombre: etiqueta}

        # --- Limpiar hábitos eliminados ---
        habitos_actuales = {h["nombre_habito"] for h in self.habits}

        # Borrar nombres eliminados
        for nombre in list(self.labels_nombres_habitos.keys()):
            if nombre not in habitos_actuales:
                self.labels_nombres_habitos[nombre].destroy()
                del self.labels_nombres_habitos[nombre]

        # Borrar estados de hábitos eliminados
        for nombre, dia_indic in list(self.labels_estado_habitos.keys()):
            if nombre not in habitos_actuales:
                self.labels_estado_habitos[(nombre, dia_indic)].destroy()
                del self.labels_estado_habitos[(nombre, dia_indic)]

        # --- Crear/actualizar tabla de hábitos ---
        for indic, habit in enumerate(self.habits):
            nombre = habit["nombre_habito"]
            fecha_creacion = habit["Fecha_creacion"]

            # Crear nombre de hábito si no existe
            if nombre not in self.labels_nombres_habitos:
                label_nombre = ctk.CTkLabel(
                    self,
                    text=nombre,
                    font=self.fonts["SMALL"],
                    fg_color=self.theme_colors["top_frame"],
                    width=COLUMN_HABIT_TABLE_WIDTH,
                )
                label_nombre.grid(column=0, row=indic + 1, padx=1, sticky="nsew")
                self.labels_nombres_habitos[nombre] = label_nombre
            else:
                # Reubicar en la fila correcta (en caso de que cambie el orden)
                self.labels_nombres_habitos[nombre].grid(
                    column=0, row=indic + 1, padx=1, sticky="nsew"
                )

            # Procesar días
            for dia_indic in range(7):
                dia_semana = self.week_start + timedelta(days=dia_indic)
                dia_semana_str = dia_semana.strftime("%Y-%m-%d")
                dia_ejecucion = habit["dias_ejecucion"][dia_indic]

                # Determinar icono y color

                if dia_semana_str < fecha_creacion:
                    texto, color_texto = "➖", df.COLOR_BORDE
                elif not dia_ejecucion:
                    texto, color_texto = "➖", df.COLOR_BORDE
                else:
                    ejecucion = next(
                        (
                            e
                            for e in self.habit_executions
                            if e["nombre_habito"] == nombre
                            and e["fecha_ejecucion"] == dia_semana_str
                        ),
                        None,
                    )
                    if dia_semana == fecha_creacion:
                        if ejecucion:
                            texto = "⭐"
                            color_texto = "green" if ejecucion["completado"] else "red"
                        elif dia_semana < self.today:
                            texto, color_texto = "⭐", "red"
                        else:
                            texto, color_texto = "⭐", "white"
                    else:
                        if ejecucion:
                            if ejecucion["completado"]:
                                texto, color_texto = "✔", "green"
                            else:
                                texto, color_texto = "✖", "red"
                        else:
                            if dia_semana >= self.date:
                                texto, color_texto = "", df.COLOR_BORDE
                            else:
                                texto, color_texto = "✖", "red"

                key = (nombre, dia_indic)

                if key in self.labels_estado_habitos:
                    self.labels_estado_habitos[key].configure(
                        text=texto, text_color=color_texto
                    )
                    # Reubicar en caso de que cambie el orden
                    self.labels_estado_habitos[key].grid(
                        column=dia_indic + 1, row=indic + 1, padx=1, sticky="nsew"
                    )
                else:
                    label_estado = ctk.CTkLabel(
                        self,
                        text=texto,
                        text_color=color_texto,
                        fg_color=self.theme_colors["top_frame"],
                    )
                    label_estado.grid(
                        column=dia_indic + 1, row=indic + 1, padx=1, sticky="nsew"
                    )
                    self.labels_estado_habitos[key] = label_estado



    def habit_board_grid_config(self):
        for column in range(1, 8):
            self.columnconfigure(column, weight=1, uniform="col")
