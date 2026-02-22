from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import infrastructure.config.defaults as df
import matplotlib.pyplot as plt

from ui.menu_ui_actions import MenuUIActions
from ui.managers.layout_manager import LayoutManager
from ui.managers.ui_refresh_coordinator import UIRefreshCoordinator
from ui.managers.navigation_manager import NavigationUIManager
from ui.navigation.graph_nav_bar import GraphNavBar
from ui.dialogs.about import AboutWindow
from ui.dialogs.habit_form_view import HabitFormView
from ui.dialogs.windows.crud_windows.quotes_window import QuoteWindow
from ui.dialogs.windows.crud_windows.goals_window import GoalWindow
from ui.dialogs.windows.font_window import FontWindow
from ui.graphs.monthly_graph import MonthlyGraph
from ui.graphs.yearly_graph import YearlyGraph
from ui.panels.graph_goal_panel import GraphGoalPanel
from core.app_state.app_state import AppState,AppMode
from ui.menu import MenuBar
from ui.top_section import TopSection
from utils.paths import icon_path
from utils.window_state import load_window_position, save_window_position
from core.view_manager.view_manager import ViewManager
from core.view_manager.views import Views
from ui.builders.main_ui_actions import MainUIActions
from ui.builders.main_view_builder import MainViewBuilder

from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)

