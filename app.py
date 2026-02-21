from core.app_controller import AppController
from domain.calendar_service import CalendarService
from domain.executions_service import ExecutionService
from domain.habit_service import HabitService
from domain.metrics_service import MetricsService
from domain.quote_service import QuoteService
from domain.reset_service import ResetService
from domain.goal_service import GoalService
from domain.style_service import StyleService
from domain.settings_service import SettingsService
from infrastructure.database.habit_repo import HabitRepository
from infrastructure.database.quote_repo import  QuoteRepository
from infrastructure.database.goal_repo import  GoalRepository
from infrastructure.database.executions_repo import ExecutionsRepository
from infrastructure.database.sqlite_db import SQLiteDB
from infrastructure.config.config_manager import ConfigManager
from infrastructure.config.theme_loader import load_theme_file
from ui.main_window import MainWindow
from utils.paths import resource_path
DB_PATH = resource_path('habit_tracker.db')
CONFIG_PATH = resource_path ('settings.json')



#========================================
#         VERSION 
#========================================

version = "2.0"
db_sql = SQLiteDB(DB_PATH)
db_sql.connect()
db_sql.initialize()

habit_repo = HabitRepository(db_sql.conn)
quote_repo = QuoteRepository(db_sql.conn)
goal_repo = GoalRepository(db_sql.conn)
execution_repo = ExecutionsRepository(db_sql.conn)
config_manager = ConfigManager(CONFIG_PATH)


settings_service = SettingsService(config_manager)

config = settings_service.get_config()

theme_file = load_theme_file(config)
style_service = StyleService(config,theme_file)
reset_service = ResetService()
habit_service = HabitService(habit_repo)
goal_service = GoalService(goal_repo)
execution_service = ExecutionService(execution_repo)
quote_service = QuoteService(quote_repo)
calendar_service = CalendarService(
    start_tracking_date=habit_service.get_start_tracking_date()
)
metrics_service = MetricsService()


controller = AppController(
    style_service= style_service,
    settings_service = settings_service,
    habit_service=habit_service,
    executions_service = execution_service,
    calendar=calendar_service,
    quote_service=quote_service,
    metrics_service=metrics_service,
    reset_service =reset_service,
    goal_service=goal_service,
    close_db_conection= db_sql.close
)


def main():

    app = MainWindow(controller,version)
    app.mainloop()

    
if __name__ == "__main__":
    main()
