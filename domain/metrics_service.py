"""
Module providing metric processing routines to evaluate weekly, monthly, and yearly habit execution performance.
"""

from calendar import monthrange
from datetime import date
from typing import List, Dict, Tuple, Any, Optional

from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class MetricsService:
    """
    Domain service responsible for statistical aggregations and habit tracking performance analytics.
    """

    DAYS_IN_WEEK: int = 7
    MONTHS_IN_YEAR: int = 12

    def calculate_all_performances(
        self,
        habits: List[Dict[str, Any]],
        executions: List[Dict[str, Any]],
        current_week_days: List[date],
        current_month: int,
        current_month_year: int,
        current_year: int,
        reference_date: date,
    ) -> Dict[str, Any]:
        """
        Executes a consolidated analytical batch calculation for all tracking temporal scopes.

        Args:
            habits (List[Dict[str, Any]]): The collection of registered domain habits.
            executions (List[Dict[str, Any]]): Raw transaction execution rows.
            current_week_days (List[date]): Collection of dates matching the active week view window.
            current_month (int): Numerical index of the target month (1-12).
            current_month_year (int): Calendar year of the targeted month.
            current_year (int): Calendar year context for yearly reports.
            reference_date (date): Operational system date constraint representing 'today'.

        Returns:
            Dict[str, Any]: A structural summary payload containing analytical scores.
        """
        execution_index: Dict[Tuple[int, date], bool] = self._index_executions(executions)

        weekly_score: int = self._calc_weekly(habits, execution_index, current_week_days)
        
        monthly_avg: int = self._calc_monthly_average(
            habits, execution_index, current_month, current_month_year
        )

        daily_month_grid: Dict[int, Optional[float]] = self._calc_daily_month(
            habits, execution_index, current_month, current_month_year, reference_date
        )

        yearly_report: Dict[str, Any] = self._calc_yearly(habits, execution_index, current_year)

        return {
            "weekly": weekly_score,
            "monthly": monthly_avg,
            "yearly": yearly_report,
            "daily_month": daily_month_grid
        }

    def _calc_daily(
        self, 
        target_date: date, 
        habits: List[Dict[str, Any]], 
        execution_index: Dict[Tuple[int, date], bool]
    ) -> float:
        weekday_index: int = (target_date.weekday() + 1) % self.DAYS_IN_WEEK
        total_scheduled: int = 0
        total_completed: int = 0

        for habit in habits:
            if habit["creation_date"] > target_date:
                continue

            config: Optional[Dict[str, Any]] = self._get_config_for_date(habit["configs"], target_date)
            if not config or not config["is_active"]:
                continue

            if not config["execution_days"][weekday_index]:
                continue

            total_scheduled += 1

            if execution_index.get((habit["id"], target_date)):
                total_completed += 1

        if total_scheduled == 0:
            return 0.0

        return (total_completed / total_scheduled) * 100.0

    def _calc_weekly(
        self, 
        habits: List[Dict[str, Any]], 
        execution_index: Dict[Tuple[int, date], bool], 
        week_days: List[date]
    ) -> int:
        if not week_days:
            return 0
            
        performances: List[float] = [
            self._calc_daily(day_entity, habits, execution_index)
            for day_entity in week_days
        ]
        return round(sum(performances) / len(week_days))

    def _calc_monthly_average(
        self, 
        habits: List[Dict[str, Any]], 
        execution_index: Dict[Tuple[int, date], bool], 
        month: int, 
        year: int
    ) -> int:
        days_in_month: int = monthrange(year, month)[1]

        performances: List[float] = [
            self._calc_daily(date(year, month, day_idx), habits, execution_index)
            for day_idx in range(1, days_in_month + 1)
        ]
        return round(sum(performances) / days_in_month)

    def _calc_yearly(
        self, 
        habits: List[Dict[str, Any]], 
        execution_index: Dict[Tuple[int, date], bool], 
        year: int
    ) -> Dict[str, Any]:
        monthly_results: List[int] = []
        total_yearly_days: int = 0
        accumulated_performance: float = 0.0

        for month in range(1, self.MONTHS_IN_YEAR + 1):
            days_in_month: int = monthrange(year, month)[1]
            total_yearly_days += days_in_month

            month_sum: float = 0.0
            for day_idx in range(1, days_in_month + 1):
                day_score: float = self._calc_daily(date(year, month, day_idx), habits, execution_index)
                month_sum += day_score
                accumulated_performance += day_score

            monthly_results.append(round(month_sum / days_in_month))

        # Mathematical Correction: Yearly average calculated directly over absolute valid tracking days
        yearly_avg: float = round(accumulated_performance / total_yearly_days, 2)

        return {
            "monthly": monthly_results,
            "yearly": yearly_avg
        }

    def _index_executions(self, executions: List[Dict[str, Any]]) -> Dict[Tuple[int, date], bool]:
        return {
            (item["habit_id"], item["execution_date"]): bool(item["executed"])
            for item in executions
            if item["executed"]
        }

    def _calc_daily_month(
        self, 
        habits: List[Dict[str, Any]], 
        execution_index: Dict[Tuple[int, date], bool], 
        month: int, 
        year: int,
        reference_date: date
    ) -> Dict[int, Optional[float]]:
        days_in_month: int = monthrange(year, month)[1]
        results: Dict[int, Optional[float]] = {}

        for day_idx in range(1, days_in_month + 1):
            current_date: date = date(year, month, day_idx)

            if current_date > reference_date:
                results[day_idx] = None
            else:
                results[day_idx] = self._calc_daily(current_date, habits, execution_index)

        return results

    def _get_config_for_date(self, configs: List[Dict[str, Any]], target_date: date) -> Optional[Dict[str, Any]]:
        for config in configs:
            if config["valid_from"] <= target_date and (config["valid_until"] is None or config["valid_until"] >= target_date):
                return config
        return None