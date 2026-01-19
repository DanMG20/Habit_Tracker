import customtkinter as ctk 
from CTkMessagebox import CTkMessagebox
from utils.tooltip import Tooltip
import infrastructure.config.defaults as df
from domain.style_service import StyleService
from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)

class DeleteHabitFrame:
    def __init__(self,controller,master):
        self.master = master
        self.controller = controller
        self.db = self.controller.db # TEMPORAL
        logger.warning("Temporal db object")
        self.load_style_settings()
        self.crear_frame_eliminar_habito()

    def load_style_settings(self):
        style_service = StyleService()
        self.theme_colors=style_service._load_theme_colors()
        self.fonts = style_service.build_fonts()


    def crear_frame_eliminar_habito(self): 
        self.frame_eliminar_habito_contenedor= ctk.CTkFrame(self.master, corner_radius=df.CORNER_RADIUS)
        self.frame_eliminar_habito_contenedor.grid(
            row=3,
            column=0,
            sticky="nsew",
            rowspan = 3, 
            padx= df.PADX,
            pady= df.PADY
        )
        self.frame_eliminar_habito= ctk.CTkScrollableFrame(
            self.frame_eliminar_habito_contenedor, 
            corner_radius=df.CORNER_RADIUS,
            fg_color=self.theme_colors["frame"]
            )
        self.frame_eliminar_habito.pack(
            fill="both",
            expand = True,                 
            padx= df.PADX,
            pady = df.PADY)
        self.listar_habitos()

    def listar_habitos(self):   
        """Lista los nombres de los hábitos en el marco, agregando solo los nuevos y evitando duplicados."""

        if not hasattr(self, "habitos_creados"):
            self.habitos_creados = set()
        if not hasattr(self, "botones_habitos"):
            self.botones_habitos = {}
        if not hasattr(self, "label_sin_habitos"):
            self.label_sin_habitos = None

        ejecuciones = self.db.cargar_ejecuciones()  # Cargar ejecuciones actuales

        # 1️⃣ Eliminar botones de hábitos que ya no existan en la base de datos
        habitos_actuales = {habit["nombre_habito"] for habit in self.db.habitos}
        for nombre in list(self.habitos_creados):
            if nombre not in habitos_actuales:
                if nombre in self.botones_habitos:
                    self.botones_habitos[nombre].destroy()
                    del self.botones_habitos[nombre]
                self.habitos_creados.remove(nombre)

        # 2️⃣ Si no hay hábitos
        if not self.db.habitos:
            if not self.habitos_creados and self.label_sin_habitos is None:
                self.label_sin_habitos = ctk.CTkLabel(
                    self.frame_eliminar_habito,
                    text="No hay hábitos registrados.",
                    text_color=df.COLOR_BORDE,
                    font=self.fonts["SMALL"]
                )
                self.label_sin_habitos.pack(pady=5)
            return  # Salir para no crear botones innecesariamente

        # 🧹 Eliminar mensaje "No hay hábitos registrados" si ya hay hábitos
        if self.label_sin_habitos:
            self.label_sin_habitos.destroy()
            self.label_sin_habitos = None

        # 3️⃣ Crear título si no existe
        if not getattr(self, "titulo_habitos", None):
            self.titulo_habitos = ctk.CTkLabel(
                self.frame_eliminar_habito,
                text="Selecciona el hábito para eliminarlo \n ESTA ACCION NO SE PUEDE DESHACER",
                font=self.fonts["SMALL"]
            )
            self.titulo_habitos.pack(pady=5)

        # 4️⃣ Crear botones solo para los hábitos nuevos
        for habit in self.db.habitos:
            nombre = habit["nombre_habito"]
            if nombre not in self.habitos_creados:
                boton = ctk.CTkButton(
                    self.frame_eliminar_habito,
                    text=nombre,
                    fg_color=habit["color"],
                    font=self.fonts["SMALL"],
                    command=lambda h=nombre: self.evento_eliminar_habito_selec(h)
                )
                boton.pack(fill="x", pady=1, padx=2)

                self.botones_habitos[nombre] = boton

                 # 🔹 Agregar tooltip con la descripción del hábito
                descripcion = habit.get("descripcion", "Sin descripción")
                Tooltip(boton, descripcion)

                self.habitos_creados.add(nombre)

    def evento_eliminar_habito_selec(self, habit_seleccionado):
            """Elimina directamente el hábito seleccionado."""
            msg = CTkMessagebox(
                master = self.master ,
                title="Confirmación",
                message=f"¿Estás seguro de que deseas eliminar el hábito '{habit_seleccionado}'?",
                font =self.fonts["SMALL"],
                icon="question", option_1="No", option_2="Yes")
            response =  msg.get()
            if response =="Yes":
                self.db.habitos = [habito for habito in self.db.habitos if habito["nombre_habito"] != habit_seleccionado]
                self.db.guardar_habitos()
                CTkMessagebox(
                    master =self.master,
                    title ="Info",
                    font= self.fonts["SMALL"],
                    message=f"El hábito '{habit_seleccionado}' ha sido eliminado.")
            self.listar_habitos()
            self.master.listar_habitos()
            self.master.lista_habitos_frame_semana()
            self.master.listar_habitos_ayer()
            