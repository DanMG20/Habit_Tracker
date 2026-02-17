import sqlite3
from typing import List, Tuple, Optional 

from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)


class QuoteRepository:
    """
    Repository responsible ONLY for SQL operations on quotes table. 
    """
    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection


    def count(self) -> int: 
        cursor = self._conn.execute(
            "SELECT COUNT(*) FROM quotes"
        )
        return cursor.fetchone()[0]
    
    def get_random(self) -> dict[str,str]:
        cursor = self._conn.execute(
        """
        SELECT quote,
        author 
        FROM quotes
        ORDER BY RANDOM()
        LIMIT 1 
        """
        )

    
        return cursor.fetchone()
    
    def get_all(self) -> List[dict[int, str, str]]:
        cursor = self._conn.execute(
        """
        SELECT id, quote, author 
        FROM quotes 
        ORDER BY id
        """
        )
        return [(row["id"], 
                 row["quote"], 
                 row["author"]) 
                 for row in cursor.fetchall()]
    
    def insert_many(self, quotes: List[Tuple[str,str]]) -> None: 
        self._conn.executemany(
        """
        INSERT INTO quotes (quote, author) 
        VALUES (?,?)
        """,
        quotes,
        ) 
        self._conn.commit()
        logger.info("Quote Inserted into database")

    
    def update(self, quote_id, new_quote, new_author):
        self._conn.execute(
            """
            UPDATE quotes 
            SET quote = ?, 
            author = ?
            WHERE id = ?

            """, (new_quote,new_author,quote_id),
        )
        self._conn.commit()
        logger.info("Quote Updated")


    def delete_by_id(self, quote_id: int) -> None:
        self._conn.execute(
            "DELETE FROM quotes WHERE id = ?", (quote_id,),
        )
        self._conn.commit()