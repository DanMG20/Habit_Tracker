class HabitRepository: 
    def __init__(self,db):
        self.db = db

    def register_execution_today(self, habit_name): 
        self.db.registrar_ejecucion_habito(habit_name)

    def register_execution_yesterday(self,habit_name):
        self.db.registrar_ejecucion_habito_ayer(habit_name)

    def get_start_tracking_date(self): 
        return self.db.get_start_tracking_date()
    

class PhraseRepository:
    def __init__(self,db):
        self.db = db
    
    def load_random_phrase(self):
        self.db.load_random_phrase()

    def get_phrase(self):
        return self.db.get_phrase()
    def get_phrases(self):
        return  self.db.get_phrases()
    def delete_selected_phrase(self,selected_phrase):
        self.db.delete_selected_phrase(selected_phrase)
