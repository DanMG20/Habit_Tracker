import customtkinter as ctk
from infrastructure.config import defaults as df
from datetime import timedelta
from ui.dialogs.view_settings import (
    COLUMN_HABIT_TABLE_WIDTH
)
from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)
 

class HabitBoardTable(ctk.CTkScrollableFrame):
    def __init__(self, master, fonts , theme_colors,get_state,date):
        super().__init__(master=master, corner_radius= df.CORNER_RADIUS,fg_color=theme_colors["frame"])
        self.master = master 
        self.fonts = fonts
        self.theme_colors = theme_colors 
        self.get_state = get_state
        self.date = date
        self.build()
        logger.info("Succesfully built")


    def build(self):
        self.draw_table()
        self.habit_board_grid_config()

    def refresh(self):
        self.draw_table()




    def draw_table(self):
        habits = self.get_state()["habits"]
        week_start = self.get_state()["week_start"]
        habit_executions = self.get_state()["executions"]



        if not habits:

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
        habitos_actuales = {h["habit_name"] for h in habits}

        # Borrar nombres eliminados
        for habit_id in list(self.labels_nombres_habitos.keys()):
            if habit_id not in habitos_actuales:
                self.labels_nombres_habitos[habit_id].destroy()
                del self.labels_nombres_habitos[habit_id]

        # Borrar estados de hábitos eliminados
        for habit_id, dia_indic in list(self.labels_estado_habitos.keys()):
            if habit_id not in habitos_actuales:
                self.labels_estado_habitos[(habit_id, dia_indic)].destroy()
                del self.labels_estado_habitos[(habit_id, dia_indic)]

        # --- Crear/actualizar tabla de hábitos ---
        for indic, habit in enumerate(habits):
            habit_id = habit["id"]
            fecha_creacion = habit["creation_date"]

            # Crear nombre de hábito si no existe
            if habit_id not in self.labels_nombres_habitos:
                label_nombre = ctk.CTkLabel(
                    self,
                    text=habit["habit_name"],
                    font=self.fonts["SMALL"],
                    fg_color=self.theme_colors["top_frame"],
                    width=COLUMN_HABIT_TABLE_WIDTH,
                )
                label_nombre.grid(column=0, row=indic + 1, padx=2,pady= 1, sticky="nsew")
                self.labels_nombres_habitos[habit_id] = label_nombre
            else:
                # Reubicar en la fila correcta (en caso de que cambie el orden)
                self.labels_nombres_habitos[habit_id].grid(
                    column=0, row=indic + 1, padx=1, sticky="nsew"
                )

            # Procesar días
            for dia_indic in range(7):
                dia_semana = week_start + timedelta(days=dia_indic)
                dia_ejecucion = habit["execution_days"][dia_indic]

                # Determinar icono y color

                if dia_semana < fecha_creacion:
                    texto, color_texto = "➖", df.COLOR_BORDE
                elif not dia_ejecucion:
                    texto, color_texto = "➖", df.COLOR_BORDE
                else:
                    ejecucion = next(
                        (
                            e
                            for e in habit_executions
                            if e["habit_id"] == habit_id
                            and e["execution_date"] == dia_semana
                        ),
                        None,
                    )
                    
                    if dia_semana == fecha_creacion:
                        
                        if ejecucion:
                            texto = "⭐"
                            
                            color_texto = "green" if ejecucion["executed"] else "red"
                        elif dia_semana < self.date:
                            texto, color_texto = "⭐", "red"
                        else:
                            texto, color_texto = "⭐", "white"
                    else:
                        if ejecucion:
                            if ejecucion["executed"]:
                                texto, color_texto = "✔", "green"
                            else:
                                texto, color_texto = "✖", "red"
                        else:
                            if dia_semana >= self.date:
                                texto, color_texto = "", df.COLOR_BORDE
                            else:
                                texto, color_texto = "✖", "red"

                key = (habit_id, dia_indic)

                if key in self.labels_estado_habitos:
                    self.labels_estado_habitos[key].configure(
                        text=texto, text_color=color_texto
                    )
                    # Reubicar en caso de que cambie el orden
                    self.labels_estado_habitos[key].grid(
                        column=dia_indic + 1, row=indic + 1, padx=2,pady=1, sticky="nsew"
                    )
                else:
                    label_estado = ctk.CTkLabel(
                        self,
                        text=texto,
                        text_color=color_texto,
                        fg_color=self.theme_colors["top_frame"],
                    )
                    label_estado.grid(
                        column=dia_indic + 1, row=indic + 1, padx=2,pady=1, sticky="nsew"
                    )
                    self.labels_estado_habitos[key] = label_estado



    def habit_board_grid_config(self):
        for column in range(1, 8):
            self.columnconfigure(column, weight=1, uniform="col")
