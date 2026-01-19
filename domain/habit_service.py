class HabitService:
    def __init__(self, habit_repository):
        self.habit_repo = habit_repository
        self.habits = self.get_all_habits()

    def habit_file_exists(self):
        return self.habit_repo.habit_file_exists()
    def get_all_habits(self):
        return self.habit_repo.get_habits()
        
    
    def complete_today(self,habit_name):
        self.habit_repo.register_execution_today(habit_name)

    def complete_yesterday(self,habit_name):
        self.habit_repo.register_execution_yesterday(habit_name)
    
    def load_habits(self):
        self.habit_repo.load_habits()
    
    def load_executions(self):
        return self.habit_repo.load_executions()

    def is_habit_completed(self, habit_name, date):
        
        date_str =date.isoformat()
        executions  = self.load_executions()
        return any(
            e["nombre_habito"] == habit_name and
            e["fecha_ejecucion"] == date_str and
            e.get("completado", False)
            for e in executions
        )
    
