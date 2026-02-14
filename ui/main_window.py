import os
import sys

from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from CTkMenuBarPlus import *

import infrastructure.config.defaults as df
from domain.style_service import StyleService
from infrastructure.logging.logger import get_logger
from ui.panels.goal_panel import GoalPanel
from ui.dialogs.about import AboutWindow
from ui.dialogs.habit_form_view import HabitFormView

from ui.dialogs.windows.crud_windows.quotes_window import QuoteWindow
from ui.dialogs.windows.crud_windows.goals_window import GoalWindow
from ui.panels.delete_habbit_panel import DeleteHabitCheckPanel
from ui.dialogs.font_settings import FontSettingsWindow
from ui.graphs.monthly_graph import MonthlyGraph
from ui.graphs.yearly_graph import YearlyGraph
from ui.habit_board.habit_board import HabitBoard
from ui.panels.today_check_panel import TodayCheckPanel
from core.app_state.app_state import AppState,AppMode
from ui.panels.yesterday_check_panel import YesterdayCheckPanel
from ui.panels.edit_habit_panel import UpdateHabitCheckPanel
from ui.menu import MenuBar
from ui.navigation.bottom_nav_bar import BottomNavBar
from ui.navigation.top_nav_bar import TopNavBar
from ui.top_section import TopSection
from utils.paths import icon_path
from utils.window_state import load_window_pos, save_window_pos

from core.view_manager.view_manager import ViewManager
from core.view_manager.views import Views

logger = get_logger(__name__)


class MainWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()

        self.title("")
        icon = icon_path()
        self.iconbitmap(icon)
        
        self.controller = controller

        self.app_state = AppState()
        self.view_manager = ViewManager()
        load_window_pos(self)
        self.load_style_settings()

        self.configure(fg_color=self.theme_colors["top_frame"])

        



        self.refresh_week_state()
        self.width_column_habitos_tabla = 400 #_> esto no sirve de mucho (solo si esta vacio)
        self.today = self.controller.get_calendar_state()["today"]
        self.yesterday = self.controller.get_calendar_state()["yesterday"]
    

        # VISTA CONSTANTE 
        self.draw_menu_bar()
        self.draw_top_section()

        # VISTA PRINCIPAL
        self.create_main_view()
        self.define_main_view_layout()
        self.define_views() 
        # VISTA AGREGAR HABITO
        self.create_add_habit_view()
        self.define_add_habit_view_layout()

        # VISTA GRAFICA 
        #self.draw_yearly_graph()
        #self.draw_monthly_graph()

        self.render_app_mode()
        self.main_grid_config()

        self.start_date_verification()

        self.open_window_maximized()
        self.protocol("WM_DELETE_WINDOW", self.close_app_event)

    def define_views(self):
        self.internal_views = {
            Views.TODAY: self.today_check_panel,
            Views.YESTERDAY: self.yesterday_check_panel,
            Views.UPDATE: self.update_check_panel,
            Views.DELETE: self.delete_check_panel,
            Views.GOAL: self.goal_panel,
        }

    def define_main_view_layout(self):
                
        self.layout_config = [
            (self.top_nav_bar, dict(row=2, column=2, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.date_frame, dict(row=2, column=0, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.goal_panel, dict(row=3, column=0, rowspan=3, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.delete_check_panel, dict(row=3, column=0, rowspan=3, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.yesterday_check_panel, dict(row=3, column=0, rowspan=3, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.update_check_panel, dict(row=3, column=0, rowspan=3, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.performance_bar_frame, dict(row=2, column=1, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.today_check_panel, dict(row=3, column=0, rowspan=3, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.habit_board, dict(row=4, column=1, columnspan=2, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.bottom_nav_bar, dict(row=5, column=1, columnspan=2, sticky="nsew", padx=df.PADX, pady=df.PADY)),
        ]

    def create_main_view(self): 
        self.create_top_nav_bar()
        self.create_date_frame()
        self.create_performance_bar_frame()
        self.create_goal_panel()
        self.create_delete_habit_panel()
        self.create_yesterday_check_button_panel()
        self.create_today_check_button_panel()
        self.create_update_check_button_panel()
        self.create_habit_board()
        self.create_bottom_nav_bar()

        
    def render_internal_view(self,current):
        current 
        print(current)
        for view, frame in self.internal_views.items():
            if view == current:
                frame.grid()
            else:
                frame.grid_remove()

    def render_app_mode(self):
        mode = self.app_state.mode


        self.hide_main_view()
        self.add_habit_view.hide()
        #self.monthly_graph_frame.grid_remove()

        if mode == AppMode.NORMAL:
            self.show_main_view()
            self.add_habit_view.hide()
            #self.monthly_graph_frame.grid_remove()

        elif mode == AppMode.ADD_HABIT:
   
            self.add_habit_view.set_view_mode("add_habit")
            self.add_habit_view.show()
        elif mode == AppMode.UPDATE_HABIT:
            self.add_habit_view.set_view_mode("update_habit")
            self.add_habit_view.show()

        elif mode == AppMode.MONTHLY_GRAPH:
            self.main_content_frame.grid_remove()
            self.monthly_graph_frame.grid()

    def show_main_view(self):

        for widget, config in self.layout_config:
            widget.grid(**config)

    def hide_main_view(self): 

        for widget, config in self.layout_config:
            widget.grid_remove()



    def draw_menu_bar(self):
        self.menu_bar = MenuBar(self)

    def draw_top_section(self):

        self.top_section = TopSection(
            self,
            self.controller.load_phrase()[0],
            self.controller.load_phrase()[1],
            self.fonts,
        )
    def create_today_check_button_panel(self): 

        self.today_check_panel = TodayCheckPanel(
            master=self,
            fonts=self.fonts,
            theme_colors=self.theme_colors,
            get_state= lambda : self.controller.get_check_panel_state(self.today),
            date = self.today,
            on_date_check=self.controller.check_habit_today
        )

    def create_update_check_button_panel(self):
        self.update_check_panel = UpdateHabitCheckPanel(
            master = self,
            fonts = self.fonts,
            theme_colors= self.theme_colors,
            get_habits= self.controller.get_all_habits,
            on_edit=self.update_habit_event,

        )

    def create_yesterday_check_button_panel(self): 
        self.yesterday_check_panel =  YesterdayCheckPanel(
            master=self,
            fonts=self.fonts,
            theme_colors=self.theme_colors,
            get_state= lambda :self.controller.get_check_panel_state(self.yesterday),
            date = self.yesterday,
            on_date_check=self.controller.check_habit_today
        )


    def create_delete_habit_panel(self):
        self.delete_check_panel = DeleteHabitCheckPanel(
            master=self,
            fonts=self.fonts,
            theme_colors=self.theme_colors,
            get_habits=self.controller.get_all_habits,
            on_delete=self.confirm_delete_habit,
            
        )


    def create_top_nav_bar(self):
        self.top_nav_bar = TopNavBar(self, self.fonts)
        self.top_nav_bar.update_header(self.headers[1])
        self.top_nav_bar.bind_navigation(
            on_left=self.go_to_previous_week_event, on_right=self.go_to_next_week_event
        )
        

    def create_bottom_nav_bar(self):
        self.bottom_nav_bar = BottomNavBar(
            master=self,
            fonts= self.fonts,
            show_goals_panel = self.goals_button_event,
            show_edit_panel = self.update_habit_button_event,
             )


    def draw_yearly_graph(self):
        logger.warning("fix _frames")
        self.yearly_graph = YearlyGraph(
            master=self,
            frames_ventana_principal=None,
            controller=self.controller,
        )

    def create_habit_board(self):
        self.habit_board = HabitBoard(
            master=self,
            fonts=self.fonts,
            theme_colors=self.theme_colors,
            on_check_yesterday = self.check_habit_yesterday_button_event,
            get_week_state = self.controller.get_week_state,
            date = self.today,
            get_state = self.controller.get_habit_board_state
        )

        
    def create_goal_panel(self): 
        self.goal_panel = GoalPanel(
            master=self,
            current_period=self.controller.get_current_period(),
            get_goals= self.controller.get_goals,
            complete_goal=self.controller.complete_goal,
            style_settings=self.style_settings,
        )

    def draw_monthly_graph(self):
        
        logger.warning("fix _frames")
        self.monthly_graph = MonthlyGraph(
            self,
            self.controller,
            None,
            self.yearly_graph,
        )

    def open_window_maximized(self):
        self.after_idle(lambda: self.state("zoomed"))

    def start_date_verification(self):
        self.controller.verify_date()
        self.after(300000, self.start_date_verification)
        logger.warning("Move this method to scheduler")
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
        self.theme_colors = style_service._load_theme_colors() ## -> quitar luego
        self.fonts = style_service.build_fonts() ## -> quitar luego
        self.style_settings = style_service.get_style_settings()

    def close_app_event(self):
        save_window_pos(self)
        self.unbind("<Configure>")
        self.controller.close_db_connection()
        for win in self.winfo_children():
            win.destroy()
        self.destroy()
        sys.exit()

    def create_add_habit_view(self):
        self.add_habit_view = HabitFormView(
            master=self,
            style_settings=self.style_settings,
            go_to_main_view = self.go_to_main_view,
            add_new_habit_event =self.add_new_habit_event,
            update_habit= self.update_habit,
            get_habit_categories=self.controller.get_habit_categories
        )


    def define_add_habit_view_layout(self):
        self.add_habit_view.name_window_frame.grid(
            row=2, column=0, columnspan=3, sticky="nsew", padx=df.PADX, pady=df.PADY
        )
        self.add_habit_view.left_frame_container.grid(
            column=0, row=3, rowspan=3, sticky="nsew", padx=df.PADX, pady=df.PADY
        )

        self. add_habit_view.right_frame_container.grid(
            row=3,
            column=1,
            columnspan=2,
            rowspan=3,
            sticky="nsew",
            padx=df.PADX,
            pady=df.PADY,
        )


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



    def main_grid_config(self):

        for columna in range(1, 2):
            self.columnconfigure(columna, weight=1)
        self.rowconfigure(4, weight=1)

    def reset_files_event(self):
        self.controller.reset_files()
        self.reiniciar_app()

    def create_date_frame(self):
        self.date_frame = ctk.CTkFrame(self, corner_radius=df.CORNER_RADIUS)
        self.draw_date()

    def draw_date(self):
        self.today_label = ctk.CTkLabel(
            self.date_frame,
            text=self.headers[0],
            anchor="center",
            font=self.fonts["SUBTITLE"],
        )
        self.today_label.pack(fill="both", expand=True, pady=df.PADY, padx=df.PADX)

    def create_performance_bar_frame(self):
        self.performance_bar_frame = ctk.CTkFrame(self, corner_radius=df.CORNER_RADIUS)

        self.draw_performance_bar()
        self.draw_performance_label()

    def draw_performance_bar(self):
        self.performance_bar = ctk.CTkProgressBar(
            self.performance_bar_frame,
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
        self.today_check_panel.refresh()
        self.update_table_and_dates(None)

    def reiniciar_app(self):
        self.destroy() 
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
        self.app_state.mode = AppMode.ADD_HABIT
        self.render_app_mode()

    def go_to_main_view(self):
        self.app_state.mode = AppMode.NORMAL
        self.render_app_mode()
 
 

    def delete_habit_button_event(self):
        
        if self.view_manager.current_view == Views.DELETE:
            next_view = self.view_manager.go_back()
        else:
            next_view = self.view_manager.open_view(Views.DELETE)
        self.render_internal_view(next_view)


    def update_habit_button_event(self):
        
        if self.view_manager.current_view == Views.UPDATE:
            next_view = self.view_manager.go_back()
        else:
            next_view = self.view_manager.open_view(Views.UPDATE)
        self.render_internal_view(next_view)


    def update_habit_event(self,habit_id):
        habit = self.controller.get_habit_by_id(habit_id)
        self.app_state.mode = AppMode.UPDATE_HABIT
        self.add_habit_view.load_habit(habit)
        self.render_app_mode()
        

    def confirm_delete_habit(self, habit_name):
        msg = CTkMessagebox(
            master=self,
            title="Confirmación",
            message=f"¿Eliminar el hábito '{habit_name}'?",
            font=self.fonts["SMALL"],
            icon="question",
            option_1="No",
            option_2="Yes",
        )

        if msg.get() == "Yes":
            self.controller.delete_habit(habit_name)
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

    def open_add_quote_window(self):
        self.add_quote_window  = QuoteWindow(
            master= self,
            style_settings= self.style_settings,
            on_add_quote= self.controller.add_quotes,
            get_quotes=self.controller.get_quotes,
            on_delete_quote=self.controller.delete_quote,
            on_update_quote=self.controller.update_quote,
        )


    def open_add_goal_window(self):
        self.add_goal_window  = GoalWindow(
            master= self,
            style_settings= self.style_settings,
            on_add= self.controller.add_goal,
            get_rows=self.controller.get_goals,
            on_delete=self.controller.delete_goal,
            on_update=self.controller.update_goal,
            current_years=self.controller.get_current_years(),
        )

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


        if self.view_manager.current_view == Views.YESTERDAY:
            self.today_label.configure(text=self.headers[0])
            next_view = self.view_manager.go_back()
        else:
            next_view = self.view_manager.open_view(Views.YESTERDAY)
            
            self.today_label.configure(text=self.headers[4])
        self.render_internal_view(next_view)


            
    def goals_button_event(self):

        if self.view_manager.current_view == Views.GOAL:
            next_view = self.view_manager.go_back()
        else:
            next_view = self.view_manager.open_view(Views.GOAL)

        self.render_internal_view(next_view)

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
        its_possible = self.controller.go_previous_week()
        if  its_possible: 
            return 
        else:
            self.refresh_week_state()
            self.habit_board.refresh()
            self.top_nav_bar.update_header(self.headers[1])
            self.update_table_and_dates(None)

    def go_to_next_week_event(self):
        its_possible = self.controller.go_next_week()
        if its_possible:
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

    def refresh_ui(self):
        self.today_check_panel.refresh()
        self.yesterday_check_panel.refresh()
        self.delete_check_panel.refresh()
        self.habit_board.refresh()
        self.update_check_panel.refresh()

    def add_new_habit_event(self,habits):

        self.controller.add_new_habit(habits)
        self.refresh_ui()

    def update_habit(self,habit):

        self.controller.update_habit(habit)
        self.refresh_ui()
