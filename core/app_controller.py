from datetime import datetime
from infrastructure.config import config_manager
from infrastructure.logging.logger import get_logger
logger = get_logger(__name__)
class AppController: 
    def __init__(self, habit_service , db, calendar, metrics_service, phrase_service): 
        self.db = db # TEMPORAL OJOOOO
        self.calendar_service = calendar
        self.metrics_service = metrics_service
        self.phrase_service = phrase_service
        logger.warning("Using temporary DB bridge")
        self.habit_service = habit_service
        self.fecha_guardada = datetime.now().date()
        self.load_config()
        self.load_phrase()


    def update_app_state(self):
        #actualiza todo el sector derecho de la pantalla asi como las fechas
        self.calendar_service.refrescar_variables()
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

    def go_previous_week(self):
        self.calendar_service.go_to_previous_week()
        logger.info("Week changed to previous")

    def go_next_week(self):
        self.calendar_service.go_to_next_week()
        logger.info("Week changed to next")

    def go_previous_month(self):
        self.calendar_service.go_to_previous_month()
        logger.info("Month changed to previous")

    def go_next_month(self):
        self.calendar_service.go_to_next_month()
        logger.info("Month changed to next")

    def go_previous_year(self):
        self.calendar_service.go_to_previous_year()
        logger.info("year changed to previous")

    def go_next_year(self):
        self.calendar_service.go_to_next_year()
        logger.info("year changed to next")
    
    def get_phrases(self):
        return self.phrase_service.get_phrases()
    

    def delete_selected_phrase(self,selected_phrase):
        self.db.evento_eliminar_frase_selec(selected_phrase)
    
    def habit_file_exists(self):
        return self.habit_service.habit_file_exists()

    def update_habits(self):
        self.habit_service.load_habits()
    def load_habit_register_executions(self):
        return self.habit_service.load_executions()
    def verify_date(self):
        hoy = datetime.now().date()
        if hoy != self.fecha_guardada:
            self.fecha_guardada = hoy 
            self.update_app_state()
        return self.fecha_guardada
    
    def get_week_state(self):
        return {
            "headers" : self.calendar_service.get_date_strings(),
        "week_start" : self.calendar_service.calculate_week_start(),
        "current_days" : self.calendar_service.current_week_days(),
        "weekly_performance" : self.metrics_service.calc_weekly_performance(),
        }

    def check_habit_today(self,habit_name):
        self.habit_service.complete_today(habit_name)
        self.rendimiento_semanal = self.metrics_service.calc_weekly_performance()
        logger.info(f"Habit completed today : {habit_name}")

    def check_habit_yesterday(self,habit_name):
            self.habit_service.complete_yesterday(habit_name)
            self.rendimiento_semanal = self.metrics_service.calc_weekly_performance()
            logger.info(f"Habit completed yesterday : {habit_name}") 

    def clean_deleted_habits(self):
        return self.habit_service.clean_deleted_habits()

    def get_habits_for_current_date(self, date):
        habits = self.habit_service.get_all_habits()

        return [
            {
                **h,
                "descripcion": h.get("descripcion", "Sin descripción")
            }
            for h in habits
            if self.calendar_service.habit_is_valid_for_date(
                h["dias_ejecucion"], date
            )
        ]

    def has_habits(self):
        return self.habit_service.habit_file_exists()

    def is_habit_completed_on_date(self,name,date_str):
        return self.habit_service.is_habit_completed(name,date_str)

    

    def get_month_state(self):
        return {
            "monthly_performance_avg": self.metrics_service.calc_monthly_performance(),
            "header" : self.calendar_service.get_month_header()
         }
    
    def get_month_header(self):
        return self.calendar_service.get_month_header()
    def load_phrase(self): 
        return self.phrase_service.get_phrase()

    def load_config(self):
        self.config =config_manager.load_config()
        config_manager.apply_config(config=self.config)

    def change_theme(self,new_theme): 
        config_manager.change_theme(self.config,new_theme)
    def change_appearance(self,new_appearance):
        config_manager.change_appearance(self.config,new_appearance)
    def change_font(self, new_font):
        config_manager.change_font(self.config,new_font)
    def load_theme_colors(self):
        return config_manager.load_theme_colors()
    
    def load_fonts(self):
        return config_manager.build_fonts()
    
    def get_monthly_performance_avg(self):
        return self.metrics_service.calc_average_monthly_performance()
    def get_month_days_range(self):
        return self.calendar_service.get_month_days_range()
    
    def get_weekly_performance(self):
        self.metrics_service.calc_weekly_performance()
    def get_daily_performance_in_month(self):
        return self.metrics_service.calc_daily_performance_in_month()
    
    def get_calendar_state(self):
        return self.calendar_service.get_calendar_state()
    
    def get_year_header(self):
        return self.calendar_service.get_year_header()
    def get_yearly_performance(self):
        return self.metrics_service.calc_yearly_performance()
    def get_month_names(self):
        return self.calendar_service.get_month_names()
    def reset_files(self):
        self.db.resetear_archivos()
