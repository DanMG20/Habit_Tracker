from typing import List, Tuple, Optional 
from infrastructure.logging.logger import get_logger 
from datetime import date,datetime
logger = get_logger(__name__)
class GoalService:

    def __init__(self,goal_repo):
        self.goal_repo = goal_repo

    def get_all(self) -> List[dict]:
        rows = self.goal_repo.get_all()
        goals = []
        periods = {
            1: "1-13",
            2: "14-26",
            3: "27-39",
            4: "40-52",
        }

        for row in rows:
            goals.append({
                "id": row["id"],
                "goal_name": row["goal_name"],
                "description": row["description"],
                "period_year": row["period_year"],
                "period_quarter": periods.get(row["period_quarter"], "Unknown"),
                "is_completed": bool(row["is_completed"]),
                "completed_at": datetime.strptime(row["completed_at"], "%Y-%m-%d").date()
                                if row["completed_at"] is not None else None,
                "created_at": datetime.strptime(row["created_at"], "%Y-%m-%d").date()
            })

        return goals
    
    def get_all_per_year(self,year): 
        rows = self.goal_repo.get_all_per_year(year)
        goals = []
        periods = {
            1: "1-13",
            2: "14-26",
            3: "27-39",
            4: "40-52",
        }

        for row in rows:
            goals.append({
                "id": row["id"],
                "goal_name": row["goal_name"],
                "description": row["description"],
                "period_year": row["period_year"],
                "period_quarter": periods.get(row["period_quarter"], "Unknown"),
                "is_completed": bool(row["is_completed"]),
                "completed_at": datetime.strptime(row["completed_at"], "%Y-%m-%d").date()
                                if row["completed_at"] is not None else None,
                "created_at": datetime.strptime(row["created_at"], "%Y-%m-%d").date()
            })

        return goals

    

    def get_completed_on_year(self,year) -> List[dict]:
        rows = self.goal_repo.get_completed_on_year(year)
        goals = []
        periods = {
            1: "1-13",
            2: "14-26",
            3: "27-39",
            4: "40-52",
        }

        for row in rows:
            goals.append({
                "id": row["id"],
                "goal_name": row["goal_name"],
                "description": row["description"],
                "period_year": row["period_year"],
                "period_quarter": periods.get(row["period_quarter"], "Unknown"),
                "is_completed": bool(row["is_completed"]),
                "completed_at": datetime.strptime(row["completed_at"], "%Y-%m-%d").date()
                                if row["completed_at"] is not None else None,
                "created_at": datetime.strptime(row["created_at"], "%Y-%m-%d").date()
            })

        return goals

    def get_rate_per_year(self, year): 
        completed_str = str(len(self.get_completed_on_year(year)))
        total_str = str(len(self.get_all_per_year(year)))
        logger.info(completed_str)
        logger.info(total_str)
        return  (f"({completed_str}/{total_str})")

    def is_goal_completed(self, goal_id):
        goals = self.get_goals_completed_on_year()
        return any(
            goal["id"] == goal_id
            and goal.get("completed_at",False) 
            for goal in goals
        )
    



    def complete_goal(self, goal_id,date):
        date_str = date.strftime("%Y-%m-%d")
        self.goal_repo.complete(goal_id,date_str,1)
 
    def get_goals_completed_on_date(self, date):
        goals = self.get_goals_completed_on_year()
        return {
            goal["id"]
            for goal in goals
            if goal["completed_at"] >= date and goal["is_completed"]
        }

    def update(self,id, new_name, new_period, new_year):

        self.goal_repo.update(id,new_name,self.convert_period(new_period),new_year)

    def convert_period(self, str_period):
        periods = {
            "1-13": 1,
            "14-26":2,
            "27-39":3,
            "40-52":4,
        }

        return periods[str_period]

    def insert(self, name, year, period, created_at):
        created_at_str = created_at.strftime("%Y-%m-%d")
        self.goal_repo.insert(name, "DEFAULT",int(year), self.convert_period(period), created_at_str)

    def delete_by_id(self, goal_id): 
        self.goal_repo.delete_by_id(goal_id)