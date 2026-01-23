## La VAMOS A CAMBBIAR A SQLITE
import json
import os
import random
import shutil
import sys
from datetime import date, datetime, timedelta

from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class SQLiteDB:
    def __init__(self, path):
        # self.conn = sqlite3.connect(path)
        pass


# ------------------------ RESOURCE PATH ------------------------
def resource_path(relative_path):
    """
    Devuelve la ruta absoluta al recurso.
    Funciona con PyInstaller (.exe) y con .py
    """
    try:
        # PyInstaller crea una carpeta temporal _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        # Durante desarrollo
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


# ------------------------ DATABASE CLASS ------------------------
class Database:
    def __init__(self):

        # Carpeta APPDATA
        self.APPDATA_DIR = os.path.join(os.environ["APPDATA"], "Habit Tracker")
        os.makedirs(self.APPDATA_DIR, exist_ok=True)

        # Archivos en APPDATA
        self.habitos_file = os.path.join(self.APPDATA_DIR, "Base_de_datos_habitos.json")
        self.registro_file = os.path.join(self.APPDATA_DIR, "registro_habitos.json")
        self.frases_file = os.path.join(self.APPDATA_DIR, "frases.json")
        # Copiar archivos por defecto si no existen
        self._copiar_si_no_existe("json/Base_de_datos_habitos.json", self.habitos_file)
        self._copiar_si_no_existe("json/frases.json", self.frases_file)

        # Cargar datos
        self.load_random_phrase()
        self.habitos = self.cargar_habitos()

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
                self.frases_file,
                os.path.join(self.APPDATA_DIR, "configuracion.json"),
                os.path.join(self.APPDATA_DIR, "posicion_ventana.json"),
                os.path.join(self.APPDATA_DIR, "frases.json"),
            ]

            for archivo in archivos_a_borrar:
                if os.path.exists(archivo):
                    os.remove(archivo)

            # Copiar archivos por defecto
            self._copiar_si_no_existe(
                "C:\\Users\\EDMG0\\Documents\\Proyectos_python\\Habit_Traker_2.0\\json\\Base_de_datos_habitos.json",
                self.habitos_file,
            )
            self._copiar_si_no_existe(
                "C:\\Users\\EDMG0\\Documents\\Proyectos_python\\Habit_Traker_2.0\\json\\frases.json",
                self.frases_file,
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

    # ------------------------ FRASES --------------------------------
    def load_random_phrase(self):
        # Si no existe el archivo de frases, lo creamos con las frases por defecto
        if not os.path.exists(self.frases_file):
            frases_por_defecto = [
                {
                    "frase": "Somos lo que hacemos repetidamente. La excelencia, entonces, no es un acto, sino un hábito.",
                    "autor": "Aristóteles",
                },
                {
                    "frase": "Lo que no se define, no se puede medir. Lo que no se mide, no se puede mejorar. Lo que no se mejora, se degrada siempre",
                    "autor": "Lord Kelvin",
                },
            ]
            with open(self.frases_file, "w", encoding="utf-8") as f:
                json.dump(frases_por_defecto, f, indent=4, ensure_ascii=False)

        # Cargar frases desde el archivo
        try:
            with open(self.frases_file, "r", encoding="utf-8") as f:
                frases = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error al leer el archivo de frases: {e}")
            frases = []

        # Guardar frases en memoria
        self.phrases = [f"{frase['frase']} - {frase['autor']}" for frase in frases]

        if frases:
            frase_random = random.choice(frases)
            self.phrase = frase_random.get("frase", "")
            self.author = frase_random.get("autor", "")
        else:
            self.phrase = "No hay frases registradas."
            self.author = ""

        logger.info("Phrase succesfully Loaded")

    def get_phrase(self):
        return {"phrase": self.phrase, "author": self.author}

    def evento_eliminar_frase_selec(self, frase_seleccionada):
        """msg = CTkMessagebox(
            master=self.master,
            title="Confirmación",
            message=f"¿Estás seguro de que deseas eliminar la frase '{frase_seleccionada}'?",
            font=styles.FUENTE_PEQUEÑA,
            icon="question", option_1="No", option_2="Sí"
        )
        if msg.get() != "Sí":
            return
        """
        if os.path.exists(self.frases_file):
            with open(self.frases_file, "r", encoding="utf-8") as f:
                frases = json.load(f)
        else:
            frases = []

        if " - " in frase_seleccionada:
            texto_frase, autor = frase_seleccionada.split(" - ", 1)
            frases = [
                f for f in frases if f["frase"] != texto_frase or f["autor"] != autor
            ]
        else:
            frases = [f for f in frases if f["frase"] != frase_seleccionada]

        with open(self.frases_file, "w", encoding="utf-8") as f:
            json.dump(frases, f, indent=4, ensure_ascii=False)

        """         CTkMessagebox(
            master=self.master,
            title="Info",
            font=styles.FUENTE_PEQUEÑA,
            message=f"La frase '{frase_seleccionada}' ha sido eliminada."
        ) """

        """       # Recargar frases y actualizar UI
        self.cargar_frases_random()
        if hasattr(self.master, "mostrar_frase"):
            self.master.mostrar_frase()
        if hasattr(self.master, "generar_menu_frases"):
            self.master.generar_menu_frases() """
