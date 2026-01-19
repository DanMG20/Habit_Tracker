import customtkinter as ctk
from domain.style_service import StyleService
from ui.top_section import TopSection
import sys
from ui.menu import MenuBar
from ui.navigation.top_nav_bar import TopNavBar
from ui.navigation.bottom_nav_bar import BottomNavBar
from utils.paths import obtener_direccion_icono
from CTkMenuBarPlus import *
from ui.dialogs.font_settings import FontSettings
from ui.dialogs.add_habbit import AddHabitFrame
from ui.graphs.monthly_graph import MonthlyGraph
from utils.window_state import load_window_pos, save_window_pos
from ui.dialogs.delete_habbit import DeleteHabitFrame
from ui.dialogs.add_quote import AddQuote
from ui.dialogs.about import About
from ui.graphs.yearly_graph import YearlyGraph
from datetime import *
from utils.tooltip import Tooltip
import infrastructure.config.defaults as df
from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)

class MainWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()

        self.title("")
        icon = obtener_direccion_icono()
        self.iconbitmap(icon)

        self.controller = controller
        self.db = self.controller.db
        self.load_style_settings()
        self.refresh_week_state()
        self.width_column_habitos_tabla = 350
        self.estado_boton_eliminar_habito = False
        self.estado_boton_marcar_ayer = False
        self.today = self.controller.get_calendar_state()["today"]
        self.yesterday = self.controller.get_calendar_state()["yesterday"]
        load_window_pos(self)
        self.load_all_frames()
        self.draw_menu_bar()
        self.draw_top_nav_bar()
        self.draw_bottom_nav_bar()
        self.draw_yearly_graph()
        self.draw_monthly_graph()
        self.grid_config()

        self.fecha_guardada = self.controller.verify_date()
        self.start_date_verification()
        self.open_window_maximized()

        self.protocol("WM_DELETE_WINDOW", self.close_event)





    def draw_menu_bar(self):
        self.menu_bar = MenuBar(self)
        self.top_section = TopSection(
            self,
            self.controller.load_phrase()['phrase'],
            self.controller.load_phrase()['author'],
            self.fonts
        )
    def draw_top_nav_bar(self):
        self.top_nav_bar = TopNavBar(
            self,
            self.fonts
        )
        self.top_nav_bar.update_header(self.headers[1])
        self.top_nav_bar.bind_navigation(
            on_left=self.go_to_previous_week_event,
            on_right=self.go_to_next_week_event
            )

    def draw_bottom_nav_bar(self):
        self.bottom_nav_bar = BottomNavBar(
            self,
            self.fonts
        )
        
    def draw_yearly_graph(self):
                self.yearly_graph = YearlyGraph(
            master=self,
            frames_ventana_principal=self.frames_ventana_principal_lista,
            controller=self.controller
        )
    
    def draw_monthly_graph(self):
        self.monthly_graph = MonthlyGraph(
            self,
            self.controller,
            self.frames_ventana_principal_lista,
            self.yearly_graph)

    def open_window_maximized(self):
        self.after_idle(lambda: self.state("zoomed"))

    def start_date_verification(self):
        self.controller.verify_date()
        self.after(300000, self.start_date_verification)
        logger.info("Date succesfully verificated")

    def refresh_week_state(self):
        date_vars = self.controller.get_week_state()
        self.headers = date_vars["headers"]
        self.week_start = date_vars["week_start"]
        self.current_days = date_vars["current_days"]
        self.rendimiento_semanal = date_vars["weekly_performance"]

    def update_table_and_dates(self, event):
        self.refresh_week_state()
        self.performance_bar.set(self.rendimiento_semanal / 100)
        self.performance_label.configure(text=f"{self.rendimiento_semanal}%")
        self.draw_habit_board_header()
        self.draw_habit_board_frame()

    def load_style_settings(self):
        style_service = StyleService()
        self.theme_colors = style_service._load_theme_colors()
        self.fonts = style_service.build_fonts()

    def close_event(self):
        save_window_pos(self)
        self.unbind("<Configure>")
        for win in self.winfo_children():
            win.destroy()
        self.destroy()                   
        sys.exit()


    def draw_add_habit_frame(self):
        self.add_habit_frame = AddHabitFrame(
            master=self,
            controller=self.controller,
            frames_ventana_principal=self.frames_ventana_principal_lista,
        )
        self.add_habit_frame.hide()
    def draw_delete_habit_frame(self):
        self.delete_habit_frame = DeleteHabitFrame(
            master=self,
            controller=self.controller,
        )

    def show_monthly_graph(self):
        if hasattr(
                self, "monthly_graph") and self.monthly_graph:
            self.monthly_graph.inicializar_frames_graf_mensual()

    def draw_yearly_graph_frame(self):
        if hasattr(self, "yearly_graph") and self.yearly_graph:
            # Solo actualizar la gráfica existente

            self.yearly_graph.abrir_frames()
            self.yearly_graph.frame_grafica_anual.grid(
                row=3,
                column=0,
                columnspan=3,
                sticky="nsew",
                rowspan=3,
                padx=df.PADX,
                pady=df.PADY
            )
        else:

            self.yearly_graph = YearlyGraph(
                self,
                self.controller,
                self.frames_ventana_principal_lista,

            )

    def load_all_frames(self):
        self.frames_ventana_principal()
        self.draw_add_habit_frame()
        self.draw_delete_habit_frame()
        self.draw_yesterday_check_frame()

    def frames_ventana_principal(self):
        self.draw_date_frame()
        self.draw_performance_bar_frame()
        self.draw_check_buttons_for_today()
        self.draw_habit_board()
        self.frames_ventana_principal_lista = [self.date_frame,
                                               self.performance_bar_frame,
                        
                                               self.check_buttons_today_frame,
                                               self.frame_tabla_habitos_contenedor,
                                               self.frame_encabezado
                                               ]

 
    def grid_config(self):
        # ----------------------------------------------PRINCIPAL
        for columna in range(1, 2):
            self.columnconfigure(columna, weight=1)
        self.rowconfigure(4, weight=1)

