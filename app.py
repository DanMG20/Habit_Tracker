from core.app_controller import AppController
from domain.calendar_service import CalendarService
from domain.habit_service import HabitService
from domain.metrics_service import MetricsService
from domain.phrase_service import PhraseService
from infrastructure.database.repositories import HabitRepository, PhraseRepository
from infrastructure.database.sqlite_db import Database
from ui.main_window import MainWindow

db = Database()
habit_repo = HabitRepository(db)
phrase_repo = PhraseRepository(db)
habit_service = HabitService(habit_repo)
phrase_service = PhraseService(phrase_repo)
calendar_service = CalendarService(
    start_tracking_date=habit_repo.get_start_tracking_date()
)

metrics_service = MetricsService(db, calendar_service)
controller = AppController(
    habit_service=habit_service,
    calendar=calendar_service,
    phrase_service=phrase_service,
    db=db,
    metrics_service=metrics_service,
)


def main():
    # configurar_logging()

    app = MainWindow(controller)
    app.mainloop()


if __name__ == "__main__":
    main()
