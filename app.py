"""
Main entry point for the Habit Tracker application.

This module acts as the Composition Root, where all dependencies 
(database, repositories, services, and controllers) are instantiated 
and injected before starting the graphical user interface.
"""

import sys
import ctypes
from typing import NoReturn

# Domain Services
from domain.calendar_service import CalendarService
from domain.executions_service import ExecutionService
from domain.habit_service import HabitService
from domain.metrics_service import MetricsService
from domain.quote_service import QuoteService
from domain.reset_service import ResetService
from domain.goal_service import GoalService
from domain.style_service import StyleService
from domain.settings_service import SettingsService

# Infrastructure
from infrastructure.database.habit_config_repo import HabitConfigRepository
from infrastructure.database.habit_repo import HabitRepository
from infrastructure.database.quote_repo import QuoteRepository
from infrastructure.database.goal_repo import GoalRepository
from infrastructure.database.executions_repo import ExecutionsRepository
from infrastructure.database.sqlite_db import SQLiteDB
from infrastructure.config.config_manager import ConfigManager
from infrastructure.config.theme_loader import load_theme_file

# UI and Core
from core.app_controller import AppController
from ui.main_window import MainWindow

# Utilities
from utils.paths import data_path

# Application Constants
APP_VERSION: str = "2.1"
APP_USER_MODEL_ID: str = "edgar.habittracker.app"
DB_PATH: str = data_path('habit_tracker.db')
CONFIG_PATH: str = data_path('settings.json')


def _setup_windows_taskbar_icon(app_id: str) -> None:
    """
    Sets the Explicit App User Model ID for Windows OS.
    
    This ensures the application icon groups correctly in the Windows taskbar 
    rather than falling back to the default Python icon. It safely ignores 
    the operation if not running on Windows.

    Args:
        app_id (str): The unique identifier for the application.
    """
    if sys.platform == "win32":
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        except (AttributeError, OSError) as error:
            # Silently ignore or log the error; it's non-critical for app execution
            print(f"Warning: Could not set Windows App ID. Details: {error}")


def main() -> None:
    """
    Initializes dependencies, sets up the composition root, and starts the UI loop.
    """
    # 1. OS-specific configurations
    _setup_windows_taskbar_icon(APP_USER_MODEL_ID)

    # 2. Database Initialization
    db_sql = SQLiteDB(DB_PATH)
    db_sql.connect()
    db_sql.initialize()

    # 3. Infrastructure & Repositories Setup
    habit_repo = HabitRepository(db_sql.conn)
    quote_repo = QuoteRepository(db_sql.conn)
    goal_repo = GoalRepository(db_sql.conn)
    execution_repo = ExecutionsRepository(db_sql.conn)
    habit_config_repo = HabitConfigRepository(db_sql.conn)
    
    config_manager = ConfigManager(CONFIG_PATH)

    # 4. Domain Services Setup
    settings_service = SettingsService(config_manager)
    config = settings_service.get_config()

    theme_file = load_theme_file(config)
    style_service = StyleService(config, theme_file)
    
    reset_service = ResetService()
    habit_service = HabitService(habit_repo, habit_config_repo)
    goal_service = GoalService(goal_repo)
    execution_service = ExecutionService(execution_repo)
    quote_service = QuoteService(quote_repo)
    
    calendar_service = CalendarService(
        start_tracking_date=habit_service.get_start_tracking_date()
    )
    metrics_service = MetricsService()

    # 5. Core Controllers Setup
    controller = AppController(
        style_service=style_service,
        settings_service=settings_service,
        habit_service=habit_service,
        executions_service=execution_service,
        calendar=calendar_service,
        quote_service=quote_service,
        metrics_service=metrics_service,
        reset_service=reset_service,
        goal_service=goal_service,
        close_db_conection=db_sql.close
    )

    # 6. UI Initialization
    app = MainWindow(controller, APP_VERSION)
    app.mainloop()


if __name__ == "__main__":
    main()