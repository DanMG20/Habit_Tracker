"""Module responsible for database persistence operations regarding quarterly goals."""

import sqlite3
from typing import Any, Dict, Final, List, Optional

from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

# Constants for default values and query structures
DEFAULT_IS_COMPLETED: Final[int] = 0
BASE_SELECT_FIELDS: Final[str] = """
    id, 
    goal_name,
    description,
    period_year,
    period_quarter,
    is_completed,
    completed_at,
    created_at
"""


class GoalRepository:
    """Repository class handling low-level SQL operations for quarterly goals."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        """Initializes the repository with an active SQLite database connection.

        Args:
            connection: An active SQLite connection object.
        """
        self._conn: sqlite3.Connection = connection
        # Ensure row factory returns dictionary-like access for type safety
        self._conn.row_factory = sqlite3.Row

    def count(self) -> int:
        """Counts the total number of quarterly goals stored in the database.

        Returns:
            The total count of goal records.

        Raises:
            sqlite3.Error: If the database query execution fails.
        """
        try:
            cursor = self._conn.execute("SELECT COUNT(*) FROM quarterly_goals")
            result = cursor.fetchone()
            return result[0] if result else 0
        except sqlite3.Error as error:
            logger.error("Failed to count quarterly goals.", exc_info=error)
            raise

    def get_all(self) -> List[Dict[str, Any]]:
        """Retrieves all quarterly goals ordered by their primary identifier.

        Returns:
            A list of dictionaries representing the quarterly goal records.
        """
        query = f"""
            SELECT {BASE_SELECT_FIELDS}
            FROM quarterly_goals 
            ORDER BY id ASC
        """
        try:
            cursor = self._conn.execute(query)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as error:
            logger.error("Failed to fetch all quarterly goals.", exc_info=error)
            raise

    def get_from_quarter(self, quarter: int, year: int) -> List[Dict[str, Any]]:
        """Retrieves quarterly goals matching a specific quarter and year.

        Args:
            quarter: The target quarter integer (e.g., 1, 2, 3, 4).
            year: The target year integer.

        Returns:
            A list of matching goal record dictionaries.
        """
        query = f"""
            SELECT {BASE_SELECT_FIELDS}
            FROM quarterly_goals 
            WHERE period_quarter = ? AND period_year = ?
            ORDER BY completed_at ASC
        """
        try:
            cursor = self._conn.execute(query, (quarter, year))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as error:
            logger.error(
                f"Failed to fetch goals for Q{quarter} {year}.", exc_info=error
            )
            raise

    def get_completed_on_year(self, year: int) -> List[Dict[str, Any]]:
        """Retrieves all completed quarterly goals for a given year.

        Args:
            year: The target year integer.

        Returns:
            A list of completed goal record dictionaries.
        """
        query = f"""
            SELECT {BASE_SELECT_FIELDS}
            FROM quarterly_goals 
            WHERE period_year = ? AND is_completed = 1
            ORDER BY completed_at ASC
        """
        try:
            cursor = self._conn.execute(query, (year,))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as error:
            logger.error(
                f"Failed to fetch completed goals for year {year}.", exc_info=error
            )
            raise

    def get_all_per_year(self, year: int) -> List[Dict[str, Any]]:
        """Retrieves all quarterly goals associated with a specific year.

        Args:
            year: The target year integer.

        Returns:
            A list of goal record dictionaries for the target year.
        """
        query = f"""
            SELECT {BASE_SELECT_FIELDS}
            FROM quarterly_goals 
            WHERE period_year = ?
            ORDER BY id ASC
        """
        try:
            cursor = self._conn.execute(query, (year,))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as error:
            logger.error(
                f"Failed to fetch goals for year {year}.", exc_info=error
            )
            raise

    def insert(
        self,
        name: str,
        description: str,
        year: int,
        quarter: int,
        created_at: str,
    ) -> None:
        """Inserts a new quarterly goal into the database.

        Args:
            name: The title/name of the goal.
            description: Detailed description of the goal.
            year: The target period year.
            quarter: The target period quarter.
            created_at: ISO formatted creation timestamp string.
        """
        query = """
            INSERT INTO quarterly_goals (
                goal_name,
                description,
                period_year,
                period_quarter,
                is_completed,
                completed_at,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            name,
            description,
            year,
            quarter,
            DEFAULT_IS_COMPLETED,
            None,
            created_at,
        )
        try:
            self._conn.execute(query, params)
            self._conn.commit()
            logger.info(f"Goal successfully inserted: '{name}'")
        except sqlite3.Error as error:
            self._conn.rollback()
            logger.error(f"Failed to insert goal: '{name}'", exc_info=error)
            raise

    def complete(
        self,
        goal_id: int,
        completed_at: str,
        is_completed: int = 1,
    ) -> None:
        """Updates the completion status and timestamp for a specific goal.

        Args:
            goal_id: The primary identifier of the goal.
            completed_at: ISO formatted completion timestamp string.
            is_completed: Flag indicating completion status (1 for true, 0 for false).
        """
        query = """
            UPDATE quarterly_goals 
            SET completed_at = ?, is_completed = ?
            WHERE id = ?
        """
        try:
            self._conn.execute(query, (completed_at, is_completed, goal_id))
            self._conn.commit()
            logger.info(f"Goal ID {goal_id} completion state updated.")
        except sqlite3.Error as error:
            self._conn.rollback()
            logger.error(
                f"Failed to update completion state for goal ID {goal_id}.",
                exc_info=error,
            )
            raise

    def update(
        self,
        goal_id: int,
        new_goal_name: str,
        new_period_quarter: int,
        new_year: int,
    ) -> None:
        """Updates the structural details of an existing goal.

        Args:
            goal_id: The primary identifier of the goal to update.
            new_goal_name: Updated title string for the goal.
            new_period_quarter: Updated quarter integer.
            new_year: Updated year integer.
        """
        query = """
            UPDATE quarterly_goals 
            SET goal_name = ?, period_year = ?, period_quarter = ?
            WHERE id = ?
        """
        try:
            self._conn.execute(
                query, (new_goal_name, new_year, new_period_quarter, goal_id)
            )
            self._conn.commit()
            logger.info(f"Goal ID {goal_id} successfully updated.")
        except sqlite3.Error as error:
            self._conn.rollback()
            logger.error(
                f"Failed to update goal ID {goal_id}.", exc_info=error
            )
            raise

    def delete_by_id(self, goal_id: int) -> None:
        """Deletes a goal record from the database by its primary identifier.

        Args:
            goal_id: The primary identifier of the goal to delete.
        """
        query = "DELETE FROM quarterly_goals WHERE id = ?"
        try:
            self._conn.execute(query, (goal_id,))
            self._conn.commit()
            logger.info(f"Goal ID {goal_id} successfully deleted.")
        except sqlite3.Error as error:
            self._conn.rollback()
            logger.error(
                f"Failed to delete goal ID {goal_id}.", exc_info=error
            )
            raise