"""Module responsible for database persistence operations regarding habit configurations."""

import sqlite3
from typing import Any, Final, List, Tuple

from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


BASE_SELECT_FIELDS: Final[str] = (
    "id, habit_id, execution_days, is_active, valid_from, valid_until"
)


class HabitConfigRepository:
    """Repository class handling low-level SQL operations for habit configurations."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        """Initializes the repository with an active SQLite database connection.

        Args:
            connection: An active SQLite database connection object.
        """
        self._conn: sqlite3.Connection = connection

    def get_all_by_habit_id(self, habit_id: int) -> List[Tuple[Any, ...]]:
        """Retrieves all configuration history records for a given habit ID.

        Args:
            habit_id: The primary identifier of the parent habit.

        Returns:
            A list of tuples representing raw habit configuration database rows.

        Raises:
            sqlite3.Error: If the database query execution fails.
        """
        query = f"""
            SELECT {BASE_SELECT_FIELDS}
            FROM habit_config
            WHERE habit_id = ?
            ORDER BY valid_from ASC
        """
        try:
            cursor = self._conn.execute(query, (habit_id,))
            return cursor.fetchall()
        except sqlite3.Error as error:
            logger.error(
                f"Failed to fetch configurations for habit ID {habit_id}.",
                exc_info=error,
            )
            raise

    def insert(self, habit_config: Tuple[int, str, str, str, str]) -> None:
        """Inserts a new habit configuration tuple record into the database.

        Args:
            habit_config: A tuple containing (habit_id, execution_days, is_active, valid_from, valid_until).

        Raises:
            sqlite3.Error: If the insertion or commit transaction fails.
        """
        query = """
            INSERT INTO habit_config (habit_id, execution_days, is_active, valid_from, valid_until) 
            VALUES (?, ?, ?, ?, ?)
        """
        try:
            self._conn.execute(query, habit_config)
            self._conn.commit()
            logger.info("Habit config inserted into database.")
        except sqlite3.Error as error:
            self._conn.rollback()
            logger.error("Failed to insert habit configuration.", exc_info=error)
            raise

    def close_config(self, latest_config_id: int, closing_date: str) -> None:
        """Closes an active habit configuration record by updating its valid_until boundary.

        Args:
            latest_config_id: The primary identifier of the active configuration record.
            closing_date: ISO formatted string or date representation for closure.

        Raises:
            sqlite3.Error: If the update operation or transaction commit fails.
        """
        query = """
            UPDATE habit_config
            SET valid_until = ?
            WHERE id = ? 
        """
        try:
            self._conn.execute(query, (closing_date, latest_config_id))
            self._conn.commit()
            logger.info(f"Habit config successfully closed for: {closing_date}")
        except sqlite3.Error as error:
            self._conn.rollback()
            logger.error(
                f"Failed to close habit config ID {latest_config_id}.",
                exc_info=error,
            )
            raise