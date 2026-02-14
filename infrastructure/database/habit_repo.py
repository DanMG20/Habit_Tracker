import sqlite3
from typing import List, Tuple, Optional
from datetime import date 

from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)

class HabitRepository:
    def __init__(self,connection: sqlite3.Connection):
        self._conn = connection


    def count(self) -> int: 
        cursor = self._conn.execute(
            "SELECT COUNT(*) FROM habits"
        )
        return cursor.fetchone()[0]
    
    def get_start_tracking_date(self):
        cursor = self._conn.execute(
            "SELECT MIN(creation_date) FROM habits"
        )
        return cursor.fetchone()[0]
    
    def get_all(self) -> List[Tuple[int, str, str]]:
        cursor = self._conn.execute(
        """
        SELECT id, 
        habit_name,
        execution_days,
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

    def get_by_id(self, habit_id) -> Tuple[int, str, str]:

        cursor = self._conn.execute(
        """
        SELECT id, 
        habit_name,
        execution_days,
        creation_date,
        habit_color,
        category,
        description
        FROM habits 
        WHERE id = ?
        """,(habit_id,)
        )

        return cursor.fetchone()
            




    def insert(self, habit: Tuple[str,str,date,str,str,str]) -> None: 
        self._conn.execute(
        """
        INSERT INTO habits (habit_name, execution_days, creation_date, habit_color, category, description) 
        VALUES (?,?,?,?,?,?)
        """,
        habit,
        ) 
        self._conn.commit()
        logger.info("Habit Inserted into database")

  
    def update(self, modified_habit: Tuple[str,str,date,str,str,str]) -> None: 

        logger.info(modified_habit)
        self._conn.execute(
        """
        UPDATE habits 
        SET habit_name = ?,
        execution_days = ?,
        habit_color = ?, 
        category = ?,
        description = ?
        WHERE id = ? 
        """,modified_habit
        ) 
        self._conn.commit()
        logger.info("Habit updated on database")



    def delete_by_id(self, habit_id: int) -> None: 
        self._conn.execute(
            "DELETE FROM habits WHERE id = ?", (habit_id,),
        )
        self._conn.commit()
        logger.info("Habit Deleted from database")





