from core.app_controller import AppController
from domain.calendar_service import CalendarService
from domain.habit_service import HabitService
from domain.metrics_service import MetricsService
from domain.quote_service import QuoteService
from infrastructure.database.habit_repo import HabitRepository
from infrastructure.database.quote_repo import  QuoteRepository
from infrastructure.database.sqlite_db import Database
from infrastructure.database.sqlite_db import SQLiteDB
from ui.main_window import MainWindow
from utils.paths import resource_path
db_path = resource_path('habit_tracker.db')
db_sql = SQLiteDB(db_path)
db_sql.connect()
db_sql.initialize()



db = Database()
habit_repo = HabitRepository(db)
quote_repo = QuoteRepository(db_sql.conn)
habit_service = HabitService(habit_repo)
quote_service = QuoteService(quote_repo)
calendar_service = CalendarService(
    start_tracking_date=habit_repo.get_start_tracking_date()
)

metrics_service = MetricsService(db, calendar_service)
controller = AppController(
    habit_service=habit_service,
    calendar=calendar_service,
    quote_service=quote_service,
    db=db,
    metrics_service=metrics_service,
)


def main():

    app = MainWindow(controller)
    app.mainloop()


if __name__ == "__main__":
    main()
