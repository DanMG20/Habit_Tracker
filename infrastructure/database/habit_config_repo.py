import sqlite3
from typing import List, Tuple, Optional
from datetime import date 

from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)

class HabitConfigRepository:
    def __init__(self,connection: sqlite3.Connection):
        self._conn = connection

    def get_all_by_habit_id(self, habit_id: int):
        cursor = self._conn.execute(
            """
            SELECT id, habit_id, execution_days, is_active, valid_from, valid_until
            FROM habit_config
            WHERE habit_id = ?
            ORDER BY valid_from ASC
            """,
            (habit_id,)
        )

        return cursor.fetchall()
            
    def insert(self, habit_config: Tuple[int,str,str,str,str]) -> None: 
        self._conn.execute(
        """
        INSERT INTO habit_config (habit_id, execution_days, is_active, valid_from, valid_until) 
        VALUES (?,?,?,?,?)
        """,
        habit_config,
        ) 
        self._conn.commit()
        logger.info("Habit config Inserted into database")



    def close_config(self,latest_config_id, closing_date):
        self._conn.execute(
        """
        UPDATE habit_config
        SET valid_until = ?
        WHERE id = ? 
        """,(closing_date,latest_config_id)
        ) 
        self._conn.commit()
        logger.info(f"Habit  config succesfully closed for : {closing_date}")




