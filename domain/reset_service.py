import os
from utils.paths import resource_path
class ResetService: 
    def __init__(self):
        pass

    # ------------------------ RESET -------------------------------- pasara controller
    def reset_files(self):


        db_path =resource_path('habit_tracker.db')
        window_pos_path = resource_path('window_position.json')

        try:    

            to_delete_files = [
                db_path,
                window_pos_path
            ]
            print(to_delete_files)
            for file in to_delete_files:
                if os.path.exists(file):
                    os.remove(file)
                else: 
                    print("NOSE QUE PASA"*10)
        except Exception as e:
            print(f"No se pudo reiniciar la app: {e}")
            
        """             CTkMessagebox(
                        master=self.master,
                        title="Error",
                        font=styles.FUENTE_PEQUEÑA,
                        message=f"No se pudo eliminar los archivos: {e}"
                    )
        """
