from calendar import monthrange
from datetime import date

from infrastructure.logging.logger import get_logger 

logger = get_logger(__name__)

class MetricsService:
    def calculate_all_performances(
        self,
        habits,
        executions,
        current_week_days,
        current_month,
        current_month_year,
        current_year,
        today,
    ):
        """
        Método único para obtener:
        - weekly
        - monthly average
        - yearly
        """

        execution_index = self._index_executions(executions)

        weekly = self._calc_weekly(
            habits,
            execution_index,
            current_week_days
        )

        monthly_avg = self._calc_monthly_average(
            habits,
            execution_index,
            current_month,
            current_month_year
        )

        daily_month = self._calc_daily_month(
            habits,
            execution_index,
            current_month,
            current_month_year,
            today
        )



        yearly = self._calc_yearly(
            habits,
            execution_index,
            current_year
        )

        return {
            "weekly": weekly,
            "monthly": monthly_avg,
            "yearly": yearly,
            "daily_month" : daily_month
        }

    def _calc_daily(self, target_date, habits, execution_index):

        weekday = (target_date.weekday() + 1) % 7

        total = 0
        completed = 0

        for habit in habits:

            # 1. Ignorar hábitos no creados aún
            if habit["creation_date"] > target_date:
                continue

            # 2. Obtener config válida para esa fecha
            config = self._get_config_for_date(
                habit["configs"],
                target_date
            )

            # 3. Si no hay config o está inactiva → ignorar
            if not config or not config["is_active"]:
                continue

            # 4. Validar si ese día aplica
            if not config["execution_days"][weekday]:
                continue

            total += 1

            # 5. Validar ejecución
            if execution_index.get((habit["id"], target_date)):
                completed += 1

        if total == 0:
            return 0

        return (completed / total) * 100

    def _calc_weekly(self, habits, execution_index, week_days):

        performances = [
            self._calc_daily(day, habits, execution_index)
            for day in week_days
        ]

        return round(sum(performances) / len(performances))


    def _calc_monthly_average(self, habits, execution_index, month, year):

        days_in_month = monthrange(year, month)[1]

        performances = [
            self._calc_daily(date(year, month, d), habits, execution_index)
            for d in range(1, days_in_month + 1)
        ]

        return round(sum(performances) / days_in_month)


    def _calc_yearly(self, habits, execution_index, year):

        monthly_results = []

        for month in range(1, 13):
            days = monthrange(year, month)[1]

            total = 0
            for d in range(1, days + 1):
                total += self._calc_daily(
                    date(year, month, d),
                    habits,
                    execution_index
                )

            monthly_results.append(round(total / days))

        yearly_avg = round(sum(monthly_results) / 12, 2)

        return {
            "monthly": monthly_results,
            "yearly": yearly_avg
        }


    def _index_executions(self, executions):
        """
        Convierte lista de ejecuciones en dict:
        {(habit_id, date): True}
        Para lookup O(1)
        """
        return {
            (e["habit_id"], e["execution_date"]): e["executed"]
            for e in executions
            if e["executed"]
        }


    def _calc_daily_month(self, habits, execution_index, month, year,today):

        days_in_month = monthrange(year, month)[1]

        results = {}

        for day in range(1, days_in_month + 1):
            current_date = date(year, month, day)

            if current_date > today:
                results[day] = None
            else:
                results[day] = self._calc_daily(
                    current_date,
                    habits,
                    execution_index
                )

        return results
    



    def _get_config_for_date(self, configs, target_date):
        for config in configs:
            if (
                config["valid_from"] <= target_date and
                (config["valid_until"] is None or config["valid_until"] >= target_date)
            ):
                return config
        return None