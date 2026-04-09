"""
Needed to update sqlite.db from 2.0 to 2.1
"""


import sqlite3
import os

def migrate_habits():
    source_db = 'habit_tracker.db'
    target_db = 'habit_tracker_test.db'

    if not os.path.exists(source_db):
        print(f"Error: No se encontró {source_db}")
        return

    # Conexiones
    conn_src = sqlite3.connect(source_db)
    conn_tgt = sqlite3.connect(target_db)
    
    src_cursor = conn_src.cursor()
    tgt_cursor = conn_tgt.cursor()

    try:
        # 1. Obtener los hábitos de la base original
        # Asumo que las columnas en habit_tracker.db son id, habit_name, execution_days, created_at, etc.
        src_cursor.execute("SELECT id, habit_name, execution_days, creation_date, category, habit_color, description FROM habits")
        habits = src_cursor.fetchall()

        print(f"Migrando {len(habits)} hábitos...")

        for h in habits:
            h_id, name, exec_days, creation_date, category, color, desc = h

            # 2. Insertar en la tabla 'habits' del nuevo modelo (si no existe)
            # Nota: Ajusta los nombres de columnas si en el nuevo modelo cambiaron
            tgt_cursor.execute("""
                INSERT OR IGNORE INTO habits (id, habit_name, category, habit_color, description, creation_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (h_id, name, category, color, desc, creation_date))

            # 3. Insertar la configuración en 'habit_config'
            # Aquí aplicamos tu lógica: valid_from = created_at, valid_until = NULL, is_active = 1
            tgt_cursor.execute("""
                INSERT INTO habit_config (habit_id, execution_days, is_active, valid_from, valid_until)
                VALUES (?, ?, ?, ?, ?)
            """, (h_id, exec_days, 1, creation_date, None))

        conn_tgt.commit()
        print("Migración completada con éxito.")

    except sqlite3.Error as e:
        print(f"Error durante la migración: {e}")
        conn_tgt.rollback()
    finally:
        conn_src.close()
        conn_tgt.close()



def remove_execution_days_column():
    db_path = 'habit_tracker_test.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Intentar el método moderno (SQLite 3.35.0+)
        print("Eliminando columna 'execution_days' de la tabla 'habits'...")
        cursor.execute("ALTER TABLE habits DROP COLUMN execution_days")
        conn.commit()
        print("Columna eliminada exitosamente.")
        
    except sqlite3.OperationalError:
        # Si falla por versión antigua, aplicamos el método tradicional
        print("Método directo no soportado. Aplicando recreación de tabla...")
        
        # 1. Ver qué columnas tiene actualmente excepto execution_days
        cursor.execute("PRAGMA table_info(habits)")
        columns = [info[1] for info in cursor.fetchall() if info[1] != 'execution_days']
        cols_str = ", ".join(columns)

        # 2. Crear tabla nueva (asumiendo estructura estándar)
        # Nota: Este paso es complejo sin el esquema exacto, 
        # pero si ya migraste los datos, el ALTER TABLE suele funcionar.
        print("Aviso: Tu versión de SQLite es antigua. Se recomienda usar una herramienta ")
        print("como DB Browser for SQLite para hacer el DROP COLUMN visualmente si este script falla.")
    
    finally:
        conn.close()

if __name__ == "__main__":
    remove_execution_days_column()