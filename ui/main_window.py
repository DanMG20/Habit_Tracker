import os
import sys

from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from CTkMenuBarPlus import *

import infrastructure.config.defaults as df
from domain.style_service import StyleService
from infrastructure.logging.logger import get_logger
from ui.dialogs.about import AboutWindow
from ui.dialogs.add_habbit import AddHabitFrame
from ui.dialogs.quotes import QuoteWindow
from ui.dialogs.delete_habbit_panel import DeleteHabitCheckPanel
from ui.dialogs.font_settings import FontSettingsWindow
from ui.graphs.monthly_graph import MonthlyGraph
from ui.graphs.yearly_graph import YearlyGraph
from ui.habit_board.habit_board import HabitBoard
from ui.today_check_panel import TodayCheckPanel
from ui.yesterday_check_panel import YesterdayCheckPanel
from ui.menu import MenuBar
from ui.navigation.bottom_nav_bar import BottomNavBar
from ui.navigation.top_nav_bar import TopNavBar
from ui.top_section import TopSection
from utils.paths import icon_path
from utils.tooltip import Tooltip
from utils.window_state import load_window_pos, save_window_pos

logger = get_logger(__name__)


class MainWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        

        self.title("")
        icon = icon_path()
        self.iconbitmap(icon)

        self.controller = controller
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
        
        
        self.draw_delete_habit_panel()
        self.draw_yesterday_check_button_panel()
        self.draw_today_check_button_panel()
        
        self.draw_habit_board()
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
            self.controller.load_phrase()[0],
            self.controller.load_phrase()[1],
            self.fonts,
        )
    def draw_today_check_button_panel(self): 

        self.today_check_panel = TodayCheckPanel(
            master=self,
            fonts=self.fonts,
            theme_colors=self.theme_colors,
            get_state= lambda : self.controller.get_check_panel_state(self.today),
            date = self.today,
            on_date_check=self.controller.check_habit_today
        )

        self.today_check_panel.grid(
            row=3, column=0, sticky="nsew", rowspan=3, padx=df.PADX, pady=df.PADY
        )

    def draw_yesterday_check_button_panel(self): 
        self.yesterday_check_panel =  YesterdayCheckPanel(
            master=self,
            fonts=self.fonts,
            theme_colors=self.theme_colors,
            get_state= lambda :self.controller.get_check_panel_state(self.yesterday),
            date = self.yesterday,
            on_date_check=self.controller.check_habit_today
        )

        self.yesterday_check_panel.grid(
            row=3, column=0, sticky="nsew", rowspan=3, padx=df.PADX, pady=df.PADY
        )

    def draw_delete_habit_panel(self):
        self.delete_check_panel = DeleteHabitCheckPanel(
            master=self,
            fonts=self.fonts,
            theme_colors=self.theme_colors,
            get_habits=self.controller.get_all_habits,
            on_delete=self.confirm_delete_habit,
            
        )
        self.delete_check_panel.grid(
            row=3, column=0, sticky="nsew", rowspan=3,
            padx=df.PADX, pady=df.PADY
        )

    def draw_top_nav_bar(self):
        self.top_nav_bar = TopNavBar(self, self.fonts)
        self.top_nav_bar.update_header(self.headers[1])
        self.top_nav_bar.bind_navigation(
            on_left=self.go_to_previous_week_event, on_right=self.go_to_next_week_event
        )

    def draw_bottom_nav_bar(self):
        self.bottom_nav_bar = BottomNavBar(self, self.fonts)

    def draw_yearly_graph(self):
        self.yearly_graph = YearlyGraph(
            master=self,
            frames_ventana_principal=self.frames_ventana_principal_lista,
            controller=self.controller,
        )

    def draw_habit_board(self):
        self.habit_board = HabitBoard(
            master=self,
            fonts=self.fonts,
            theme_colors=self.theme_colors,
            on_check_yesterday = self.check_habit_yesterday_button_event,
            get_week_state = self.controller.get_week_state,
            date = self.today,
            get_state = self.controller.get_habit_board_state
        )
        self.habit_board.grid( 
            row=4, 
            column=1,
            columnspan= 2, 
            sticky="nsew", 
            padx=df.PADX, 
            pady=df.PADY)

    def draw_monthly_graph(self):
        self.monthly_graph = MonthlyGraph(
            self,
            self.controller,
            self.frames_ventana_principal_lista,
            self.yearly_graph,
        )

    def open_window_maximized(self):
        self.after_idle(lambda: self.state("zoomed"))

    def start_date_verification(self):
        self.controller.verify_date()
        self.after(300000, self.start_date_verification)
        logger.info("Date succesfully verificated")

    def refresh_week_state(self):
        logger.info("OJITO AQUI ")
        date_vars = self.controller.get_week_state()
        self.headers = date_vars["headers"]
        self.week_start = date_vars["week_start"]
        self.current_days = date_vars["current_days"]
        self.rendimiento_semanal = date_vars["weekly_performance"]

    def update_table_and_dates(self, event):
        self.refresh_week_state()
        self.performance_bar.set(self.rendimiento_semanal / 100)
        self.performance_label.configure(text=f"{self.rendimiento_semanal}%")

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
            add_new_habit_event =self.add_new_habit_event,
            frames_ventana_principal=self.frames_ventana_principal_lista,
        )
        self.add_habit_frame.hide()


    def show_monthly_graph(self):
        if hasattr(self, "monthly_graph") and self.monthly_graph:
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
                pady=df.PADY,
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
        

    def frames_ventana_principal(self):
        self.draw_date_frame()
        self.draw_performance_bar_frame()
        self.frames_ventana_principal_lista = [
            self.date_frame,
            self.performance_bar_frame,

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
        self.date_frame = ctk.CTkFrame(self, corner_radius=df.CORNER_RADIUS)
        self.date_frame.grid(row=2, column=0, sticky="nsew", pady=df.PADY, padx=df.PADX)
        self.draw_date()

    def draw_date(self):
        self.fecha_hoy_label = ctk.CTkLabel(
            self.date_frame,
            text=self.headers[0],
            anchor="center",
            font=self.fonts["SUBTITLE"],
        )
        self.fecha_hoy_label.pack(fill="both", expand=True, pady=df.PADY, padx=df.PADX)

    def draw_performance_bar_frame(self):
        self.performance_bar_frame = ctk.CTkFrame(self, corner_radius=df.CORNER_RADIUS)
        self.performance_bar_frame.grid(
            row=2, column=1, sticky="nsew", padx=df.PADX, pady=df.PADY
        )
        self.draw_performance_bar()
        self.draw_performance_label()

    def draw_performance_bar(self):
        self.performance_bar = ctk.CTkProgressBar(
            self.performance_bar_frame,
            # progress_color=estilos.COLOR_CONTRASTE,
            corner_radius=df.CORNER_RADIUS * 2,
        )
        self.performance_bar.pack(
            side="left",
            fill="both",
            expand=True,
            padx=df.PADX * 1.5,
            pady=df.PADY * 1.5,
        )
        self.performance_bar.set(self.rendimiento_semanal / 100)

    def draw_performance_label(self):
        self.performance_label = ctk.CTkLabel(
            self.performance_bar_frame,
            text=f"{self.rendimiento_semanal}%",
            font=self.fonts["SMALL"],
        )
        self.performance_label.pack(
            side="right", fill="both", padx=df.PADX * 2, pady=df.PADY
        )


    def actualizacion_agregar_habito(self):
        self.draw_today_check_button_panel()
        self.update_table_and_dates(None)

    def reiniciar_app(self):
        self.destroy()  # Cierra la ventana
        os.execl(sys.executable, sys.executable, *sys.argv)

    def delete_phrase_event(self, selected_phrase):
        self.controller.delete_selected_phrase(selected_phrase)

    def change_nav_config_to_month(self):
        self.top_nav_bar.bind_navigation(
            on_left=self.go_to_previous_month_event,
            on_right=self.go_to_next_month_event,
        )

    def change_nav_config_to_year(self):
        self.top_nav_bar.bind_navigation(
            on_left=self.previous_year_event, on_right=self.next_year_event
        )

    def check_habit_yesterday_event(self, habit_name):
        self.controller.check_habit_yesterday(habit_name)
        self.rendimiento_semanal = self.controller.get_weekly_performance()
        self.update_table_and_dates(None)
        # Actualizar botón: cambiar texto y deshabilitar
        if (
            hasattr(self, "botones_habitos_ayer")
            and habit_name in self.botones_habitos_ayer
        ):
            boton = self.botones_habitos_ayer[habit_name]
            boton.configure(text=f"{habit_name} - Completado!", state="disabled")

    def add_habit_button_event(self):
        self.add_habit_frame.crear_frame_derecho()
        self.add_habit_frame.name_window_frame()
        for frame in self.add_habit_frame.frames_agregar_habito:
            frame.tkraise()

    def delete_habit_button_event(self):
        self.estado_boton_eliminar_habito = not self.estado_boton_eliminar_habito
        if self.estado_boton_eliminar_habito:
            self.delete_check_panel.tkraise()
        else:
            self.today_check_panel.tkraise()


    def confirm_delete_habit(self, habit_id):
        msg = CTkMessagebox(
            master=self,
            title="Confirmación",
            message=f"¿Eliminar el hábito '{habit_id}'?",
            font=self.fonts["SMALL"],
            icon="question",
            option_1="No",
            option_2="Yes",
        )

        if msg.get() == "Yes":
            self.controller.delete_habit(habit_id)
            self.refresh_ui()

    
    def change_theme_event(self, new_theme=None, nuevo_modo=None):
        msg = CTkMessagebox(
            master=self,
            title="Confirmación",
            message=f"¿Estás seguro de que deseas cambiar el tema a '{new_theme}'? \n es necesario reiniciar la aplicación",
            font=self.fonts["SMALL"],
            icon="question",
            option_1="No",
            option_2="Sí",
        )
        response = msg.get()
        if response == "Sí":
            self.controller.change_theme(new_theme)
            self.reiniciar_app()

    def add_quote_window(self):
        self.add_quote_window = QuoteWindow(
            master=self,
         on_add_quote=self.add_new_quote_event,
         get_quotes=self.controller.get_quotes,
         on_delete_quote=self.controller.delete_quote,
         on_update_quote=self.controller.update_quote)

    def font_window_event(self):
        self.font_settings_window = FontSettingsWindow(master=self)

    def about_window_event(self):
        self.about_window = AboutWindow(self)

    def monthly_graph_event(self):

        # Configurar botones para cambiar entre meses
        self.change_nav_config_to_month()
        # Cambia el encabezado del frame control
        self.top_nav_bar.update_header(self.controller.get_month_header())
        # Calcula el rendimiento que ira en la barra
        self.monthly_performance_avg = self.controller.get_monthly_performance_avg()
        # Configura la barra con el rendimiento mensual
        self.performance_bar.set(self.monthly_performance_avg / 100)
        self.performance_label.configure(text=f"{self.monthly_performance_avg}%")
        # Muestra el frame de la grafica mensual
        self.show_monthly_graph()
        self.monthly_graph.frame_botones_navegacion.tkraise()

    def check_habit_yesterday_button_event(self):

        self.estado_boton_marcar_ayer = not self.estado_boton_marcar_ayer
        if self.estado_boton_marcar_ayer:
            self.yesterday_check_panel.tkraise()
            self.fecha_hoy_label.configure(text=self.headers[4])
        else:
            self.fecha_hoy_label.configure(text=self.headers[0])
            self.today_check_panel.tkraise()

    def previous_year_event(self):
        # Si ya existe una gráfica previa, destruirla
        if (
            hasattr(self.yearly_graph, "frame_grafica_anual")
            and self.yearly_graph.frame_grafica_anual
        ):
            self.yearly_graph.frame_grafica_anual.destroy()
            self.yearly_graph.frame_grafica_anual = None
            self.yearly_graph.canvas_grafica = None
        # actualiza la fecha
        self.controller.go_previous_year()
        self.refresh_week_state()
        # calcular rendimientos de nuevo
        yearly_performance = self.controller.get_yearly_performance()
        # Cambia el encabezado del frame control
        self.top_nav_bar.update_header(self.controller.get_year_header())
        # setear barra de progrreso
        self.performance_bar.set(yearly_performance[1] / 100)
        self.performance_label.configure(text=f"{yearly_performance[1]}%")
        self.draw_yearly_graph_frame()

    def next_year_event(self):
        # Si ya existe una gráfica previa, destruirla

        if (
            hasattr(self.yearly_graph, "frame_grafica_anual")
            and self.yearly_graph.frame_grafica_anual
        ):
            self.yearly_graph.frame_grafica_anual.destroy()
            self.yearly_graph.frame_grafica_anual = None
            self.yearly_graph.canvas_grafica = None

            # actualiza la fecha
        self.controller.go_next_year()
        self.refresh_week_state()
        # calcular rendimientos de nuevo
        rend = self.controller.get_yearly_performance()
        # Cambia el encabezado del frame control
        self.top_nav_bar.update_header(self.controller.get_year_header())
        # setear barra de progrreso
        self.performance_bar.set(rend[1] / 100)
        self.performance_label.configure(text=f"{rend[1]}%")
        self.draw_yearly_graph_frame()

    def go_to_previous_week_event(self):
        response = self.controller.go_previous_week()
        if  response: 
            return 
        else:
            self.refresh_week_state()
            self.habit_board.refresh()
            self.top_nav_bar.update_header(self.headers[1])
            self.update_table_and_dates(None)

    def go_to_next_week_event(self):
        response = self.controller.go_next_week()
        if response:
            return
        else:
            self.refresh_week_state()
            self.habit_board.refresh()
            self.top_nav_bar.update_header(self.headers[1])
            self.update_table_and_dates(None)

    def go_to_previous_month_event(self):

        if (
            hasattr(self.monthly_graph, "frame_grafica_mensual")
            and self.monthly_graph.frame_grafica_mensual
        ):
            self.monthly_graph.frame_grafica_mensual.destroy()
            self.monthly_graph.frame_grafica_mensual = None
            self.monthly_graph.canvas_grafica = None

        self.controller.go_previous_month()
        self.refresh_week_state()
        self.monthly_performance_avg = self.controller.get_monthly_performance_avg()
        self.top_nav_bar.update_header(self.controller.get_month_header())
        self.performance_bar.set(self.monthly_performance_avg / 100)
        self.performance_label.configure(text=f"{self.monthly_performance_avg}%")
        self.show_monthly_graph()

    def go_to_next_month_event(self):

        # Si ya existe una gráfica previa, destruirla
        if (
            hasattr(self.monthly_graph, "frame_grafica_mensual")
            and self.monthly_graph.frame_grafica_mensual
        ):
            self.monthly_graph.frame_grafica_mensual.destroy()
            self.monthly_graph.frame_grafica_mensual = None
            self.monthly_graph.canvas_grafica = None

        self.controller.go_next_month()
        self.refresh_week_state()
        self.monthly_performance_avg = self.controller.get_monthly_performance_avg()
        self.top_nav_bar.update_header(text=self.controller.get_month_header())
        self.performance_bar.set(self.monthly_performance_avg / 100)
        self.performance_label.configure(text=f"{self.monthly_performance_avg}%")
        # Muestra el frame de la grafica mensual
        self.show_monthly_graph()

    def habit_check_event(self, habit_name):
        self.controller.check_habit_today(habit_name)
        self.update_table_and_dates(None)
        self.disable_habit_button(habit_name)

    def disable_habit_button(self, habit_name):
        # Actualizar botón: cambiar texto y deshabilitar
        if hasattr(self, "botones_habitos") and habit_name in self.habit_check_buttons:
            boton = self.habit_check_buttons[habit_name]
            boton.configure(text=f"{habit_name} - Completado!", state="disabled")

    def add_new_quote_event(self,quotes):
        self.controller.add_quotes(quotes)
    

    def refresh_ui(self):
        self.today_check_panel.refresh()
        self.yesterday_check_panel.refresh()
        self.delete_check_panel.refresh()
        self.habit_board.refresh()

    def add_new_habit_event(self,habits):

        self.controller.add_new_habit(habits)
        self.refresh_ui()
