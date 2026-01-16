from datetime import datetime

class AppController: 
    def __init__(self, habit_service , db, calendar): 
        self.db = db # TEMPORAL OJOOOO
        self.calendar = calendar # TEMPORAAAAL 
        self.habit_service = habit_service
        self.fecha_guardada = datetime.now().date()

    def update_app(self):
        print("El programa se ha actualizado")
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

    def go_previus_week(self):
        self.calendar.semana_anterior()

    def go_next_week(self):
        self.calendar.semana_siguiente()

    def verify_date(self):
        hoy = datetime.now().date()
        if hoy != self.fecha_guardada:
            self.fecha_guardada = hoy 
            self.update_app()
        return self.fecha_guardada
    
    def get_week_state(self):
        return {
            "headers" : self.calendar.date_vars(),
        "week_start" : self.calendar.inicio_semana(),
        "current_days" : self.calendar.dias_actuales(),
        "weekly_performance" : self.calendar.calcular_rendimiento_semanal(),
        }

    def check_habit_today(self,habit_name):
        self.habit_service.complete_today(habit_name)
        self.rendimiento_semanal = self.calendar.calcular_rendimiento_semanal()
