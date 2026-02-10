import os
from utils.paths import resource_path
class ResetService: 
    def __init__(self):
        pass

    # ------------------------ RESET -------------------------------- pasara controller
    def reset_files(self):
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

            db_path =resource_path('habit_tracker.db')
            window_pos_path = resource_path('window_position.json')
            to_delete_files = [
                db_path,
                window_pos_path
            ]

            for file in to_delete_files:
                if os.path.exists(file):
                    os.remove(file)
        except Exception as e:
            print(f"No se pudo reiniciar la app: {e}")
            
        """             CTkMessagebox(
                        master=self.master,
                        title="Error",
                        font=styles.FUENTE_PEQUEÑA,
                        message=f"No se pudo eliminar los archivos: {e}"
                    )
        """
