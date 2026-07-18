"""
Migration utility script to evolve the SQLite database schema.
Removes the redundant 'execution_days' column from the 'habits' table.
"""

import sqlite3
from paths import data_path  # Update this import path based on your real path manager


def migrate_habits_table() -> None:
    """
    Alters the habits table structure to drop the obsolete execution_days column.
    
    Uses a safe transaction block to protect historical user entries.
    """
    # Establish connection directly to the persistent binary file
    connection = sqlite3.connect(data_path('habit_tracker.db'))
    cursor = connection.cursor()

    try:
        print("Starting database schema migration...")
        
        # 1. Execute the alter table statement using standard SQLite commands
        cursor.execute("ALTER TABLE habits DROP COLUMN execution_days;")
        
        # 2. Commit the changes permanently to the disk if successful
        connection.commit()
        print("Migration successful! Column 'execution_days' successfully dropped from 'habits' table.")
        
    except sqlite3.OperationalError as error:
        # Prevent failure if the migration was already applied previously
        connection.rollback()
        print(f"Migration aborted. Database operational error encountered: {error}")
        
    except Exception as general_error:
        connection.rollback()
        print(f"Critical failure during migration execution. Rollback triggered: {general_error}")
        
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    migrate_habits_table()