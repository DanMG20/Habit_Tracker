from datetime import datetime
from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)
class AppController: 
    def __init__(self, habit_service , db, calendar, metrics_service): 
        self.db = db # TEMPORAL OJOOOO
        self.calendar = calendar # TEMPORAAAAL 
        self.metrics_service =metrics_service
        logger.warning("Using temporary DB bridge")
        logger.warning("Using temporary calendar bridge")
        self.habit_service = habit_service
        self.fecha_guardada = datetime.now().date()

    def update_app_state(self):
        #actualiza todo el sector derecho de la pantalla asi como las fechas
        self.calendar.refrescar_variables()
        self.refrescar_tabla_y_fechas(None)
        #actualiza el contenido de la fecha que indica el dia de hoy
        self.fecha_hoy_label.configure(text = self.encabezados[0])
        self.listar_habitos()
        #Selecciona una nueva frase de la base de datos de frases 
        self.db_objeto.cargar_frases_random()
        # Actualiza el frame que contiene las frases
        for widget in self.frame_frase_0_1.winfo_children():
            widget.destroy()
        self.mostrar_frase()
        # Reprogramar la ejecución después de 900,000 ms (15 min)
        logger.info("App state updated")

    def go_previus_week(self):
        self.calendar.go_to_previous_week()
        logger.info("Week changed to previous")

    def go_next_week(self):
        self.calendar.go_to_next_week()
        logger.info("Week changed to next")

    def verify_date(self):
        hoy = datetime.now().date()
        if hoy != self.fecha_guardada:
            self.fecha_guardada = hoy 
            self.update_app_state()
        return self.fecha_guardada
    
    def get_week_state(self):
        return {
            "headers" : self.calendar.get_date_strings(),
        "week_start" : self.calendar.calculate_week_start(),
        "current_days" : self.calendar.current_week_days(),
        "weekly_performance" : self.metrics_service.calc_weekly_performance(),
        }

    def check_habit_today(self,habit_name):
        self.habit_service.complete_today(habit_name)
        self.rendimiento_semanal = self.metrics_service.calc_weekly_performance()
        logger.info(f"Habit completed today : {habit_name}")

    def get_month_state(self):
        return {
            "monthly_performance_avg": self.metrics_service.calc_monthly_performance(),
         }
        
        