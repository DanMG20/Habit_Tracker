from ventanas.VentanaPrincipal import VentanaPrincipal
from infrastructure.database.sqlite_db import Database
from infrastructure.database.repositories import HabitRepository
from domain.habit_service import HabitService
from core.app_controller import AppController
from domain.calendar_service import CalendarService
#from ui.main_window import MainWindow

db = Database()
habit_repo = HabitRepository(db)
habit_service = HabitService(habit_repo)
calendar_service = CalendarService(db)
controller = AppController(
    habit_service=habit_service,
    calendar=calendar_service,
    db=db
)
def main():
    #configurar_logging()

    app = VentanaPrincipal(controller)
    app.mainloop()

if __name__ == "__main__":
    main()