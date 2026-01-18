class HabitService:
    def __init__(self, habit_repository):
        self.habit_repo = habit_repository

    def complete_today(self,habit_name):
        self.habit_repo.register_execution_today(habit_name)

    def complete_yesterday(self,habit_name):
        self.habit_repo.register_execution_yesterday(habit_name)