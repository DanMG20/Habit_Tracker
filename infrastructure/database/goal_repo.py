import sqlite3
from typing import List, Tuple, Optional 

from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)


class GoalRepository:
    """
    Repository responsible ONLY for SQL operations on goal table. 
    """
    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection


    def count(self) -> int: 
        cursor = self._conn.execute(
            "SELECT COUNT(*) FROM quarterly_goals"
        )
        return cursor.fetchone()[0]
    

    
    def get_all(self) -> List[Tuple[int, str, str,str, str,str,str,str]]:
        cursor = self._conn.execute(
        """
        SELECT id, 
        goal_name,
        description,
        period_year,
        period_quarter,
        is_completed,
        completed_at,
        created_at

        FROM quarterly_goals 
        ORDER BY id
        """
        )
        return cursor.fetchall()
    
    def insert(
        self,
        name: str,
        description: str,
        year: int,
        quarter: int,
        created_at: str
    ) -> None:

        self._conn.execute(
            """
            INSERT INTO quarterly_goals
            (
                goal_name,
                description,
                period_year,
                period_quarter,
                is_completed,
                completed_at,
                created_at
            )
            VALUES (?,?,?,?,?,?,?)
            """,
            (
                name,
                description,
                year,
                quarter,
                0,          # is_completed default
                None,       # completed_at default
                created_at
            ),
        )

        self._conn.commit()
        logger.info("Goal Inserted")
    
    def complete(self, goal_id, completed_at, is_completed):
        self._conn.execute(
            """
            UPDATE quarterly_goals 
            SET completed_at = ?, 
            is_completed = ?,
            WHERE id = ?

            """, (completed_at,is_completed,goal_id),
        )
        self._conn.commit()
        logger.info("Goal Updated")




    def update(self, goal_id, new_goal_name,new_period_quarter,new_year):
        self._conn.execute(
            """
            UPDATE quarterly_goals 
            SET goal_name = ?, 
            period_year = ?,
            period_quarter = ?
            WHERE id = ?

            """, (new_goal_name,new_year,new_period_quarter,goal_id),
        )
        self._conn.commit()
        logger.info("Goal Updated")


    def delete_by_id(self, goal_id: int) -> None:
        self._conn.execute(
            "DELETE FROM quarterly_goals WHERE id = ?", (goal_id,),
        )
        self._conn.commit()