from infrastructure.logging.logger import get_logger
from infrastructure.database.migrations import run_migrations
import sqlite3
logger = get_logger(__name__)


class SQLiteDB:
    def __init__(self, path):
        self.path = path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON;")

    
    def initialize(self):
        if not self.conn:
            raise RuntimeError("Database not connected")
        run_migrations(self.conn)

    def close(self):
        if self.conn:
            self.conn.close()
 




