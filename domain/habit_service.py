from typing import Optional, Tuple, List 
import json
from infrastructure.logging.logger import get_logger 
from datetime import date,datetime
from datetime import timedelta
logger = get_logger(__name__)


class HabitService:
    def __init__(self, habit_repository,habit_config_repository):
        self.habit_repo = habit_repository
        self.habit_config_repo = habit_config_repository

    def get_start_tracking_date(self):
        if self.habit_repo.get_start_tracking_date() != None: 
            return datetime.strptime(self.habit_repo.get_start_tracking_date(), "%Y-%m-%d").date()
        return 
    
    def get_all(self):
        rows = self.habit_repo.get_all()

        habits = []
        for row in rows:

            configs_raw = self.habit_config_repo.get_all_by_habit_id(row["id"])

            configs = []
            for config in configs_raw:
                configs.append({
                    "id": config["id"],
                    "execution_days": json.loads(config["execution_days"]),
                    "is_active": config["is_active"],
                    "valid_from": datetime.strptime(config["valid_from"], "%Y-%m-%d").date(),
                    "valid_until": datetime.strptime(config["valid_until"], "%Y-%m-%d").date() if config["valid_until"] else None
                })

            habits.append({
                "id": row["id"],
                "habit_name": row["habit_name"],
                "configs": configs,
                "creation_date": datetime.strptime(row["creation_date"], "%Y-%m-%d").date(),
                "habit_color": row["habit_color"],
                "category": row["category"],
                "description": row["description"] or "Sin descripción"
            })

        return habits

    def get_by_id(self, habit_id):
        row = self.habit_repo.get_by_id(habit_id)

        configs_raw = self.habit_config_repo.get_all_by_habit_id(habit_id)

        configs = []
        for config in configs_raw:
            configs.append({
                "id": config["id"],
                "execution_days": json.loads(config["execution_days"]),
                "is_active": bool(config["is_active"]),
                "valid_from": datetime.strptime(config["valid_from"], "%Y-%m-%d").date(),
                "valid_until": datetime.strptime(config["valid_until"], "%Y-%m-%d").date() if config["valid_until"] else None
            })

        return {
            "id": row["id"],
            "habit_name": row["habit_name"],
            "configs": configs,
            "creation_date": datetime.strptime(row["creation_date"], "%Y-%m-%d").date(),
            "habit_color": row["habit_color"],
            "category": row["category"],
            "description": row["description"] or "Sin descripción"
        }
    
    def delete_by_id(self, habit_id): 
        self.habit_repo.delete_by_id(habit_id)

    def get_categories(self):
        return self.habit_repo.get_categories()
    
    def add_new(self, habit):
        today = date.today()

        habit_to_insert = (
            habit["name"],
            today,
            habit["color"],
            habit["category"],
            habit["description"]
        )

        habit_id = self.habit_repo.insert(habit_to_insert)

        initial_config = (
            habit_id,
            json.dumps(habit["execution_days"]),
            1,          # is_active
            today,      # valid_from
            None        # valid_until
        )

        self.habit_config_repo.insert(initial_config)

        logger.info(f"Habit created with ID {habit_id}")

    def update(self, modified_habit):
        logger.info(f"modified habit {modified_habit}")

        # 1. Actualizar datos base (SIN execution_days)
        habit_to_update = (
            modified_habit["name"],
            modified_habit["color"],
            modified_habit["category"],
            modified_habit["description"],
            modified_habit["id"]
        )

        self.habit_repo.update(habit_to_update)

        # 2. Obtener configs actuales
        habit = self.get_by_id(modified_habit["id"])
        configs = habit["configs"]

        latest_config = self.get_latest_config(configs)

        new_days = modified_habit["execution_days"]
        new_state = modified_habit["is_active"]

        if latest_config:
            current_days = latest_config["execution_days"]
            current_state = latest_config["is_active"]

            if  current_days == new_days and current_state == new_state :
                logger.info("No config change detected")
                return

            # 3. Cerrar config actual
            self.habit_config_repo.close_config(
                latest_config["id"],
                (date.today()- timedelta(days = 1))
            )

        # 4. Crear nueva config
        new_config = (
            modified_habit["id"],
            json.dumps(new_days),
            new_state,
            date.today(),
            None
        )

        self.habit_config_repo.insert(new_config)

        logger.info("New config version created")


    def get_latest_config(self, configs):
        return configs[-1] if configs else None
        


    def get_config_for_date(self, configs, target_date):
        for config in configs:
            if (
                config["valid_from"] <= target_date and
                (config["valid_until"] is None or config["valid_until"] >= target_date)
            ):
                return config
        return None
    

    def is_habit_scheduled_for_date(self, habit, target_date):

        # 1. No existía aún
        if habit["creation_date"] > target_date:
            return False

        config = self.get_config_for_date(
            habit["configs"],
            target_date
        )

        # 2. No hay config o está inactivo
        if not config or not config["is_active"]:
            return False

        weekday = (target_date.weekday() + 1) % 7

        return config["execution_days"][weekday]