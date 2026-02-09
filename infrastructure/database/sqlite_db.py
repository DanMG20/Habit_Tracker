## La VAMOS A CAMBBIAR A SQLITE
import json
import os
import random
import shutil
from datetime import date, datetime, timedelta
from utils.paths import resource_path
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
        logger.info("db succesfully connected") 

    
    def initialize(self):
        if not self.conn:
            raise RuntimeError("Database not connected")
        run_migrations(self.conn)

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("DB connection closed")
# ------------------------ DATABASE CLASS ------------------------
class Database:
    def __init__(self):



        # Archivos en APPDATA
        self.habitos_file = resource_path("json/Base_de_datos_habitos.json")
        self.registro_file = resource_path( "json/registro_habitos.json")
        self.quotes_file = resource_path("resources/json/default_quotes.json")
    
        self._copiar_si_no_existe("resources/json/default_quotes.json", self.quotes_file)


        self.habitos = self.cargar_habitos()  # equivalent to connect db DONE

    def get_start_tracking_date(self) -> date | None:
        if not self.habitos:
            return
        return min(
            datetime.strptime(h["Fecha_creacion"], "%Y-%m-%d").date()
            for h in self.habitos
        )

    def get_phrases(self):
        return self.phrases

    # ------------------------ UTIL ----------------------------
    def _copiar_si_no_existe(self, archivo_origen, archivo_destino):
        """
        Copia archivo por defecto a APPDATA solo si no existe.
        """
        if not os.path.exists(archivo_destino):
            origen = resource_path(archivo_origen)
            if os.path.exists(origen):
                shutil.copy(origen, archivo_destino)
                print(f"✅ Copiado {origen} a {archivo_destino}")
            else:
                print(f"⚠️ No se encontró el archivo origen: {origen}")

    # ------------------------ HÁBITOS --------------------------
    def cargar_habitos(self):
        if not os.path.exists(self.habitos_file):
            return []
        with open(self.habitos_file, "r", encoding="utf-8") as archivo:
            try:
                return json.load(archivo)
            except json.JSONDecodeError:
                print("Archivo de hábitos corrupto, retornando lista vacía")
                return []

    def guardar_habitos(self):
        with open(self.habitos_file, "w", encoding="utf-8") as archivo:
            json.dump(self.habitos, archivo, indent=4, ensure_ascii=False)

    def crear_habito(self, nombre_habito_nuevo, dias_ejecucion, color, descripcion):
        fecha_creacion_string = str(datetime.now().date())
        dias_ejecucion_valores = list(dias_ejecucion)

        for habito in self.habitos:
            if nombre_habito_nuevo == habito["nombre_habito"]:
                print("Este hábito ya existe, intenta con otro nombre.")
                return

        habito = {
            "nombre_habito": nombre_habito_nuevo,
            "dias_ejecucion": dias_ejecucion_valores,
            "Fecha_creacion": fecha_creacion_string,
            "color": color,
            "descripcion": descripcion,
        }
        self.habitos.append(habito)
        self.guardar_habitos()
        print(f"El hábito '{nombre_habito_nuevo}' ha sido creado con éxito.")

    # ------------------------ EJECUCIONES -----------------------
    def cargar_ejecuciones(self):
        if not os.path.exists(self.registro_file):
            return []
        with open(self.registro_file, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def guardar_ejecuciones(self, ejecuciones):
        with open(self.registro_file, "w", encoding="utf-8") as f:
            json.dump(ejecuciones, f, indent=4, ensure_ascii=False)

    def registrar_ejecucion_habito(self, nombre_habito):
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        ejecuciones = self.cargar_ejecuciones()

        if any(
            ejec["nombre_habito"] == nombre_habito
            and ejec["fecha_ejecucion"] == fecha_actual
            for ejec in ejecuciones
        ):
            return
            """           CTkMessagebox(master=self.master,
                          font=styles.FUENTE_PEQUEÑA,
                          message=("Información", f"El hábito '{nombre_habito}' ya fue completado hoy."),
                          icon="check", option_1="Aceptar") """

        nuevo_registro = {
            "nombre_habito": nombre_habito,
            "fecha_ejecucion": fecha_actual,
            "completado": True,
        }
        ejecuciones.append(nuevo_registro)
        self.guardar_ejecuciones(ejecuciones)
        """         CTkMessagebox(master=self.master,
                            font=styles.FUENTE_PEQUEÑA,
                            message=("Éxito", f"Se registró como completado el hábito '{nombre_habito}' para hoy."),
                            icon="check", option_1="Aceptar")
        """

    def registrar_ejecucion_habito_ayer(self, nombre_habito):
        fecha_ayer = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        ejecuciones = self.cargar_ejecuciones()

        if any(
            ejec["nombre_habito"] == nombre_habito
            and ejec["fecha_ejecucion"] == fecha_ayer
            for ejec in ejecuciones
        ):
            return
            """             CTkMessagebox(master=self.master,
                          font=styles.FUENTE_PEQUEÑA,
                          message=("Información", f"El hábito '{nombre_habito}' ya fue completado ayer."),
                          icon="check", option_1="Aceptar")
            """

        nuevo_registro = {
            "nombre_habito": nombre_habito,
            "fecha_ejecucion": fecha_ayer,
            "completado": True,
        }
        ejecuciones.append(nuevo_registro)
        self.guardar_ejecuciones(ejecuciones)
        """         CTkMessagebox(master=self.master,
                      font=styles.FUENTE_PEQUEÑA,
                      message=("Éxito", f"Se registró como completado el hábito '{nombre_habito}' para ayer."),
                      icon="check", option_1="Aceptar") """

    # ------------------------ RESET --------------------------------
    def resetear_archivos(self):
        """msg = CTkMessagebox(
            master=self.master,
            title="Confirmación",
            message="¿Estás seguro de que deseas restaurar la aplicación? TODOS los archivos y registros serán borrados. Esta acción no se puede deshacer.",
            font=styles.FUENTE_PEQUEÑA,
            icon="question",
            option_1="No",
            option_2="Sí"
                    if msg.get() != "Sí":
            return
        )"""

        try:
            archivos_a_borrar = [
                self.habitos_file,
                self.registro_file,
                self.quotes_file,
                os.path.join(self.APPDATA_DIR, "configuracion.json"),
                os.path.join(self.APPDATA_DIR, "posicion_ventana.json"),
                os.path.join(self.APPDATA_DIR, "frases.json"),
            ]

            for archivo in archivos_a_borrar:
                if os.path.exists(archivo):
                    os.remove(archivo)

            self._copiar_si_no_existe(
                "C:\\Users\\EDMG0\\Documents\\Proyectos_python\\Habit_Traker_2.0\\resources\\json\\default_quotes.json",
                self.quotes_file,
            )

            """             CTkMessagebox(
                            master=self.master,
                            title="Información",
                            font=styles.FUENTE_PEQUEÑA,
                            message="Los registros han sido eliminados. Se reiniciará la aplicación."
                        )
            """

        except Exception as e:
            print(f"No se pudo reiniciar la app: {e}")
        """             CTkMessagebox(
                        master=self.master,
                        title="Error",
                        font=styles.FUENTE_PEQUEÑA,
                        message=f"No se pudo eliminar los archivos: {e}"
                    )
        """