# --------------------------------------------------FRAMES PRINCIPALES----
    def reset_files_event(self):
        self.controller.reset_files()
        self.reiniciar_app()

    def draw_date_frame(self):
        self.date_frame = ctk.CTkFrame(
            self, corner_radius=df.CORNER_RADIUS)
        self.date_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            pady=df.PADY,
            padx=df.PADX
        )
        self.draw_date()
    def draw_date(self):
        self.fecha_hoy_label = ctk.CTkLabel(
            self.date_frame,
            text=self.headers[0],
            anchor="center",
            font=self.fonts["SUBTITLE"])
        self.fecha_hoy_label.pack(
            fill="both",
            expand=True,
            pady=df.PADY,
            padx=df.PADX)

    def draw_performance_bar_frame(self):
        self.performance_bar_frame = ctk.CTkFrame(
            self, corner_radius=df.CORNER_RADIUS)
        self.performance_bar_frame.grid(
            row=2,
            column=1,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY
        )
        self.draw_performance_bar()
        self.draw_performance_label()
    def draw_performance_bar(self):
        self.performance_bar = ctk.CTkProgressBar(
            self.performance_bar_frame,
            # progress_color=estilos.COLOR_CONTRASTE,
            corner_radius=df.CORNER_RADIUS * 2)
        self.performance_bar.pack(
            side="left",
            fill="both",
            expand=True,
            padx=df.PADX * 1.5,
            pady=df.PADY * 1.5
        )
        self.performance_bar.set(self.rendimiento_semanal / 100)
    def draw_performance_label(self):
        self.performance_label = ctk.CTkLabel(
            self.performance_bar_frame,
            text=f"{self.rendimiento_semanal}%",
            font=self.fonts["SMALL"])
        self.performance_label.pack(
            side="right",
            fill="both",
            padx=df.PADX * 2,
            pady=df.PADY
        )


    def draw_check_buttons_for_today(self):
        self.check_buttons_today_frame = ctk.CTkFrame(
            self,
            corner_radius=df.CORNER_RADIUS,
        )
        self.check_buttons_today_frame.grid(
            row=3,
            column=0,
            sticky="nsew",
            rowspan=3,
            padx=df.PADX,
            pady=df.PADY
        )

        self.scroll_frame_check_buttons_today = ctk.CTkScrollableFrame(
            self.check_buttons_today_frame,
            corner_radius=df.CORNER_RADIUS,
            fg_color=self.theme_colors["frame"],
        )
        self.scroll_frame_check_buttons_today.pack(
            fill="both",
            expand=True,
            padx=df.PADX,
            pady=df.PADY)
        self.draw_check_buttons_of_date(self.today)

    def draw_habit_board(self):
        self.frame_tabla_habitos_contenedor = ctk.CTkFrame(
            self,
            corner_radius=df.CORNER_RADIUS,
            fg_color=self.theme_colors["frame"]
        )
        self.frame_tabla_habitos_contenedor.grid(row=3,
                                                 column=1,
                                                 rowspan=2,
                                                 columnspan=2,
                                                 sticky="nsew",
                                                 pady=df.PADY,
                                                 padx=df.PADX
                                                 )

        self.frame_tabla_habitos = ctk.CTkScrollableFrame(
            self.frame_tabla_habitos_contenedor,
            corner_radius=df.CORNER_RADIUS,
            fg_color=self.theme_colors["frame"])
        self.frame_tabla_habitos.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY
        )
        self.habit_board_grid_config()
        self.draw_habit_board_frame()
        # ----------------------------------------------FRAME TABLA HABITOS
        self.frame_tabla_habitos_contenedor.columnconfigure(0, weight=1)

        self.frame_tabla_habitos_contenedor.rowconfigure(1, weight=1)
        self.draw_habit_board_header()

