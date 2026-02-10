from typing import List, Tuple, Optional 
from infrastructure.logging.logger import get_logger 
from datetime import date,datetime
logger = get_logger(__name__)
class ExecutionService:

    def __init__(self,execution_repo):
        self.execution_repo = execution_repo

    def get_all(self) -> Tuple[int,int,date,bool]:
        rows = self.execution_repo.get_all()
        executions = []
        for row in rows: 
            executions.append({
                "id": row["id"],
                "habit_id" : row["habit_id"],
                "execution_date" : datetime.strptime(
                    row["execution_date"], "%Y-%m-%d").date(),
                "executed": bool(row["executed"])
            })
        return executions


    def is_habit_completed(self, habit_name, date):
        executions = self.get_all()
        return any(
            e["habit_id"] == habit_name
            and e["execution_date"] == date
            and e.get("executed", False)
            for e in executions
        )

    def complete_habit_on_date(self, habit_id,date):
        logger.info("Puede que quite esta parte del codigo")
        date_str = date.strftime("%Y-%m-%d")
        executions = self.get_all()

        if any(
            execution["habit_id"] == habit_id
            and execution["execution_date"] == date
            for execution in executions
        ):
            return
            """           CTkMessagebox(master=self.master,
                          font=styles.FUENTE_PEQUEÑA,
                          message=("Información", f"El hábito '{nombre_habito}' ya fue completado hoy."),
                          icon="check", option_1="Aceptar") """
        
        self.execution_repo.insert((habit_id,date_str,1))
        """         CTkMessagebox(master=self.master,
                            font=styles.FUENTE_PEQUEÑA,
                            message=("Éxito", f"Se registró como completado el hábito '{nombre_habito}' para hoy."),
                            icon="check", option_1="Aceptar")
        """

    def get_habits_completed_on_date(self, date):
        executions = self.get_all()
        return {
            e["habit_id"]
            for e in executions
            if e["execution_date"] == date and e["executed"]
        }

