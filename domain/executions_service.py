"""
Module providing execution logging services to record and query habit completion history.
"""

from datetime import date, datetime
from typing import List, Dict, Set, Any, Optional

from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class ExecutionService:
    """
    Domain service responsible for tracking and validating historical habit executions.
    """

    DATE_FORMAT: str = "%Y-%m-%d"

    def __init__(self, execution_repo: Any) -> None:
        """
        Initializes the ExecutionService injecting its concrete data access repository.

        Args:
            execution_repo (Any): The repository interface interacting with execution tables.
        """
        self.execution_repo: Any = execution_repo

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all logged habit executions mapped as dynamic dictionaries.

        Returns:
            List[Dict[str, Any]]: A collection containing full execution history payloads.
        """
        rows = self.execution_repo.get_all()
        executions: List[Dict[str, Any]] = []
        
        for row in rows: 
            executions.append({
                "id": row["id"],
                "habit_id": row["habit_id"],
                "execution_date": datetime.strptime(row["execution_date"], self.DATE_FORMAT).date(),
                "executed": bool(row["executed"])
            })
        return executions

    def is_habit_completed(self, habit_id: int, target_date: date) -> bool:
        """
        Verifies if a specific habit marks validation completion constraints on a given date.

        Args:
            habit_id (int): The unique identifier of the tracked target habit.
            target_date (date): The specific calendar date entity to validate against.

        Returns:
            bool: True if the habit record exists and is validated as completed, False otherwise.
        """
        date_str: str = target_date.strftime(self.DATE_FORMAT)

        row: Optional[Dict[str, Any]] = self.execution_repo.get_by_habit_and_date(habit_id, date_str)
        
        if row:
            return bool(row["executed"])
        return False

    def complete_habit_on_date(self, habit_id: int, target_date: date) -> None:
        """
        Logs a successful validation mark execution event checkpoint for a specific habit.

        Args:
            habit_id (int): The unique identifier of the target habit.
            target_date (date): The calendar date when the habit validation occurred.
        """
        date_str: str = target_date.strftime(self.DATE_FORMAT)

        if self.is_habit_completed(habit_id, target_date):
            logger.debug(f"Habit with ID {habit_id} already marked completed on {date_str}. Skipping insert.")
            return
            
        self.execution_repo.insert((habit_id, date_str, 1))
        logger.info(f"Successfully recorded execution for habit ID {habit_id} on {date_str}.")

    def get_habits_completed_on_date(self, target_date: date) -> Set[int]:
            """
            Compiles a high-performance hash set containing unique IDs of habits completed on a target date.

            Args:
                target_date (date): The reference day parameters to scan history against.

            Returns:
                Set[int]: A unique set collection matching verified completed habit IDs.
            """
            date_str: str = target_date.strftime(self.DATE_FORMAT)
            rows = self.execution_repo.get_all_by_date(date_str)
            

            return {
                row["habit_id"]
                for row in rows
                if bool(row["executed"])
            }