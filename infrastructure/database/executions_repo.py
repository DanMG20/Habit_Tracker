"""
Module managing direct persistence access and operations for habit execution records in SQLite.
"""

import sqlite3
from typing import List, Optional

from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class ExecutionsRepository:
    """
    Repository responsible ONLY for SQL operations on executions table.
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        """
        Initializes the repository injecting the concrete SQLite connection handler.

        Args:
            connection (sqlite3.Connection): Active database connection with row_factory configured.
        """
        self._conn: sqlite3.Connection = connection

    def get_all(self) -> List[sqlite3.Row]:
        cursor = self._conn.execute(
            """
            SELECT id, 
                   habit_id,
                   execution_date, 
                   executed
            FROM executions
            ORDER BY id
            """
        )
        return cursor.fetchall()

    def get_by_habit_and_date(self, habit_id: int, date_str: str) -> Optional[sqlite3.Row]:
        """
        Retrieves a single execution log filtered by a specific habit identifier and date string.

        Args:
            habit_id (int): The unique identifier of the target habit.
            date_str (str): The formatted text representation of the target date ('YYYY-MM-DD').

        Returns:
            Optional[sqlite3.Row]: The matching execution row data, or None if no log exists.
        """
        cursor = self._conn.execute(
            """
            SELECT id, 
                   habit_id,
                   execution_date, 
                   executed
            FROM executions
            WHERE habit_id = ? AND execution_date = ?
            """,
            (habit_id, date_str)
        )
        return cursor.fetchone()

    def get_all_by_date(self, date_str: str) -> List[sqlite3.Row]:
        """
        Retrieves all registered habit execution rows matching a specific calendar date threshold.

        Args:
            date_str (str): The formatted text representation of the target date ('YYYY-MM-DD').

        Returns:
            List[sqlite3.Row]: A collection containing execution rows matching the targeted date parameters.
        """
        cursor = self._conn.execute(
            """
            SELECT id, 
                   habit_id,
                   execution_date, 
                   executed
            FROM executions
            WHERE execution_date = ?
            """,
            (date_str,)
        )
        return cursor.fetchall()
    
    def insert(self, execution: tuple) -> None:
        self._conn.execute(
            """
            INSERT INTO executions (habit_id, execution_date, executed)
            VALUES (?, ?, ?)
            """,
            execution,
        )
        self._conn.commit()
        logger.info(f"Successfully logged execution state in database for habit ID {execution[0]}.")