"""
Module providing calendar utility routines and navigational tracking timeline states.
"""

import calendar
from datetime import date, timedelta
from typing import Dict, List, Optional, Any
from dateutil.relativedelta import relativedelta
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class CalendarService:
    """
    Domain service responsible for tracking and navigating application timeline context.
    
    Manages current, historical, and dynamic boundaries for weeks, months, and years.
    """

    DAYS_OF_WEEK: List[str] = [
        "Domingo",
        "Lunes",
        "Martes",
        "Miércoles",
        "Jueves",
        "Viernes",
        "Sábado"
    ]

    MONTHS_OF_YEAR: List[str] = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    QUARTERLY_PERIODS: Dict[str, tuple] = {
        "1-13": (1, 13),
        "14-26": (14, 26),
        "27-39": (27, 39),
        "40-52": (40, 52),
    }

    def __init__(self, start_tracking_date: Optional[date] = None) -> None:
        """
        Initializes the CalendarService with optional baseline tracking date constraints.

        Args:
            start_tracking_date (Optional[date]): The earliest historical date allowed for tracking.
        """
        self.tracking_start_date: Optional[date] = start_tracking_date
        
        # Explicit type hinting declaration to avoid redundant double assignment
        self.today: date
        self.yesterday: date
        self.current_date: date
        self.current_month_date: date
        self.current_year_date: date
        
        self.reset_vars()

    # ======================== STATE ===========================
    def has_day_changed(self) -> bool:
        """
        Detects if the structural operational system calendar day shifted.

        Returns:
            bool: True if day changed and states were synchronized, False otherwise.
        """
        current_today: date = date.today()
        if current_today != self.today:
            logger.info(f"System day transition detected: {self.today} -> {current_today}")
            self.reset_vars()
            return True
        return False

    def get_today(self) -> date:
        return self.today
    
    def get_current_years(self) -> Dict[str, int]:
        return {
            "current_year": self.today.year,
            "next_year": (self.today + relativedelta(years=1)).year
        }

    def get_calendar_state(self) -> Dict[str, Any]:
        return {
            "today": self.today,
            "yesterday": self.yesterday,
            "current_year": self.today.year,
            "current_period": self.get_current_period()
        }

    def get_current_period(self) -> Optional[str]:
        iso_week: int = self.today.isocalendar().week
        for period_str, (start, end) in self.QUARTERLY_PERIODS.items():
            if start <= iso_week <= end:
                return period_str
        return None

    def reset_vars(self) -> None:
        """Synchronizes tracking references back to the real-world standard time snapshot."""
        self.today = date.today()
        self.yesterday = self.today - timedelta(days=1)
        self.current_date = self.today
        self.current_month_date = self.today
        self.current_year_date = self.today

    def get_date_headers(self) -> Dict[str, str]:
        weekday_index: int = (self.today.weekday() + 1) % 7
        today_string: str = self.DAYS_OF_WEEK[weekday_index]
        yesterday_string: str = self.DAYS_OF_WEEK[(weekday_index - 1) % 7]

        week_string: str = str((self.current_date + timedelta(days=1)).isocalendar().week)

        return {
            'today': f"HOY, {today_string} {self.today.day}",
            'weekly': f"Semana {week_string}",
            'monthly': self.get_month_header(),
            'yearly': str(self.get_year()),
            'yesterday': f"AYER, {yesterday_string} {self.yesterday.day}",
        }

    def calculate_week_start(self) -> date:
        return self.current_date - timedelta(days=(self.current_date.weekday() + 1) % 7)

    def get_current_week_days(self) -> List[date]:
        week_start: date = self.calculate_week_start()
        return [week_start + timedelta(days=i) for i in range(7)]

    def get_month_names(self) -> List[str]:
        return self.MONTHS_OF_YEAR

    def get_month_range(self) -> int:
        return calendar.monthrange(
            self.current_month_date.year, 
            self.current_month_date.month
        )[1]

    def get_month_header(self) -> str:
        # Zero-indexed array offset matches month index safely
        return self.MONTHS_OF_YEAR[self.current_month_date.month - 1]
    
    def get_month_nav(self) -> int:
        return self.current_month_date.month
    
    def get_year_month_nav(self) -> int:
        return self.current_month_date.year

    def get_year(self) -> int:
        return self.current_year_date.year

    # ======================== NAVIGATION ===========================
    def go_to_next_week(self) -> bool:
        if self.current_date <= self.today + timedelta(weeks=1):
            self.current_date += timedelta(weeks=1)
            return True
        logger.warning("Navigation constraints blocked advancement to the next week.")
        return False

    def go_to_previous_week(self) -> bool:
        if self.tracking_start_date and self.current_date <= self.tracking_start_date:
            logger.warning("Navigation constraints blocked backward step to the previous week.")
            return False
        self.current_date -= timedelta(weeks=1)
        return True

    def go_to_next_month(self) -> bool:
        if self.current_month_date <= self.today + relativedelta(months=1):
            self.current_month_date += relativedelta(months=1)
            return True
        logger.warning("Navigation constraints blocked advancement to the next month.")
        return False

    def go_to_previous_month(self) -> bool:
        if self.tracking_start_date and self.current_month_date <= self.tracking_start_date:
            logger.warning("Navigation constraints blocked backward step to the previous month.")
            return False
        self.current_month_date -= relativedelta(months=1)
        return True
    
    def go_to_next_year(self) -> bool:
        if self.current_year_date <= self.today + relativedelta(years=1):
            self.current_year_date += relativedelta(years=1)
            logger.info(f"Active timeline year advanced to: {self.current_year_date.year}")
            return True
        logger.warning("Navigation constraints blocked advancement to the next year.")
        return False

    def go_to_previous_year(self) -> bool:
        if self.tracking_start_date and self.current_year_date <= self.tracking_start_date:
            logger.warning("Navigation constraints blocked backward step to the previous year.")
            return False
        self.current_year_date -= relativedelta(years=1)
        logger.info(f"Active timeline year reverted to: {self.current_year_date.year}")
        return True

    def habit_is_valid_for_date(self, execution_days: List[bool], target_date: date) -> bool:
        return execution_days[self.get_weekday_index(target_date)]

    def get_weekday_index(self, target_date: date) -> int:
        return (target_date.weekday() + 1) % 7