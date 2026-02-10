from core.app_controller import AppController
from domain.calendar_service import CalendarService
from domain.executions_service import ExecutionService
from domain.habit_service import HabitService
from domain.metrics_service import MetricsService
from domain.quote_service import QuoteService
from domain.reset_service import ResetService
from infrastructure.database.habit_repo import HabitRepository
from infrastructure.database.quote_repo import  QuoteRepository
from infrastructure.database.executions_repo import ExecutionsRepository
from infrastructure.database.sqlite_db import SQLiteDB
from ui.main_window import MainWindow
from utils.paths import resource_path
db_path = resource_path('habit_tracker.db')
db_sql = SQLiteDB(db_path)
db_sql.connect()
db_sql.initialize()


habit_repo = HabitRepository(db_sql.conn)
quote_repo = QuoteRepository(db_sql.conn)
execution_repo = ExecutionsRepository(db_sql.conn)

reset_service = ResetService()
habit_service = HabitService(habit_repo)
execution_service = ExecutionService(execution_repo)
quote_service = QuoteService(quote_repo)
calendar_service = CalendarService(
    start_tracking_date=habit_service.get_start_tracking_date()
)

metrics_service = MetricsService()
controller = AppController(
    habit_service=habit_service,
    executions_service = execution_service,
    calendar=calendar_service,
    quote_service=quote_service,
    metrics_service=metrics_service,
    reset_service =reset_service
)


def main():

    app = MainWindow(controller)
    app.mainloop()


if __name__ == "__main__":
    main()
