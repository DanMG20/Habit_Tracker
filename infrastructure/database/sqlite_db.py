"""Module responsible for managing SQLite database connection lifecycles and migrations."""

import sqlite3
from pathlib import Path
from typing import Optional, Union

from infrastructure.database.migrations import run_migrations
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class SQLiteDB:
    """Manages SQLite database connection lifecycles, configuration pragmas, and migrations."""

    def __init__(self, path: Union[str, Path]) -> None:
        """Initializes the database manager with a target file path.

        Args:
            path: The file system path to the SQLite database file.
        """
        self._path: Path = Path(path)
        self.conn: Optional[sqlite3.Connection] = None

    @property
    def connection(self) -> sqlite3.Connection:
        """Provides access to the active database connection.

        Returns:
            The active sqlite3.Connection object.

        Raises:
            RuntimeError: If the database is not currently connected.
        """
        if self.conn is None:
            raise RuntimeError("Database connection is not active. Call connect() first.")
        return self.conn

    def connect(self) -> None:
        """Establishes a connection to the SQLite database and configures runtime pragmas.

        Raises:
            sqlite3.Error: If the connection attempt or pragma execution fails.
        """
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self.conn = sqlite3.connect(str(self._path))
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON;")
            logger.info(f"Database connection successfully established: {self._path}")
        except sqlite3.Error as error:
            logger.error(f"Failed to connect to SQLite database at {self._path}", exc_info=error)
            raise

    def initialize(self) -> None:
        """Executes database schema migrations on the active connection.

        Raises:
            RuntimeError: If called before establishing a database connection.
            sqlite3.Error: If migration execution encounters a database fault.
        """
        if self.conn is None:
            logger.error("Attempted to initialize migrations without an active connection.")
            raise RuntimeError("Database not connected. Cannot run migrations.")

        try:
            run_migrations(self.conn)
            logger.info("Database migrations successfully executed.")
        except sqlite3.Error as error:
            logger.error("Failed during database migration execution.", exc_info=error)
            raise

    def close(self) -> None:
        """Safely closes the active database connection if open."""
        if self.conn is not None:
            try:
                self.conn.close()
                logger.info(f"Database connection closed for: {self._path}")
            except sqlite3.Error as error:
                logger.error("Error occurred while closing the database connection.", exc_info=error)
            finally:
                self.conn = None

    def __enter__(self)-> "SQLiteDB":
        """Context manager entry point establishing automatic connection.

        Returns:
            The connected instance of SQLiteDB.
        """
        self.connect()
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[object]) -> None:
        """Context manager exit point ensuring safe connection cleanup."""
        self.close()