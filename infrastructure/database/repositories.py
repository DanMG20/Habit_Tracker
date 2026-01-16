class HabitRepository: 
    def __init__(self,db):
        self.db = db


    
    def register_execution_today(self, habit_name): 
        self.db.registrar_ejecucion_habito(habit_name)