import sqlite3
from typing import List, Tuple, Optional 

from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)



class ExecutionsRepository: 

    """
    Repository responsible ONLY for SQL operations on executions table. 
    """
    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection

    def get_all(self) -> List[Tuple[int,int,str,int]]:
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
    
    def insert(self, execution: Tuple[int,str,str]) -> None:
        self._conn.execute(
        """
        INSERT INTO executions (habit_id,execution_date,executed)
        VALUES (?,?,?)
        """,
        execution,
        )
        self._conn.commit()
        logger.info("Execution inserted on db")



