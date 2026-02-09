def run_migrations(conn):
    """
    Crea el schema inicial de la base de datos.
    Esta función es idempotente: puede ejecutarse múltiples veces sin romper nada.
    """

    # ========================
    # Tabla: habits
    # ========================
    conn.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_name TEXT NOT NULL UNIQUE,
            execution_days TEXT NOT NULL,
            creation_date DATE NOT NULL,
            habit_color TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT
        );
    """)

    # ========================
    # Tabla: executions
    # ========================
    conn.execute("""
        CREATE TABLE IF NOT EXISTS executions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER NOT NULL,
            execution_date DATE NOT NULL,
            executed INTEGER NOT NULL CHECK (executed IN (0, 1)),
            FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
        );
    """)

    # ========================
    # Tabla: quotes
    # ========================
    conn.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT NOT NULL,
            author TEXT
        );
    """)

    # ========================
    # Tabla: Goals
    # ========================
    conn. execute("""
        CREATE TABLE IF NOT EXISTS quarterly_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_name TEXT NOT NULL,
            description TEXT,
            period_year INTEGER NOT NULL,
            period_quarter INTEGER NOT NULL CHECK (period_quarter IN (1,2,3,4)),
            is_completed INTEGER NOT NULL CHECK (is_completed IN (0,1)),
            completed_at DATE,
            created_at DATE NOT NULL
        );
    """)

    conn.commit()