# ---------------------------------------------FRAMES SECUNDARIOS --------
    def draw_habit_board_header(self):
        # --------------------------------------FRAME
        self.frame_encabezado = ctk.CTkFrame(
            self.frame_tabla_habitos_contenedor,
            corner_radius=df.CORNER_RADIUS,
            fg_color=self.theme_colors["frame"]
        )
        self.frame_encabezado.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(df.PADX, df.PADX * 3.5),
            pady=df.PADY
        )
        self.boton_marcar = ctk.CTkButton(
            self.frame_encabezado,
            text="¿Olvidaste marcar ayer?",
            command=self.evento_marcar_ayer,
            # fg_color=estilos.COLOR_CONTRASTE,
            width=self.width_column_habitos_tabla,
            font=self.fonts["SMALL"])
        self.boton_marcar.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY
        )
        # Labels dias actuales
        for indice, dia in enumerate(self.current_days):
            if dia < self.today:
                color_label = self.theme_colors["top_frame"]
            elif dia == self.today:
                color_label = self.theme_colors["button"]
            elif dia > self.today:
                color_label = self.theme_colors["progressbar"]

            ctk.CTkLabel(self.frame_encabezado,
                         text=dia.day,
                         font=self.fonts["SMALL"],
                         fg_color=color_label,
                         corner_radius=999
                         ).grid(row=0,
                                column=indice + 1,
                                sticky="nsew",
                                padx=1,
                                pady=df.PADY
                                )
            self.frame_encabezado.columnconfigure(
                indice + 1, weight=1, uniform="col")
        encabezados = [
            "Actividad",
            "Domingo",
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado"]
        for ind, encabezado in enumerate(encabezados):
            ctk.CTkLabel(self.frame_encabezado,
                         text=encabezado,
                         font=self.fonts["SMALL"]
                         ).grid(
                             row=1,
                             column=ind,
                             sticky="nsew",
                             padx=2,
                             pady=df.PADY,

            )

    def draw_yesterday_check_frame(self):
        self.frame_btn_completar_ayer_contenedor = ctk.CTkFrame(
            self,
            corner_radius=df.CORNER_RADIUS,
        )
        self.frame_btn_completar_ayer_contenedor.grid(
            row=3,
            column=0,
            sticky="nsew",
            rowspan=3,
            padx=df.PADX,
            pady=df.PADY
        )

        self.frame_btn_completar_ayer = ctk.CTkScrollableFrame(
            self.frame_btn_completar_ayer_contenedor,
            corner_radius=df.CORNER_RADIUS,
            fg_color=self.theme_colors["frame"],
        )
        self.frame_btn_completar_ayer.pack(
            fill="both",
            expand=True,
            padx=df.PADX,
            pady=df.PADY)
        self.listar_habitos_ayer()



    def listar_habitos_ayer(self):
        """Lista los nombres de los hábitos en el marco, agregando solo los nuevos y eliminando los que ya no existan."""
        if not hasattr(self, "habitos_creados_ayer"):
            self.habitos_creados_ayer = set()
        if not hasattr(self, "botones_habitos_ayer"):
            self.botones_habitos_ayer = {}

        # Cargar ejecuciones actuales
        ejecuciones = self.controller.load_habit_register_executions()

        # 1️⃣ Eliminar botones de hábitos que ya no estén en la base de datos
        habitos_actuales = {habit["nombre_habito"]
                            for habit in self.db.habitos}
        for nombre in list(self.habitos_creados_ayer):
            if nombre not in habitos_actuales:
                if nombre in self.botones_habitos_ayer:
                    self.botones_habitos_ayer[nombre].destroy()
                    del self.botones_habitos_ayer[nombre]
                self.habitos_creados_ayer.remove(nombre)

        # 2️⃣ Si no hay hábitos
        if not self.db.habitos:
            if not self.habitos_creados_ayer:
                if not hasattr(self, "mensaje_no_habitos_ayer"):
                    self.mensaje_no_habitos_ayer = ctk.CTkLabel(
                        self.frame_btn_completar_ayer,
                        text="No hay hábitos registrados.",
                        fg_color=self.theme_colors["frame"],
                        text_color=df.COLOR_BORDE,
                        font=self.fonts["SMALL"]
                    )
                    self.mensaje_no_habitos_ayer.pack(pady=5)
            return
        else:
            # Eliminar mensaje de "No hay hábitos" si ahora sí hay
            if hasattr(self, "mensaje_no_habitos_ayer"):
                self.mensaje_no_habitos_ayer.destroy()
                del self.mensaje_no_habitos_ayer

        # 3️⃣ Crear título si no existe
        if not getattr(self, "titulo_habitos_ayer", None):
            self.titulo_habitos_ayer = ctk.CTkLabel(
                self.frame_btn_completar_ayer,
                text="Selecciona el hábito para completarlo!",
                text_color=df.COLOR_BORDE,
                font=self.fonts["SMALL"]
            )
            self.titulo_habitos_ayer.pack(pady=5)
        if not getattr(self, "titulo_habitos_ayer_2", None):
            self.titulo_habitos_ayer_2 = ctk.CTkLabel(
                self.frame_btn_completar_ayer,
                text="(Recuerda que esto marcará los hábitos la fecha de ayer)",
                text_color=df.COLOR_AUTOR,
                font=self.fonts["SMALL"]
            )
            self.titulo_habitos_ayer_2.pack(pady=5)

        # 4️⃣ Crear botones solo para nuevos hábitos
        fecha_ayer_str = self.yesterday.strftime("%Y-%m-%d")
        for habit in self.db.habitos:
            nombre = habit["nombre_habito"]
            if nombre not in self.habitos_creados_ayer:
                boton = ctk.CTkButton(
                    self.frame_btn_completar_ayer,
                    text=nombre,
                    fg_color=habit["color"],
                    text_color=df.COLOR_BORDE,
                    font=self.fonts["SMALL"],
                    command=lambda h=nombre: self.evento_marcar_habito_ayer(h)
                )
                boton.pack(fill="x", pady=1, padx=2)

                self.botones_habitos_ayer[nombre] = boton

                # 5️⃣ Verificar si el hábito está completado ayer
                completado = any(
                    e["nombre_habito"] == nombre and
                    e["fecha_ejecucion"] == fecha_ayer_str and
                    e.get("completado", False)
                    for e in ejecuciones
                )

                # 📅 Calcular índice de día (semana iniciando en domingo)
                indice_dia = (self.yesterday.weekday() + 1) % 7

                # 🚫 Deshabilitar botón si ya fue completado, no toca ese día,
                # o si el hábito se creó ayer
                if (
                    completado
                    or not habit["dias_ejecucion"][indice_dia]
                    or habit["Fecha_creacion"] == self.today
                ):
                    boton.configure(
                        text=f"{nombre} - Completado!",
                        state="disabled")

                self.habitos_creados_ayer.add(nombre)

    def create_no_habits_message(self):
        if not hasattr(self, "no_habit_message"):
            self.no_habit_message = ctk.CTkLabel(
                self.scroll_frame_check_buttons_today,
                text="No hay hábitos registrados.",
                fg_color=self.theme_colors["frame"],
                text_color=df.COLOR_BORDE,
                font=self.fonts["SMALL"]
            )
            self.no_habit_message.pack(pady=5)

    def delete_no_habits_message(self):
        if hasattr(self, "no_habits_message"):
            self.no_habit_message.destroy()
            del self.no_habit_message

    def draw_check_frame_title(self):
        # 3️⃣ Crear título si no existe
        if not getattr(self, "titulo_habitos", None):
            self.titulo_habitos = ctk.CTkLabel(
                self.scroll_frame_check_buttons_today,
                text="Selecciona el hábito para completarlo!",
                text_color=df.COLOR_BORDE,
                font=self.fonts["SMALL"]
            )
            self.titulo_habitos.pack(pady=5)

    def draw_check_button(self, habit_name, color):
        button = ctk.CTkButton(
            self.scroll_frame_check_buttons_today,
            text=habit_name,
            fg_color=color,
            text_color=df.COLOR_BORDE,
            font=self.fonts["SMALL"],
            command=lambda h=habit_name: self.habit_check_event(h)
        )
        button.pack(fill="x", pady=1, padx=2)
        return button

    def _draw_single_habit(self, name, color, description=None):

        button = self.draw_check_button(name, color)
        # self.habit_check_buttons[name] = button
        Tooltip(button, description)
        # today_str = self.today.strftime("%Y-%m-%d")

        if self.controller.is_habit_completed_on_date(name, self.today):
            button.configure(
                text=f"{name} - Completado!",
                state="disabled"
            )

    def draw_check_buttons_of_date(self, date):
        if not self.controller.has_habits():
            self.create_no_habits_message()
            return

        self.delete_no_habits_message()
        self.draw_check_frame_title()

        for habit in self.controller.get_habits_for_current_date(date):
            self._draw_single_habit(
                habit["nombre_habito"],
                habit["color"],
                habit["descripcion"]
            )

    def draw_habit_board_frame(self):
        # Recargar datos actualizados
        self.db.cargar_habitos()
        ejecuciones = self.db.cargar_ejecuciones()

        # --- Si no hay hábitos ---
        if not self.db.habitos:
            # 🔴 Eliminar labels viejos de hábitos si existen
            if hasattr(self, "labels_nombres_habitos"):
                for label in self.labels_nombres_habitos.values():
                    label.destroy()
                self.labels_nombres_habitos.clear()

            if hasattr(self, "labels_estado_habitos"):
                for label in self.labels_estado_habitos.values():
                    label.destroy()
                self.labels_estado_habitos.clear()

            # Mostrar mensaje "sin hábitos"
            if not hasattr(self, "label_mensaje_sin_habitos"):
                self.label_mensaje_sin_habitos = ctk.CTkLabel(
                    self.frame_tabla_habitos,
                    text="Crea un nuevo hábito para comenzar! 😏",
                    font=self.fonts["SMALL"]
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
        habitos_actuales = {h["nombre_habito"] for h in self.db.habitos}

        # Borrar nombres eliminados
        for nombre in list(self.labels_nombres_habitos.keys()):
            if nombre not in habitos_actuales:
                self.labels_nombres_habitos[nombre].destroy()
                del self.labels_nombres_habitos[nombre]

        # Borrar estados de hábitos eliminados
        for (nombre, dia_indic) in list(self.labels_estado_habitos.keys()):
            if nombre not in habitos_actuales:
                self.labels_estado_habitos[(nombre, dia_indic)].destroy()
                del self.labels_estado_habitos[(nombre, dia_indic)]

        # --- Crear/actualizar tabla de hábitos ---
        for indic, habit in enumerate(self.db.habitos):
            nombre = habit["nombre_habito"]
            fecha_creacion = habit["Fecha_creacion"]

            # Crear nombre de hábito si no existe
            if nombre not in self.labels_nombres_habitos:
                label_nombre = ctk.CTkLabel(
                    self.frame_tabla_habitos,
                    text=nombre,
                    font=self.fonts["SMALL"],
                    fg_color=self.theme_colors["top_frame"],
                    width=self.width_column_habitos_tabla,
                )
                label_nombre.grid(
                    column=0, row=indic + 1, padx=1, sticky="nsew")
                self.labels_nombres_habitos[nombre] = label_nombre
            else:
                # Reubicar en la fila correcta (en caso de que cambie el orden)
                self.labels_nombres_habitos[nombre].grid(
                    column=0, row=indic + 1, padx=1, sticky="nsew")

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
                        (e for e in ejecuciones if e["nombre_habito"] ==
                         nombre and e["fecha_ejecucion"] == dia_semana_str),
                        None
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
                            if dia_semana >= self.today:
                                texto, color_texto = "", df.COLOR_BORDE
                            else:
                                texto, color_texto = "✖", "red"

                key = (nombre, dia_indic)

                if key in self.labels_estado_habitos:
                    self.labels_estado_habitos[key].configure(
                        text=texto, text_color=color_texto)
                    # Reubicar en caso de que cambie el orden
                    self.labels_estado_habitos[key].grid(
                        column=dia_indic + 1, row=indic + 1, padx=1, sticky="nsew")
                else:
                    label_estado = ctk.CTkLabel(
                        self.frame_tabla_habitos,
                        text=texto,
                        text_color=color_texto,
                        fg_color=self.theme_colors["top_frame"],
                    )
                    label_estado.grid(
                        column=dia_indic + 1,
                        row=indic + 1,
                        padx=1,
                        sticky="nsew")
                    self.labels_estado_habitos[key] = label_estado

    def habit_board_grid_config(self):
        for column in range(1, 8):
            self.frame_tabla_habitos.columnconfigure(
                column, weight=1, uniform="col")

    def actualizacion_agregar_habito(self):
        self.draw_check_buttons_of_date(self.today)
        self.update_table_and_dates(None)



    def reiniciar_app(self):
        self.destroy()  # Cierra la ventana
        os.execl(sys.executable, sys.executable, *sys.argv)


    def delete_phrase_event(self, selected_phrase):
        self.controller.delete_selected_phrase(selected_phrase)

    def change_nav_config_to_month(self):
        self.top_nav_bar.bind_navigation(
            on_left=self.go_to_previous_month_event,
            on_right=self.go_to_next_month_event
        )

    def change_nav_config_to_year(self):
        self.top_nav_bar.bind_navigation(
            on_left=self.evento_anio_anterior,
            on_right=self.evento_anio_siguiente
        )

    def evento_marcar_habito_ayer(self, habit_name):
        self.controller.check_habit_yesterday(habit_name)
        self.rendimiento_semanal = self.controller.get_weekly_performance()
        self.update_table_and_dates(None)
        # Actualizar botón: cambiar texto y deshabilitar
        if hasattr(
                self, "botones_habitos_ayer") and habit_name in self.botones_habitos_ayer:
            boton = self.botones_habitos_ayer[habit_name]
            boton.configure(
                text=f"{habit_name} - Completado!",
                state="disabled")

    def evento_btn_agregar_habito(self):
        self.add_habit_frame.crear_frame_derecho()
        self.add_habit_frame.nombre_ventana_frame_1_0()
        for frame in self.add_habit_frame.frames_agregar_habito:
            frame.tkraise()

    def evento_btn_eliminar_habito(self):
        self.estado_boton_eliminar_habito = not self.estado_boton_eliminar_habito
        if self.estado_boton_eliminar_habito:
            self.delete_habit_frame.frame_eliminar_habito_contenedor.tkraise()
        else:
            self.check_buttons_today_frame.tkraise()

    def evento_cambiar_tema(self, new_theme=None, nuevo_modo=None):
        msg = CTkMessagebox(
            master=self,
            title="Confirmación",
            message=f"¿Estás seguro de que deseas cambiar el tema a '{new_theme}'? \n es necesario reiniciar la aplicación",
            font=self.fonts["SMALL"],
            icon="question", option_1="No", option_2="Sí")
        response = msg.get()
        if response == "Sí":
            self.controller.change_theme(new_theme)
            self.reiniciar_app()

    def evento_agregar_frase(self):
        self.ventana_agregar_frase_objeto = AddQuote(
            master=self,
            controller=self.controller
        )

    def evento_ventana_fuente(self):
        self.fuente_objeto = FontSettings(master=self)

    def evento_acerca_de_ventana(self):
        self.acerca_de_objeto = About(self)

    def evento_grafica_mensual(self):

        # Configurar botones para cambiar entre meses
        self.change_nav_config_to_month()
        # Cambia el encabezado del frame control
        self.top_nav_bar.update_header(self.controller.get_month_header())
        # Calcula el rendimiento que ira en la barra
        self.monthly_performance_avg = self.controller.get_monthly_performance_avg()
        # Configura la barra con el rendimiento mensual
        self.performance_bar.set(self.monthly_performance_avg / 100)
        self.performance_label.configure(
            text=f"{self.monthly_performance_avg}%")
        # Muestra el frame de la grafica mensual
        self.show_monthly_graph()
        self.monthly_graph.frame_botones_navegacion.tkraise()

    def evento_marcar_ayer(self):

        self.estado_boton_marcar_ayer = not self.estado_boton_marcar_ayer
        if self.estado_boton_marcar_ayer:
            self.frame_btn_completar_ayer_contenedor.tkraise()
            self.fecha_hoy_label.configure(text=self.headers[4])
        else:
            self.fecha_hoy_label.configure(text=self.headers[0])
            self.check_buttons_today_frame.tkraise()

    def evento_anio_anterior(self):
        # Si ya existe una gráfica previa, destruirla
        if hasattr(self.yearly_graph,
                   "frame_grafica_anual") and self.yearly_graph.frame_grafica_anual:
            self.yearly_graph.frame_grafica_anual.destroy()
            self.yearly_graph.frame_grafica_anual = None
            self.yearly_graph.canvas_grafica = None
        # actualiza la fecha
        self.controller.go_previous_year()
        self.refresh_week_state()
        # calcular rendimientos de nuevo
        yearly_performance = self.controller.get_yearly_performance()
        # Cambia el encabezado del frame control
        self.label_f_control.configure(text=self.controller.get_year_header())
        # setear barra de progrreso
        self.performance_bar.set(yearly_performance[1] / 100)
        self.performance_label.configure(text=f"{yearly_performance[1]}%")
        self.draw_yearly_graph_frame()

    def evento_anio_siguiente(self):
        # Si ya existe una gráfica previa, destruirla

        if hasattr(self.yearly_graph,
                   "frame_grafica_anual") and self.yearly_graph.frame_grafica_anual:
            self.yearly_graph.frame_grafica_anual.destroy()
            self.yearly_graph.frame_grafica_anual = None
            self.yearly_graph.canvas_grafica = None

            # actualiza la fecha
        self.controller.go_next_year()
        self.refresh_week_state()
        # calcular rendimientos de nuevo
        rend = self.controller.get_yearly_performance()
        # Cambia el encabezado del frame control
        self.label_f_control.configure(text=self.controller.get_year_header())
        # setear barra de progrreso
        self.performance_bar.set(rend[1] / 100)
        self.performance_label.configure(text=f"{rend[1]}%")
        self.draw_yearly_graph_frame()

    def go_to_previous_week_event(self):
        self.controller.go_previous_week()
        self.refresh_week_state()
        self.top_nav_bar.update_header(self.headers[1])
        self.update_table_and_dates(None)

    def go_to_next_week_event(self):
        self.controller.go_next_week()
        self.refresh_week_state()
        self.top_nav_bar.update_header(self.headers[1])
        self.update_table_and_dates(None)

    def go_to_previous_month_event(self):

        if hasattr(self.monthly_graph,
                   "frame_grafica_mensual") and self.monthly_graph.frame_grafica_mensual:
            self.monthly_graph.frame_grafica_mensual.destroy()
            self.monthly_graph.frame_grafica_mensual = None
            self.monthly_graph.canvas_grafica = None

        self.controller.go_previous_month()
        self.refresh_week_state()
        self.monthly_performance_avg = self.controller.get_monthly_performance_avg()
        self.top_nav_bar.update_header(self.controller.get_month_header())
        self.performance_bar.set(self.monthly_performance_avg / 100)
        self.performance_label.configure(
            text=f"{self.monthly_performance_avg}%")
        self.show_monthly_graph()

    def go_to_next_month_event(self):

        # Si ya existe una gráfica previa, destruirla
        if hasattr(self.monthly_graph,
                   "frame_grafica_mensual") and self.monthly_graph.frame_grafica_mensual:
            self.monthly_graph.frame_grafica_mensual.destroy()
            self.monthly_graph.frame_grafica_mensual = None
            self.monthly_graph.canvas_grafica = None

        self.controller.go_next_month()
        self.refresh_week_state()
        self.monthly_performance_avg = self.controller.get_monthly_performance_avg()
        self.top_nav_bar.update_header(text=self.controller.get_month_header())
        self.performance_bar.set(self.monthly_performance_avg / 100)
        self.performance_label.configure(
            text=f"{self.monthly_performance_avg}%")
        # Muestra el frame de la grafica mensual
        self.show_monthly_graph()

    def habit_check_event(self, habit_name):
        self.controller.check_habit_today(habit_name)
        self.update_table_and_dates(None)
        self.disable_habit_button(habit_name)

    def disable_habit_button(self, habit_name):
        # Actualizar botón: cambiar texto y deshabilitar
        if hasattr(
                self, "botones_habitos") and habit_name in self.habit_check_buttons:
            boton = self.habit_check_buttons[habit_name]
            boton.configure(
                text=f"{habit_name} - Completado!",
                state="disabled")