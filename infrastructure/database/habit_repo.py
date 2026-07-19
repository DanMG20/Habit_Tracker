"""Module responsible for database persistence operations regarding habits."""

import sqlite3
from datetime import date
from typing import Any, List, Optional, Tuple

from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class HabitRepository:
    """Repository class handling low-level SQL operations for habits."""

    def __init__(self, connection: sqlite3.Connection) -> None:
        """Initializes the repository with a pre-configured SQLite connection.

        Args:
            connection: An active, pre-configured SQLite database connection.
        """
        self._conn = connection

    def count(self) -> int:
        """Counts the total number of habits stored in the database.

        Returns:
            The total count of habit records.
        """
        cursor = self._conn.execute("SELECT COUNT(*) FROM habits")
        return cursor.fetchone()[0]

    def get_start_tracking_date(self) -> Optional[Any]:
        """Retrieves the earliest habit creation date from the database.

        Returns:
            The earliest creation date string/record or None if table is empty.
        """
        cursor = self._conn.execute("SELECT MIN(creation_date) FROM habits")
        return cursor.fetchone()[0]

    def get_all(self) -> List[Tuple[int, str, str, str, str, str]]:
        """Retrieves all habits ordered by their primary identifier.

        Returns:
            A list of tuples containing all habit row fields.
        """
        cursor = self._conn.execute(
            """
            SELECT id, 
            habit_name,
            creation_date,
            habit_color,
            category,
            description
            FROM habits 
            ORDER BY id
            """
        )
        return cursor.fetchall()

    def get_categories(self) -> List[str]:
        """Retrieves all distinct habit categories in alphabetical order.

        Returns:
            A list of unique category strings.
        """
        cursor = self._conn.execute(
            """
            SELECT
            DISTINCT(category)
            FROM habits 
            ORDER BY category
            """
        )
        rows = cursor.fetchall()
        return [row["category"] for row in rows]

    def get_by_id(self, habit_id: int) -> Tuple[int, str, str, str, str, str]:
        """Retrieves a single habit record by its primary identifier.

        Args:
            habit_id: The primary identifier of the habit.

        Returns:
            A tuple containing the matching habit fields.
        """
        cursor = self._conn.execute(
            """
            SELECT id, 
            habit_name,
            creation_date,
            habit_color,
            category,
            description
            FROM habits 
            WHERE id = ?
            """,
            (habit_id,),
        )
        return cursor.fetchone()

    def insert(self, habit: Tuple[str, str, date, str, str]) -> Optional[int]:
        """Inserts a new habit tuple record into the database.

        Args:
            habit: A tuple containing habit attributes for insertion.

        Returns:
            The primary key ID generated for the inserted row.
        """
        cursor = self._conn.execute(
            """
            INSERT INTO habits (habit_name, creation_date, habit_color, category, description) 
            VALUES (?,?,?,?,?)
            """,
            habit,
        )
        self._conn.commit()
        logger.info("Habit Inserted into database")
        return cursor.lastrowid

    def update(self, modified_habit: Tuple[str, str, str, str, int]) -> None:
        """Updates an existing habit record in the database.

        Args:
            modified_habit: A tuple containing modified habit values and target ID.
        """
        self._conn.execute(
            """
            UPDATE habits 
            SET habit_name = ?,
            habit_color = ?, 
            category = ?,
            description = ?
            WHERE id = ? 
            """,
            modified_habit,
        )
        self._conn.commit()
        logger.info("Habit updated on database")

    def delete_by_id(self, habit_id: int) -> None:
        """Deletes a habit record from the database by its primary identifier.

        Args:
            habit_id: The primary identifier of the habit to delete.
        """
        self._conn.execute(
            "DELETE FROM habits WHERE id = ?",
            (habit_id,),
        )
        self._conn.commit()
        logger.info("Habit Deleted from database")