class MainWindow(ctk.CTk):
    def __init__(self, controller, version):
        super().__init__()
        self.version = version
        self.controller = controller
        self.app_state = AppState()
        self.view_manager = ViewManager()
        self._pending_event = None

        self._configure_window()
        self._initialize_services()
        self._create_views()
        self._configure_layouts()
        self._configure_managers()
        self.trigger_refresh("day_changed")
        self.open_window_maximized()
        self.start_date_verification()
        self.protocol("WM_DELETE_WINDOW", self.close_app_event)

    def _configure_window(self):
        self.title("")
        self.after(
            100,
            lambda: self.iconbitmap(icon_path()))
        
        load_window_position(self)

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
        self.create_graph_panel()
        self.define_views()

    def _configure_layouts(self):
        self.define_main_view_layout()
        self.define_add_habit_view_layout()
        self.define_monthly_graph_view_layout()
        self.define_yearly_graph_view_layout()
        self.register_layouts()
        self.register_components()
        self.render_app_mode()
        self._main_grid_config()

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
        self.ui_refresh_coordinator.register(self.monthly_graph)
        self.ui_refresh_coordinator.register(self.yearly_graph)
        self.ui_refresh_coordinator.register(self.performance_bar)
        self.ui_refresh_coordinator.register(self.habit_board)
        self.ui_refresh_coordinator.register(self.today_check_panel)
        self.ui_refresh_coordinator.register(self.yesterday_check_panel)
        self.ui_refresh_coordinator.register(self.delete_check_panel)
        self.ui_refresh_coordinator.register(self.update_check_panel)
        self.ui_refresh_coordinator.register(self.goal_panel)
        self.ui_refresh_coordinator.register(self.top_nav_bar)
        self.ui_refresh_coordinator.register(self.date_header)
        self.ui_refresh_coordinator.register(self.top_section)
        self.ui_refresh_coordinator.register(self.graph_goal_panel)

    def refresh_ui(self):
        view_state = self.controller.build_view_state()
        self.ui_refresh_coordinator.refresh(
            view_state,
            self.app_state.mode,
            self.view_manager.current_view,
            event=self._pending_event
        )
        self._pending_event = None

    def trigger_refresh(self, event_type):
        self._pending_event = event_type
        self.refresh_ui()

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
            (self.habit_form_view.header_frame, dict(row=2, column=0, columnspan=3, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.habit_form_view.left_panel, dict(column=0, row=3, rowspan=3, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self. habit_form_view.right_panel,dict(row=3,column=1,columnspan=2,rowspan=3,sticky="nsew",padx=df.PADX,pady=df.PADY,)),
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
            columnspan=2,
            sticky="nsew",
            rowspan=3,
            padx=df.PADX,
            pady=df.PADY,)),

            (self.graph_nav_bar, dict(row=2, column=0, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.top_nav_bar, dict(row=2, column=2, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.performance_bar, dict(row=2, column=1, sticky="nsew", padx=df.PADX, pady=df.PADY)),

            (self.graph_goal_panel, dict(row=3, column=2, rowspan = 3, sticky="nsew", padx=df.PADX, pady=df.PADY))
            
                ]


    def create_navigation_manager(self): 
        self.navigation_manager = NavigationUIManager(
            controller=self.controller,
            top_nav_bar=self.top_nav_bar,
            graph_nav_bar=self.graph_nav_bar,
            trigger_refresh=self.trigger_refresh,
            go_to_monthly_graph=self.go_to_monthly_graph_view,
            go_to_yearly_graph=self.go_to_yearly_graph_view,
        )


    def _build_ui_actions(self) -> MainUIActions:

        return MainUIActions(
            confirm_delete_habit=self.delete_habit,
            update_habit_event=self.update_habit_event,
            habit_check_event=self.habit_check_event,
            check_habit_yesterday_event=self.check_habit_yesterday_event,

            show_delete_panel=self.show_delete_panel,
            show_update_panel=self.show_update_check_panel,
            show_yesterday_panel=self.show_check_yesterday_panel,
            show_today_panel=self.show_today_check_panel,
            show_goals_panel=self.show_goals_panel,

            go_to_add_habit_view=self.go_to_add_habit_view,
            go_to_graph_view=self.go_to_monthly_graph_view,
        )


    def _build_ui_menu_actions(self) -> MenuUIActions:
        return MenuUIActions(
            open_font =self.open_font_window,
            reset_files=self.reset_files_event,
            open_add_quote=self.open_add_quote_window,
            open_add_goal =self.open_add_goal_window,
            open_about = self.open_about_window,
            change_appearance= self.change_appearance_event,
            change_theme = self.change_theme_event,
            )

    def create_main_view(self):

        actions = self._build_ui_actions()

        views = MainViewBuilder.build(
            master=self,
            style_settings=self.styles,
            actions=actions
        )

        self.top_nav_bar = views.top_nav_bar
        self.date_header = views.date_header
        self.performance_bar = views.performance_bar
        self.goal_panel = views.goal_panel
        self.delete_check_panel = views.delete_check_panel
        self.update_check_panel = views.update_check_panel
        self.yesterday_check_panel = views.yesterday_check_panel
        self.today_check_panel = views.today_check_panel
        self.habit_board = views.habit_board
        self.bottom_nav_bar = views.bottom_nav_bar

        
    def render_internal_view(self,current):
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
            self.render_internal_view(self.view_manager.current_view)
        elif mode == AppMode.ADD_HABIT:
            self.habit_form_view.set_view_mode("add")
            self.layout_manager.show("habit_form")      
        elif mode == AppMode.UPDATE_HABIT:
            self.habit_form_view.set_view_mode("edit")
            self.layout_manager.show("habit_form")
        elif mode == AppMode.MONTHLY_GRAPH:
            self.layout_manager.show("monthly_graph")
        elif mode == AppMode.YEARLY_GRAPH:
            self.layout_manager.show("yearly_graph")

    def draw_menu_bar(self):

        menu_actions = self._build_ui_menu_actions()
        self.menu_bar = MenuBar(
            master =self,
            actions = menu_actions,
            styles= self.styles
            )
    def create_top_section(self):
        self.top_section = TopSection(
            self,
            self.styles,
        )

    def create_yearly_graph(self):
        self.yearly_graph = YearlyGraph(
            master=self,
            style_settings=self.styles
        )

    def create_monthly_graph(self):
    
        self.monthly_graph = MonthlyGraph(
            master=self,
            style_settings=self.styles
        )

    def start_date_verification(self):
        if self.controller.verify_date():
            logger.info("Day changed → full UI refresh")
            self.trigger_refresh("day_changed")
        self.after(300000, self.start_date_verification)

    def create_habit_form_view(self):
        self.habit_form_view = HabitFormView(
            master=self,
            styles=self.styles,
            go_to_main_view = self.go_to_main_view,
            create_habit_callback=self.add_new_habit_event,
            update_habit_callback= self.update_habit,
            get_categories_callback=self.controller.get_habit_categories
        )

    def create_graph_nav_bar(self): 

        self.graph_nav_bar = GraphNavBar(
            master = self, 
            style_settings= self.styles,
            go_to_main_view= self.go_to_main_view
    
        )

    def create_graph_panel(self):
        self.graph_goal_panel = GraphGoalPanel(
            master = self, 
            style_settings= self.styles
        )

    def _main_grid_config(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

    def go_to_add_habit_view(self):
        self.app_state.mode = AppMode.ADD_HABIT
        self.render_app_mode()

    def go_to_main_view(self):
        self.app_state.mode = AppMode.NORMAL
        self.navigation_manager.set_weekly_mode()
        self.render_app_mode()
        self.trigger_refresh("view_changed")

    def go_to_monthly_graph_view(self):
        self.app_state.mode = AppMode.MONTHLY_GRAPH
        self.navigation_manager.set_monthly_mode()
        self.render_app_mode()
        self.trigger_refresh("graph_changed")

    def go_to_yearly_graph_view(self):
        self.app_state.mode = AppMode.YEARLY_GRAPH
        self.navigation_manager.set_yearly_mode()
        self.render_app_mode()
        self.trigger_refresh("graph_changed")

    def update_habit_event(self,habit_id):
        habit = self.controller.get_habit_by_id(habit_id)
        self.app_state.mode = AppMode.UPDATE_HABIT
        self.habit_form_view.load_habit(habit)
        self.render_app_mode()
        

    def delete_habit(self, id):
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
            self.trigger_refresh("habit_changed")

            

    def delete_goal(self,id):
        self.controller.delete_goal(id)
        self.trigger_refresh("goal_changed")

    def add_goal(self,goal):
        self.controller.add_goal(goal)
        self.trigger_refresh("goal_changed")

    def update_goal(self,id,name,period,year): 
        self.controller.update_goal(id,name,period,year)
        self.trigger_refresh("goal_changed")

    #===========================================Open windows===================================
    def open_font_window(self):
        self.font_window = FontWindow(
            master=self,
            styles=self.styles,
            update_font=self.change_font_event
            )
        
    def open_add_quote_window(self):
        self.add_quote_window  = QuoteWindow(
            master= self,
            styles= self.styles,
            on_add_quote= self.controller.add_quotes,
            get_quotes=self.controller.get_quotes,
            on_delete_quote=self.controller.delete_quote,
            on_update_quote=self.controller.update_quote,
        )
    def open_add_goal_window(self):
        self.add_goal_window  = GoalWindow(
            master= self,
            styles= self.styles,
            on_add= self.add_goal,
            get_rows=self.controller.get_goals,
            on_delete=self.delete_goal,
            on_update=self.update_goal,
            current_years=self.controller.get_current_years(),
        )


    def open_about_window(self):
        self.about_window = AboutWindow(
            master = self,
            version =self.version,
            styles =self.styles,
            )

    #============================================show panels====================
    def show_delete_panel(self):
        if self.view_manager.current_view == Views.DELETE:
            return
        self.view_manager.open_view(Views.DELETE)
        self.render_internal_view(self.view_manager.current_view)

    def show_update_check_panel(self):
        if self.view_manager.current_view == Views.UPDATE:
            return
        self.view_manager.open_view(Views.UPDATE)
        self.render_internal_view(self.view_manager.current_view)

    def show_check_yesterday_panel(self):
        if self.view_manager.current_view == Views.YESTERDAY: 
            return
        self.view_manager.open_view(Views.YESTERDAY)
        self.render_internal_view(self.view_manager.current_view)
        self.trigger_refresh("view_changed")


    def show_today_check_panel(self):
        if self.view_manager.current_view == Views.TODAY: 
            return
        self.view_manager.open_view(Views.TODAY)
        self.render_internal_view(self.view_manager.current_view)
        self.trigger_refresh("view_changed")

    def show_goals_panel(self):
        if self.view_manager.current_view == Views.GOAL:
            return
        self.view_manager.open_view(Views.GOAL)
        self.render_internal_view(self.view_manager.current_view)

    def update_habit(self,habit):
        self.controller.update_habit(habit)
        self.trigger_refresh("habit_changed")

    def add_new_habit_event(self,habits):
        self.controller.add_new_habit(habits)
        self.trigger_refresh("habit_changed")

    def complete_goal_event(self,goal_id): 
        self.controller.complete_goal(goal_id)
        self.trigger_refresh("goal_changed")

    def habit_check_event(self, habit_id):
        self.controller.check_habit_today(habit_id)
        self.trigger_refresh("habit_changed")

    def check_habit_yesterday_event(self, habit_id):
        self.controller.check_habit_yesterday(habit_id)
        self.trigger_refresh("habit_changed")

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
            self.controller.update_theme(new_theme)
            self.restart()


    def change_appearance_event(self, new_appearance=None):
        self.controller.update_appearance(new_appearance)
        self.trigger_refresh("appearance_changed")
   

    def change_font_event(self, new_font=None):
        msg = CTkMessagebox(
            master=self,
            title="Confirmación",
            message=f"¿Estás seguro de que deseas cambiar la fuente a '{new_font}'? \n es necesario reiniciar la aplicación",
            font=self.fonts["SMALL"],
            icon="question",
            option_1="No",
            option_2="Sí",
        )
        response = msg.get()
        if response == "Sí":
            self.controller.update_font(new_font)
            self.restart()

    def restart(self):
        self.close_app_event()
        self.controller.restart()

    def reset_files_event(self):
        msg = CTkMessagebox(
            master=self,
            title="Confirmación",
            message=f"¿Estás seguro de que deseas RESTAURAR LA APLICACIÓN ?  se borrarán TODOS tus datos (NO SE PUEDE DESHACER !!!)",
            font=self.fonts["SMALL"],
            icon="question",
            option_1="No",
            option_2="Sí",
        )
        response = msg.get()
        if response == "Sí":
            self.controller.reset_files()
            self.restart()

    def close_app_event(self):
        save_window_position(self)
        try:
            self.unbind("<Configure>")
            plt.close("all")
        except:
            pass
        self.quit()
        self.destroy()

    def load_style_settings(self):
        self.styles = self.controller.get_styles()
        self.theme_colors = self.styles["colors"]
        self.fonts = self.styles["fonts"]
        self.current_font = self.styles["current_font"]

    def open_window_maximized(self):
        self.after_idle(lambda: self.state("zoomed"))
