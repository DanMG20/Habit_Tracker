"""
Module providing goal management capabilities, coordinating quarterly and yearly performance objectives.
"""

import sqlite3
from datetime import date, datetime
from typing import List, Dict, Any, Optional

from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class GoalService:
    """
    Domain service responsible for enforcing business rules and mapping structures for quarterly targets.
    """

    DATE_FORMAT: str = "%Y-%m-%d"

    QUARTER_PERIODS: Dict[int, str] = {
        1: "1-13",
        2: "14-26",
        3: "27-39",
        4: "40-52",
    }

    PERIOD_TO_INT: Dict[str, int] = {
        "1-13": 1,
        "14-26": 2,
        "27-39": 3,
        "40-52": 4,
    }

    def __init__(self, goal_repo: Any) -> None:
        """
        Initializes the GoalService injecting its data persistence layer handler.

        Args:
            goal_repo (Any): The repository interface providing persistent table operations.
        """
        self.goal_repo: Any = goal_repo

    def _map_row_to_goal(self, row: sqlite3.Row) -> Dict[str, Any]:
        """
        Private helper method to map a single persistent infrastructure row into a core domain dictionary.
        """
        completed_at_val = row["completed_at"]
        created_at_val = row["created_at"]

        return {
            "id": row["id"],
            "goal_name": row["goal_name"],
            "description": row["description"],
            "period_year": row["period_year"],
            "period_quarter": self.QUARTER_PERIODS.get(row["period_quarter"], "Unknown"),
            "is_completed": bool(row["is_completed"]),
            "completed_at": datetime.strptime(completed_at_val, self.DATE_FORMAT).date() 
                            if completed_at_val is not None else None,
            "created_at": datetime.strptime(created_at_val, self.DATE_FORMAT).date()
                            if created_at_val is not None else None
        }

    def get_all(self) -> List[Dict[str, Any]]:
        rows = self.goal_repo.get_all()
        return [self._map_row_to_goal(row) for row in rows]

    def get_from_quarter(self, quarter_str: str, year: int) -> List[Dict[str, Any]]:
        int_quarter: int = self.convert_period(quarter_str)
        rows = self.goal_repo.get_from_quarter(int_quarter, year)
        
        logger.debug(f"Filtering metrics context. Quarter: '{quarter_str}' Mapped: {int_quarter}, Year: {year}")
        return [self._map_row_to_goal(row) for row in rows]

    def get_all_per_year(self, year: int) -> List[Dict[str, Any]]: 
        rows = self.goal_repo.get_all_per_year(year)
        return [self._map_row_to_goal(row) for row in rows]

    def get_completed_on_year(self, year: int) -> List[Dict[str, Any]]:
        rows = self.goal_repo.get_completed_on_year(year)
        return [self._map_row_to_goal(row) for row in rows]

    def get_rate_per_year(self, year: int) -> str: 
        completed_count: int = len(self.get_completed_on_year(year))
        total_count: int = len(self.get_all_per_year(year))
        return f"({completed_count}/{total_count})"

    def complete_goal(self, goal_id: int, target_date: date) -> None:
        date_str: str = target_date.strftime(self.DATE_FORMAT)
        self.goal_repo.complete(goal_id, date_str, 1)
        logger.info(f"Goal ID {goal_id} successfully updated to verified completion state on {date_str}.")


    def update(self, goal_id: int, new_name: str, new_period: str, new_year: int) -> None:
        mapped_period: int = self.convert_period(new_period)
        self.goal_repo.update(goal_id, new_name, mapped_period, new_year)
        logger.info(f"Parameters successfully propagated to data layer for updated Goal ID {goal_id}.")

    def convert_period(self, str_period: str) -> int:
        return self.PERIOD_TO_INT[str_period]

    def insert(self, name: str, year: int, period: str, created_at: date) -> None:
        created_at_str: str = created_at.strftime(self.DATE_FORMAT)
        mapped_period: int = self.convert_period(period)
        self.goal_repo.insert(name, "DEFAULT", int(year), mapped_period, created_at_str)
        logger.info(f"New goal entity '{name}' successfully queued and created.")

    def delete_by_id(self, goal_id: int) -> None: 
        self.goal_repo.delete_by_id(goal_id)
        logger.info(f"Target goal ID {goal_id} successfully detached and removed from infrastructure table.")