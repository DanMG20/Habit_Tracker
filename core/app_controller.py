from core.runtime import restart_application
from infrastructure.config import config_manager
from core.view_state_builder import ViewStateBuilder
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class AppController:
    def __init__(self,
                  habit_service,
                    calendar,
                    reset_service,
                    executions_service, 
                    metrics_service, 
                    quote_service,
                    goal_service,
                    close_db_conection, 
                    ):
        self.calendar_service = calendar
        self.metrics_service = metrics_service
        self.quote_service = quote_service
        self.reset_service = reset_service
        self.executions_service = executions_service
        self.habit_service = habit_service
        self.goal_service = goal_service
        self.close_db_connection = close_db_conection
        self.view_state_builder = ViewStateBuilder(
            calendar_service=calendar,
            metrics_service=metrics_service,
            goal_service=goal_service,
            habit_service=habit_service,
            executions_service=executions_service,
            quote_service=quote_service,
        )
        self.load_config()

 #========================STATE===================
    def build_view_state(self): 
        return self.view_state_builder.build()
    
 #========================NAV===================
    def go_previous_week(self):
        return self.calendar_service.go_to_previous_week()

    def go_next_week(self):
        return self.calendar_service.go_to_next_week()
 
    def go_to_previous_month(self):
        return self.calendar_service.go_to_previous_month()

    def go_to_next_month(self):
        return self.calendar_service.go_to_next_month()

    def go_to_previous_year(self):
        return self.calendar_service.go_to_previous_year()

    def go_to_next_year(self):
        return self.calendar_service.go_to_next_year()
    
 #========================QUOTES===================

    def get_quote(self):
        return self.quote_service.get_quote()

    def get_quotes(self):
        return self.quote_service.get_all_quotes()
    
    def add_quotes(self, quotes):
        self.quote_service.add_quotes(quotes)

    def update_quote(self,quote_id, new_quote, new_author):
        self.quote_service.update_quote(quote_id,
                                        new_quote, 
                                        new_author) 

    def delete_quote(self, quote_id):
        self.quote_service.delete_selected_quote(quote_id)

 #========================HABITS===================

    def get_habit_by_id(self,habit_id): 
        return self.habit_service.get_by_id(habit_id)
    
    def get_habit_categories(self):
        return self.habit_service.get_categories()
    
    def update_habit(self,habit):
        self.habit_service.update(habit)

    def add_new_habit(self,habit): 
        self.habit_service.add_new(habit)
    
    def delete_habit(self,habit_id): 
        self.habit_service.delete_by_id(habit_id)

    def get_all_habits(self):
        return self.habit_service.get_all()

 #========================GOALS===================
    
    def complete_goal(self, goal_id):
        return self.goal_service.complete_goal(goal_id,self._get_today())
    
    def get_goals(self):
        return self.goal_service.get_all()
    
    def delete_goal(self,goal_id): 
        self.goal_service.delete_by_id(goal_id)

    def update_goal(self, goal_id, goal_name, period, year): 
        self.goal_service.update(goal_id, goal_name, period, year)
        
    def add_goal(self,goal):
        logger.warning("Fix this code")
        self.goal_service.insert(goal[0][0], goal[0][2],goal[0][1] , self._get_today())

 #========================EXECUTIONS===================

    def check_habit_today(self, habit_name):
        self.executions_service.complete_habit_on_date(habit_name,self._get_today())
        logger.info(f"Habit completed today : {habit_name}")

    def check_habit_yesterday(self, habit_name):
        self.executions_service.complete_habit_on_date(habit_name,self._get_yesterday())
        logger.info(f"Habit completed yesterday : {habit_name}")

 #========================CALENDAR===================

    def _get_today(self):
        return self.calendar_service.get_calendar_state()["today"]

    def _get_yesterday(self):
        return self.calendar_service.get_calendar_state()["yesterday"]


    def get_current_period(self):
        return self.calendar_service.get_current_period()
    
    def get_current_years(self):
        return self.calendar_service.get_current_years()
    
    def verify_date(self): 
        return self.calendar_service.has_day_changed()

 #========================STYLE===================

    def load_theme_colors(self):
        return config_manager.load_theme_colors()

    def load_fonts(self):
        return config_manager.build_fonts()


 #========================SETTINGS===================

    def load_config(self):
        self.config = config_manager.load_config()
        config_manager.apply_config(config=self.config)

    def change_theme(self, new_theme):
        config_manager.change_theme(self.config, new_theme)

    def change_appearance(self, new_appearance):
        config_manager.change_appearance(self.config, new_appearance)

    def change_font(self, new_font):
        config_manager.change_font(self.config, new_font)

    def reset_files(self):
        self.close_db()
        self.reset_service.reset_files()

    def close_db(self):
        self.close_db_connection()

    def restart(self): 
        restart_application()