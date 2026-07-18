"""
Module managing habit domain business logic, coordinating lifecycle configurations and schedules.
"""

import json
import sqlite3
from datetime import date, datetime, timedelta
from typing import List, Dict, Any, Optional

from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class HabitService:
    """
    Domain service responsible for enforcing business rules regarding habits and their versioned states.
    """

    DATE_FORMAT: str = "%Y-%m-%d"
    DEFAULT_DESCRIPTION: str = "No description provided"

    def __init__(self, habit_repository: Any, habit_config_repository: Any) -> None:
        """
        Initializes the HabitService injecting concrete data and configuration access repositories.

        Args:
            habit_repository (Any): Repository layer managing base habit persistence.
            habit_config_repository (Any): Repository layer managing versioned habit configuration profiles.
        """
        self.habit_repo: Any = habit_repository
        self.habit_config_repo: Any = habit_config_repository

    def _map_row_to_config(self, config_row: sqlite3.Row) -> Dict[str, Any]:
        """
        Private helper method to transform a persistent configuration row into a structured domain payload.
        """
        until_val = config_row["valid_until"]
        return {
            "id": config_row["id"],
            "execution_days": json.loads(config_row["execution_days"]),
            "is_active": bool(config_row["is_active"]),
            "valid_from": datetime.strptime(config_row["valid_from"], self.DATE_FORMAT).date(),
            "valid_until": datetime.strptime(until_val, self.DATE_FORMAT).date() if until_val else None
        }

    def _map_row_to_habit(self, habit_row: sqlite3.Row, configs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Private helper method to safely transform a persistent habit row into a unified core domain dictionary.
        """
        return {
            "id": habit_row["id"],
            "habit_name": habit_row["habit_name"],
            "configs": configs,
            "creation_date": datetime.strptime(habit_row["creation_date"], self.DATE_FORMAT).date(),
            "habit_color": habit_row["habit_color"],
            "category": habit_row["category"],
            "description": habit_row["description"] or self.DEFAULT_DESCRIPTION
        }

    def get_start_tracking_date(self) -> Optional[date]:
        """
        Retrieves the earliest baseline system creation record timestamp.

        Returns:
            Optional[date]: The date entity of the earliest habit, or None if empty.
        """
        raw_date: Optional[str] = self.habit_repo.get_start_tracking_date()
        if raw_date is not None: 
            return datetime.strptime(raw_date, self.DATE_FORMAT).date()
        return None
    
    def get_all(self) -> List[Dict[str, Any]]:
        rows = self.habit_repo.get_all()
        habits: List[Dict[str, Any]] = []
        
        for row in rows:
            configs_raw = self.habit_config_repo.get_all_by_habit_id(row["id"])
            configs = [self._map_row_to_config(c) for c in configs_raw]
            habits.append(self._map_row_to_habit(row, configs))

        return habits

    def get_by_id(self, habit_id: int) -> Optional[Dict[str, Any]]:
        row = self.habit_repo.get_by_id(habit_id)
        if not row:
            logger.warning(f"Habit record matching ID {habit_id} could not be retrieved.")
            return None

        configs_raw = self.habit_config_repo.get_all_by_habit_id(habit_id)
        configs = [self._map_row_to_config(c) for c in configs_raw]
        return self._map_row_to_habit(row, configs)
    
    def delete_by_id(self, habit_id: int) -> None: 
        self.habit_repo.delete_by_id(habit_id)
        logger.info(f"Habit ID {habit_id} along with linked cascades successfully detached.")

    def get_categories(self) -> List[str]:
        return self.habit_repo.get_categories()
    
    def add_new(self, habit_data: Dict[str, Any]) -> None:
        today_date: date = date.today()

        habit_to_insert: tuple = (
            habit_data["name"],
            today_date,
            habit_data["color"],
            habit_data["category"],
            habit_data["description"]
        )

        habit_id: int = self.habit_repo.insert(habit_to_insert)

        initial_config: tuple = (
            habit_id,
            json.dumps(habit_data["execution_days"]),
            1,  # Structural integer active status indicator
            today_date,
            None
        )

        self.habit_config_repo.insert(initial_config)
        logger.info(f"Successfully generated new habit entity profile with generated ID {habit_id}.")

    def update(self, modified_habit: Dict[str, Any]) -> None:
        habit_to_update: tuple = (
            modified_habit["name"],
            modified_habit["color"],
            modified_habit["category"],
            modified_habit["description"],
            modified_habit["id"]
        )

        self.habit_repo.update(habit_to_update)

        habit: Optional[Dict[str, Any]] = self.get_by_id(modified_habit["id"])
        if not habit:
            logger.error(f"Aborting dynamic subprofile update. Missing baseline target ID {modified_habit['id']}.")
            return

        configs: List[Dict[str, Any]] = habit["configs"]
        latest_config: Optional[Dict[str, Any]] = self.get_latest_config(configs)

        new_days: List[bool] = modified_habit["execution_days"]
        new_state: bool = bool(modified_habit["is_active"])

        if latest_config:
            current_days: List[bool] = latest_config["execution_days"]
            current_state: bool = latest_config["is_active"]

            if current_days == new_days and current_state == new_state:
                logger.debug("No baseline version changes captured for internal configurations.")
                return

            yesterday_limit: date = date.today() - timedelta(days=1)
            self.habit_config_repo.close_config(latest_config["id"], yesterday_limit)

        new_config: tuple = (
            modified_habit["id"],
            json.dumps(new_days),
            1 if new_state else 0,
            date.today(),
            None
        )

        self.habit_config_repo.insert(new_config)
        logger.info(f"Successfully versioned and committed new state settings for Habit ID {modified_habit['id']}.")

    def get_latest_config(self, configs: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        return configs[-1] if configs else None
        
    def get_config_for_date(self, configs: List[Dict[str, Any]], target_date: date) -> Optional[Dict[str, Any]]:
        for config in configs:
            if config["valid_from"] <= target_date and (config["valid_until"] is None or config["valid_until"] >= target_date):
                return config
        return None
    
    def is_habit_scheduled_for_date(self, habit_data: Dict[str, Any], target_date: date) -> bool:
        if habit_data["creation_date"] > target_date:
            return False

        config: Optional[Dict[str, Any]] = self.get_config_for_date(habit_data["configs"], target_date)
        if not config or not config["is_active"]:
            return False

      
        weekday_index: int = (target_date.weekday() + 1) % 7
        return bool(config["execution_days"][weekday_index])