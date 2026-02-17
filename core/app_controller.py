from datetime import datetime
from core.runtime import restart_application
from infrastructure.config import config_manager
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
        self.fecha_guardada = datetime.now().date()

        self.today= self.calendar_service.get_today()
        self.load_config()
        self.quote_service.initialize_quotes()
        self.load_phrase()


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

    def habit_file_exists(self):
        return self.habit_service.habit_file_exists()

    def load_habits(self):
        self.habit_service.load_habits()

    def get_habit_by_id(self,habit_id): 
        return self.habit_service.get_by_id(habit_id)
    
    def get_habit_categories(self):
        return self.habit_service.get_categories()
    
    def update_habit(self,habit):
        self.habit_service.update(habit)
    
    def load_habit_register_executions(self):
        return self.habit_service.load_executions()

    def get_current_period(self):
        return self.calendar_service.get_current_period()
    
    def complete_goal(self, goal_id):
        return self.goal_service.complete_goal(goal_id,self.today)
    
    def get_goals(self):
        return self.goal_service.get_all()
    
    def delete_goal(self,goal_id): 
        self.goal_service.delete_by_id(goal_id)

    def update_goal(self, goal_id, goal_name, period, year): 
        self.goal_service.update(goal_id, goal_name, period, year)
        
    def add_goal(self,goal):
        logger.warning("Fix this code")
        self.goal_service.insert(goal[0][0], goal[0][2],goal[0][1] , self.today)


    def get_current_years(self):
        return self.calendar_service.get_current_years()
    
    def verify_date(self):

        hoy = datetime.now().date()
        if hoy != self.fecha_guardada:
            self.fecha_guardada = hoy
            self.update_app_state()
        return self.fecha_guardada
    
    def build_view_state(self):
        """
        Construye todo el estado necesario para renderizar la UI.
        La UI NO debería llamar métodos individuales después de esto.
        """

        # Estado general de fechas y rendimiento
        app_state = self.update_app_state()

        today = self.get_calendar_state()["today"]
        yesterday = self.get_calendar_state()["yesterday"]

        return {
            # ======= HEADERS =======
            "headers": app_state["headers"],

            # ======= PERFORMANCE =======
            "performances": {
                "weekly": app_state["performances"]["weekly"],
                "monthly": app_state["performances"]["monthly"],
                "yearly": app_state["performances"]["yearly"],
            },

            # ======= PANELS =======
            "panels": {
                "today": self.get_check_panel_state(today),
                "yesterday": self.get_check_panel_state(yesterday),
                "update": {
                                "habits": self.get_all_habits(),
                                "completed": []
                            },
                            "delete": {
                                "habits": self.get_all_habits(),
                                "completed": []
                            },
                "goals": {
                        "goals": self.get_goals(),
                        "current_period": self.get_current_period(),
                }
            },

            # ======= HABIT BOARD =======
            "habit_board": self.get_habit_board_state(),

            # ======= GRAPHS =======
            "graphs": {
                "monthly": {
                    "month_range": self.get_month_range(),
                    "daily_performance": self.get_daily_performance_per_month(),
                },
                "yearly": {
                    "month_names": self.get_month_names(),
                    "monthly_performance": self.get_yearly_performance()["monthly"],
                },
            },

            # ======= EXTRA =======
            "current_period": self.get_current_period(),
            "current_years": self.get_current_years(),
            "habit_categories": self.get_habit_categories(),
        }


    def update_app_state(self):
        return {
            "headers": self.calendar_service.get_date_headers(),
            "week_start": self.calendar_service.calculate_week_start(),
            "current_days": self.calendar_service.current_week_days(),
            "performances": {
                "weekly": self.get_weekly_performance(),
                "monthly": self.get_monthly_performance(),
                "yearly": self.get_yearly_performance()["yearly"],
            }
        }
    
    def get_date_headers(self):
        return self.calendar_service.get_date_headers
    
    def get_daily_performance(self):
        return self.metric_service.calc_weekly_performance(
            habits= self.habit_service.get_all(),
            executions = self.executions_service.get_all(),
            week_start= self.calendar_service.calculate_week_start()
            )
    

    def get_weekly_performance(self):
        return self.metrics_service.calc_weekly_performance(
                habits= self.habit_service.get_all(),
                executions = self.executions_service.get_all(),
                week_start= self.calendar_service.calculate_week_start()
            )
    
    def get_yearly_performance(self):
        return self.metrics_service.calc_yearly_performance(
            get_year =self.calendar_service.get_year,
            habits= self.habit_service.get_all(),
            executions = self.executions_service.get_all(),
            ) 
    
    def get_daily_performance_per_month(self): 
        return self.metrics_service.calc_daily_performance_in_month(
            get_month = self.calendar_service.get_month_nav,
            get_year = self.calendar_service.get_year_month_nav,
            executions = self.executions_service.get_all(),
            habits= self.habit_service.get_all(),
        )

    def get_monthly_performance(self):
        return self.metrics_service.calc_average_monthly_performance(
            get_month = self.calendar_service.get_month_nav,
            get_year = self.calendar_service.get_year_month_nav,
            get_month_range = self.calendar_service.get_month_range,
            executions = self.executions_service.get_all(),
            habits = self.habit_service.get_all()
        )

    def get_month_range(self):
        return self.calendar_service.get_month_range()

    def get_habit_board_state(self):
        return {
            "today": self.calendar_service.get_calendar_state()["today"],
            "habits": self.habit_service.get_all(),
            "executions": self.executions_service.get_all(),
            "week_days": self.calendar_service.current_week_days(),
            "week_start": self.calendar_service.calculate_week_start()

        }
    def check_habit_today(self, habit_name):

        date = self.calendar_service.get_calendar_state()["today"]
        self.executions_service.complete_habit_on_date(habit_name,date)
        self.rendimiento_semanal = self.get_weekly_performance()
        logger.info(f"Habit completed today : {habit_name}")

    def check_habit_yesterday(self, habit_name):
        self.habit_service.complete_yesterday(habit_name)
        self.rendimiento_semanal = self.get_weekly_performance()
        logger.info(f"Habit completed yesterday : {habit_name}")

    def clean_deleted_habits(self):
        return self.habit_service.clean_deleted_habits()

    def get_habits_for_current_date(self, date):
        habits = self.habit_service.get_all()


        return [
            {
                "id": h["id"],
                "habit_name": h["habit_name"],
                "execution_days": (h["execution_days"]),
                "creation_date": h["creation_date"],
                "habit_color": h["habit_color"],
                "category": h["category"],
                "description": h["description"] or "Sin descripción"
            }
            for h in habits
            if self.calendar_service.habit_is_valid_for_date(h["execution_days"], date)
        ]

    def has_habits(self):
        return self.habit_service.habit_file_exists()

    def is_habit_completed_on_date(self, name, date_str):
        return self.habit_service.is_habit_completed(name, date_str)

    def get_month_state(self):
        return {
            "monthly_performance_avg": self.metrics_service.calc_monthly_performance(),
            "header": self.calendar_service.get_month_header(),
        }
  
    def add_new_habit(self,habit): 
        self.habit_service.add_new(habit)
    
    def delete_habit(self,habit_id): 
        self.habit_service.delete_by_id(habit_id)

    
    def get_check_panel_state(self,date):

        return {
            "habits": self.get_habits_for_current_date(date),
            "completed": self.executions_service.get_habits_completed_on_date(date),
        }
    
    def get_all_habits(self):
        return self.habit_service.get_all()


    def get_month_header(self):
        return self.calendar_service.get_month_header()

    def load_phrase(self):
        return self.quote_service.get_quote()

    def load_config(self):
        self.config = config_manager.load_config()
        config_manager.apply_config(config=self.config)

    def change_theme(self, new_theme):
        config_manager.change_theme(self.config, new_theme)

    def change_appearance(self, new_appearance):
        config_manager.change_appearance(self.config, new_appearance)

    def change_font(self, new_font):
        config_manager.change_font(self.config, new_font)

    def load_theme_colors(self):
        return config_manager.load_theme_colors()

    def load_fonts(self):
        return config_manager.build_fonts()


    def get_calendar_state(self):
        return self.calendar_service.get_calendar_state()

    def get_year_header(self):
        return self.calendar_service.get_year_header()

    def get_month_names(self):
        return self.calendar_service.get_month_names()

    def reset_files(self):
        self.close_db_connection()
        self.reset_service.reset_files()

    def close_db_connection(self):
        self.close_db_connection()

    def restart(self): 
        restart_application()