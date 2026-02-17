from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
from CTkMenuBarPlus import *
import infrastructure.config.defaults as df
from domain.style_service import StyleService
from infrastructure.logging.logger import get_logger
from ui.panels.goal_panel import GoalPanel
import matplotlib.pyplot as plt
from ui.managers.layout_manager import LayoutManager
from ui.managers.ui_refresh_coordinator import UIRefreshCoordinator
from ui.managers.navigation_manager import NavigationUIManager
from ui.navigation.graph_nav_bar import GraphNavBar
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
from ui.performance_bar import PerformanceBar
from ui.navigation.bottom_nav_bar import BottomNavBar
from ui.navigation.top_nav_bar import TopNavBar
from ui.top_section import TopSection
from utils.paths import icon_path
from utils.window_state import load_window_pos, save_window_pos
from core.view_manager.view_manager import ViewManager
from core.view_manager.views import Views
from ui.date_header import DateHeader
logger = get_logger(__name__)


class MainWindow(ctk.CTk):
    def __init__(self, controller):
        super().__init__()

        self.controller = controller
        self.app_state = AppState()
        self.view_manager = ViewManager()

        self._configure_window()
        self._initialize_services()
        self._create_views()
        self._configure_layouts()
        self._configure_managers()

        self.refresh_ui()
        self.open_window_maximized()
        self.protocol("WM_DELETE_WINDOW", self.close_app_event)

        
    def _configure_window(self):
        self.title("")
        self.iconbitmap(icon_path())
        load_window_pos(self)

        self.load_style_settings()
        self.configure(fg_color=self.theme_colors["top_frame"])
    def _initialize_services(self):
        self.layout_manager = LayoutManager()
        self.ui_refresh_coordinator = UIRefreshCoordinator()

    def _create_views(self):
        self.draw_menu_bar()
        self.create_top_section()

        self.create_main_view()
        self.create_habit_form_view()

        self.create_monthly_graph()
        self.create_yearly_graph()
        self.create_graph_nav_bar()

        self.define_views()

    def _configure_layouts(self):
        self.define_main_view_layout()
        self.define_add_habit_view_layout()
        self.define_monthly_graph_view_layout()
        self.define_yearly_graph_view_layout()

        self.register_layouts()
        self.register_components()

        self.render_app_mode()
        self.main_grid_config()

    def _configure_managers(self):
        self.create_navigation_manager()



    def define_views(self):
        self.internal_views = {
            Views.TODAY: self.today_check_panel,
            Views.YESTERDAY: self.yesterday_check_panel,
            Views.UPDATE: self.update_check_panel,
            Views.DELETE: self.delete_check_panel,
            Views.GOAL: self.goal_panel,
        }

    def register_layouts(self):

        self.layout_manager.register("main", self.main_view_layout)
        self.layout_manager.register("habit_form",self.habit_form_view_layout)
        self.layout_manager.register("monthly_graph", self.monthly_graph_view_layout)
        self.layout_manager.register("yearly_graph", self.yearly_graph_view_layout)

    def register_components(self):
        self.ui_refresh_coordinator.register(self.monthly_graph, group="graphs")
        self.ui_refresh_coordinator.register(self.yearly_graph, group="graphs")
        self.ui_refresh_coordinator.register(self.performance_bar, group="navigation")
        self.ui_refresh_coordinator.register(self.top_nav_bar, group="navigation")
        self.ui_refresh_coordinator.register(self.habit_board, group="board")
        self.ui_refresh_coordinator.register(self.date_header, group = "navigation")
        self.ui_refresh_coordinator.register(self.today_check_panel, group="panels")
        self.ui_refresh_coordinator.register(self.yesterday_check_panel, group="panels")
        self.ui_refresh_coordinator.register(self.delete_check_panel, group="panels")
        self.ui_refresh_coordinator.register(self.update_check_panel, group="panels")
        self.ui_refresh_coordinator.register(self.goal_panel, group="panels")

    def refresh_ui(self):
        view_state = self.controller.build_view_state()
        self.ui_refresh_coordinator.refresh_all(
            view_state,
            self.app_state.mode,
            self.view_manager.current_view
        )


    def define_main_view_layout(self):
            
        self.main_view_layout = [
            (self.top_nav_bar, dict(row=2, column=2, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.date_header, dict(row=2, column=0, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.goal_panel, dict(row=3, column=0, rowspan=3, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.delete_check_panel, dict(row=3, column=0, rowspan=3, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.yesterday_check_panel, dict(row=3, column=0, rowspan=3, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.update_check_panel, dict(row=3, column=0, rowspan=3, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.performance_bar, dict(row=2, column=1, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.today_check_panel, dict(row=3, column=0, rowspan=3, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.habit_board, dict(row=4, column=1, columnspan=2, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.bottom_nav_bar, dict(row=5, column=1, columnspan=2, sticky="nsew", padx=df.PADX, pady=df.PADY)),
        ]


    def define_add_habit_view_layout(self):

        self.habit_form_view_layout = [
            (self.habit_form_view.name_window_frame, dict(row=2, column=0, columnspan=3, sticky="nsew", padx=df.PADX, pady=df.PADY)),
            (self.habit_form_view.left_frame_container, dict(column=0, row=3, rowspan=3, sticky="nsew", padx=df.PADX, pady=df.PADY)),
            (self. habit_form_view.right_frame_container,dict(row=3,column=1,columnspan=2,rowspan=3,sticky="nsew",padx=df.PADX,pady=df.PADY,)),
        ]


    def define_monthly_graph_view_layout(self):

        self.monthly_graph_view_layout = [
            (self.monthly_graph, dict(row=3,
            column=0,
            columnspan=3,
            sticky="nsew",
            rowspan=3,
            padx=df.PADX,
            pady=df.PADY,)),

            (self.graph_nav_bar, dict(row=2, column=0, sticky="nsew", padx=df.PADX, pady=df.PADY)),
            (self.top_nav_bar, dict(row=2, column=2, sticky="nsew", padx=df.PADX, pady=df.PADY)),
            (self.performance_bar, dict(row=2, column=1, sticky="nsew", padx=df.PADX, pady=df.PADY)),
            
                ]
        
    def define_yearly_graph_view_layout(self):

        self.yearly_graph_view_layout = [
            (self.yearly_graph, dict(row=3,
            column=0,
            columnspan=3,
            sticky="nsew",
            rowspan=3,
            padx=df.PADX,
            pady=df.PADY,)),

            (self.graph_nav_bar, dict(row=2, column=0, sticky="nsew", padx=df.PADX, pady=df.PADY)),
            (self.top_nav_bar, dict(row=2, column=2, sticky="nsew", padx=df.PADX, pady=df.PADY)),
            (self.performance_bar, dict(row=2, column=1, sticky="nsew", padx=df.PADX, pady=df.PADY)),
            
                ]


    def create_navigation_manager(self): 

        self.navigation_manager = NavigationUIManager(
            controller=self.controller,
            top_nav_bar=self.top_nav_bar,
            graph_nav_bar=self.graph_nav_bar,
            refresh_ui=self.refresh_ui,
            go_to_monthly_graph=self.go_to_monthly_graph_view,
            go_to_yearly_graph=self.go_to_yearly_graph_view,
        )

    def create_main_view(self): 
        self.create_top_nav_bar()
        self.create_date_header()
        self.create_performance_bar()
        self.create_goal_panel()
        self.create_delete_habit_panel()
        self.create_yesterday_check_button_panel()
        self.create_today_check_button_panel()
        self.create_update_check_button_panel()
        self.create_habit_board()
        self.create_bottom_nav_bar()

        
    def render_internal_view(self,current):
        current 
        for view, frame in self.internal_views.items():
            if view == current:
                frame.grid()
            else:
                frame.grid_remove()

    def render_app_mode(self):
        mode = self.app_state.mode

        self.layout_manager.hide("main")
        self.layout_manager.hide("habit_form")
        self.layout_manager.hide("monthly_graph")
        self.layout_manager.hide("yearly_graph")

        if mode == AppMode.NORMAL:
            self.layout_manager.show("main")

        elif mode == AppMode.ADD_HABIT:
            self.habit_form_view.set_view_mode("add_habit")
            self.layout_manager.show("habit_form")      
        elif mode == AppMode.UPDATE_HABIT:
            self.habit_form_view.set_view_mode("update_habit")
            self.layout_manager.show("habit_form")
        elif mode == AppMode.MONTHLY_GRAPH:
            self.layout_manager.show("monthly_graph")
        elif mode == AppMode.YEARLY_GRAPH:
            self.layout_manager.show("yearly_graph")





    def draw_menu_bar(self):
        self.menu_bar = MenuBar(self)

    def create_top_section(self):

        self.top_section = TopSection(
            self,
            self.controller.load_phrase()[0],
            self.controller.load_phrase()[1],
            self.fonts,
        )


    def create_today_check_button_panel(self): 

        self.today_check_panel = TodayCheckPanel(
            master=self,
            style_settings = self.style_settings,
            on_date_check=self.habit_check_event,
        )

    def create_update_check_button_panel(self):
        self.update_check_panel = UpdateHabitCheckPanel(
            master = self,
            style_settings = self.style_settings,
            on_edit=self.update_habit_event,

        )

    def create_yesterday_check_button_panel(self): 
        self.yesterday_check_panel =  YesterdayCheckPanel(
            master=self,
            style_settings= self.style_settings,
            on_date_check=self.controller.check_habit_today
        )


    def create_delete_habit_panel(self):
        self.delete_check_panel = DeleteHabitCheckPanel(
            master=self,
            style_settings = self.style_settings,
            on_delete=self.confirm_delete_habit,
            
        )


    def create_top_nav_bar(self):
        self.top_nav_bar = TopNavBar(
            master =self, 
            style_settings=self.style_settings
            )

    def create_performance_bar(self): 
        self.performance_bar = PerformanceBar(
            master=self,
            style_settings=self.style_settings,
        )

    def create_date_header(self): 
        self.date_header = DateHeader(
            master= self, 
            style_settings= self.style_settings,
        )


    def create_bottom_nav_bar(self):
        self.bottom_nav_bar = BottomNavBar(
            master=self,
            style_settings= self.style_settings,
            show_goals_panel = self.show_goals_panel,
            show_edit_panel = self.show_update_check_panel,
            show_delete_panel= self.show_delete_panel,
            go_to_add_habit_view= self.go_to_add_habbit_view,
            go_to_graph_view=self.go_to_monthly_graph_view,
            )


    def create_yearly_graph(self):
        self.yearly_graph = YearlyGraph(
            master=self,
            style_settings=self.style_settings
        )

    def create_habit_board(self):
        self.habit_board = HabitBoard(
            master=self,
            style_settings = self.style_settings,
            show_yesterday_check_panel= self.show_check_yesterday_panel,
        )

    
    def create_goal_panel(self): 
        self.goal_panel = GoalPanel(
            master=self,
            complete_goal=self.complete_goal_event,
            style_settings=self.style_settings,
        )

    def create_monthly_graph(self):
    
        self.monthly_graph = MonthlyGraph(
            master=self,
            style_settings=self.style_settings
        )
    def start_date_verification(self):
        self.controller.verify_date()
        self.after(300000, self.start_date_verification)
        logger.warning("Move this method to scheduler")
        logger.info("Date succesfully verificated")


    def create_habit_form_view(self):
        self.habit_form_view = HabitFormView(
            master=self,
            style_settings=self.style_settings,
            go_to_main_view = self.go_to_main_view,
            add_new_habit_event =self.add_new_habit_event,
            update_habit= self.update_habit,
            get_habit_categories=self.controller.get_habit_categories
        )

    def create_graph_nav_bar(self): 

        self.graph_nav_bar = GraphNavBar(
            master = self, 
            style_settings= self.style_settings,
            go_to_main_view= self.go_to_main_view
    
        )


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




    def go_to_add_habbit_view(self):
        self.app_state.mode = AppMode.ADD_HABIT
        self.render_app_mode()

    def go_to_main_view(self):
        self.app_state.mode = AppMode.NORMAL
        self.navigation_manager.set_weekly_mode()
        self.render_app_mode()

        #self.ui_refresh_coordinator.refresh_group("main")
        self.refresh_ui()


    def go_to_monthly_graph_view(self):
        self.app_state.mode = AppMode.MONTHLY_GRAPH
        self.navigation_manager.set_monthly_mode()
        self.render_app_mode()
        self.refresh_ui()
    def go_to_yearly_graph_view(self):
        self.app_state.mode = AppMode.YEARLY_GRAPH
        self.navigation_manager.set_yearly_mode()
        self.render_app_mode()
        #self.ui_refresh_coordinator.refresh_group("navigation")
        #self.ui_refresh_coordinator.refresh_group("graphs")
        self.refresh_ui()


    def update_habit_event(self,habit_id):
        logger.warning("arreglar que el habito se cargue internamente")
        habit = self.controller.get_habit_by_id(habit_id)
        self.app_state.mode = AppMode.UPDATE_HABIT
        self.habit_form_view.load_habit(habit)
        self.render_app_mode()
        

    def confirm_delete_habit(self, id):
        logger.warning(" arreglar que pase el nombre en vez del id")
        msg = CTkMessagebox(
            master=self,
            title="Confirmación",
            message=f"¿Eliminar el hábito '{id}'?",
            font=self.fonts["SMALL"],
            icon="question",
            option_1="No",
            option_2="Yes",
        )
        if msg.get() == "Yes":
            self.controller.delete_habit(id)
            self.refresh_ui()

    #===========================================Open windows===================================

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
    def open_font_window(self):
        self.font_settings_window = FontSettingsWindow(master=self)

    def open_about_window(self):
        self.about_window = AboutWindow(self)


    #============================================show panels "====================

    def show_delete_panel(self):
        if self.view_manager.current_view == Views.DELETE:
            next_view = self.view_manager.go_back()
        else:
            next_view = self.view_manager.open_view(Views.DELETE)
        self.render_internal_view(next_view)


    def show_update_check_panel(self):
        if self.view_manager.current_view == Views.UPDATE:
            next_view = self.view_manager.go_back()
        else:
            next_view = self.view_manager.open_view(Views.UPDATE)
        self.render_internal_view(next_view)

    def show_check_yesterday_panel(self):
        if self.view_manager.current_view == Views.YESTERDAY:
            next_view = self.view_manager.go_back()
        else:
            next_view = self.view_manager.open_view(Views.YESTERDAY)
        self.render_internal_view(next_view)
        self.refresh_ui()

    def show_goals_panel(self):
        if self.view_manager.current_view == Views.GOAL:
            next_view = self.view_manager.go_back()
        else:
            next_view = self.view_manager.open_view(Views.GOAL)
        self.render_internal_view(next_view)



# EMPIEZA REFACTORRRRRRRRRRRRRRRRRRRRRR DEBAJO DE ESTO SE SUPONE QUE FUNCIONA BIEN 
    def update_habit(self,habit):
        self.controller.update_habit(habit)
        self.refresh_ui()

    def add_new_habit_event(self,habits):
        self.controller.add_new_habit(habits)
        self.refresh_ui()

    def complete_goal_event(self,goal_id): 
        self.controller.complete_goal(goal_id)
        self.refresh_ui()

    def habit_check_event(self, habit_id):
        self.controller.check_habit_today(habit_id)
        self.refresh_ui()

    def check_habit_yesterday_event(self, habit_id):
        self.controller.check_habit_yesterday(habit_id)
        self.refresh_ui()

    def change_theme_event(self, new_theme=None):
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
            self.restart()

    def restart(self):
        self.quit()
        self.close_app_event()
        self.controller.restart()

    def reset_files_event(self):
        self.controller.reset_files()
        self.restart()


    def close_app_event(self):
        save_window_pos(self)
        try:
            self.unbind("<Configure>")
            plt.close("all")
        except:
            pass
        self.destroy()

    def load_style_settings(self):
        style_service = StyleService()
        self.style_settings = style_service.get_style_settings()
        self.theme_colors = self.style_settings["colors"]
        self.fonts = self.style_settings["fonts"]

    def open_window_maximized(self):
        self.after_idle(lambda: self.state("zoomed"))
