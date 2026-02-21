from typing import Optional, Tuple, List 
import json
from infrastructure.logging.logger import get_logger 
from datetime import date,datetime
logger = get_logger(__name__)


class HabitService:
    def __init__(self, habit_repository):
        self.habit_repo = habit_repository


    def get_start_tracking_date(self):
        if self.habit_repo.get_start_tracking_date() != None: 
            return datetime.strptime(self.habit_repo.get_start_tracking_date(), "%Y-%m-%d").date()
        return 


    def get_all(self):
        rows = self.habit_repo.get_all()
        habits = []
        for row in rows:
            habits.append({
                "id": row["id"],
                "habit_name": row["habit_name"],
                "execution_days": json.loads(row["execution_days"]), 
                "creation_date":  datetime.strptime(row["creation_date"], "%Y-%m-%d").date(),               
                "habit_color": row["habit_color"],
                "category": row["category"],
                "description": row["description"] or "Sin descripción"
            })
        return habits


    

    def get_by_id(self, habit_id): 
        row = self.habit_repo.get_by_id(habit_id)

        return ({
                "id": row["id"],
                "habit_name": row["habit_name"],
                "execution_days": json.loads(row["execution_days"]), 
                "creation_date":  datetime.strptime(row["creation_date"], "%Y-%m-%d").date(),               
                "habit_color": row["habit_color"],
                "category": row["category"],
                "description": row["description"] or "Sin descripción"
            })



    def delete_by_id(self, habit_id): 
        self.habit_repo.delete_by_id(habit_id)

    def get_categories(self):
        return self.habit_repo.get_categories()
    
    def add_new(self,habit):
        execution_days_json = json.dumps(habit["execution_days"])
        habit_to_insert = (
        habit["name"],
        execution_days_json,
        date.today(),
        habit["color"],
        habit["category"],
        habit["description"]
        )
        self.habit_repo.insert(habit_to_insert)

    def update(self,modified_habit): 
        execution_days_json = json.dumps(modified_habit["execution_days"])
        habit_to_update = (
        modified_habit["name"],
        execution_days_json,
        modified_habit["color"],
        modified_habit["category"],
        modified_habit["description"],
        modified_habit["id"]
        )
        self.habit_repo.update(habit_to_update)
