import calendar
import locale
from datetime import date, timedelta

from dateutil.relativedelta import relativedelta

from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")


class CalendarService:
    def __init__(self, start_tracking_date: date | None = None):
        self.tracking_start_date =  start_tracking_date
        self.reset_vars()

    # ======================== ESTADO ===========================

    def get_today(self):
        return self.TODAY
    
    def get_current_years(self):
        return({
            "current_year" : self.TODAY.year,
            "next_year" : (self.TODAY + relativedelta(years=1)).year
        })
        

    def get_calendar_state(self):
        return {
            "today": self.TODAY,
            "yesterday": self.YESTERDAY,
        }
    def get_current_period(self):
        trimestral_periods = {
            "1-13": (1,13),
            "14-26":(14,26),
            "27-39":(27,39),
            "40-52":(40,52),
        }
        for period_str,period in trimestral_periods.items():
            if self.TODAY.isocalendar().week>= period[0] and self.TODAY.isocalendar().week<= period[1]:
                return period_str



    def reset_vars(self):
        self.TODAY = date.today()
        self.YESTERDAY = self.TODAY - timedelta(days=1)
        self.current_date = date.today()
        self.current_month_date = date.today()
        self.current_year_date = date.today()

    def get_date_headers(self):
        DAY_STRING = [
            "Domingo",
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
        ]

        weekday_index = (self.TODAY.weekday() + 1) % 7
        today_string = DAY_STRING[weekday_index]
        yesterday_string = DAY_STRING[(weekday_index - 1) % 7]

        week_string = str((self.current_date + timedelta(days=1)).isocalendar().week)

        return ({
            'today' :f"HOY, {today_string} {self.TODAY.day}",
            'weekly':f"Semana {week_string}",
            'monthly': self.get_month_header(),
            'yearly': self.get_year(),
            'yesterday' :f"AYER, {yesterday_string} {self.YESTERDAY.day}",
        })

    def calculate_week_start(self):
        """Returns Sunday of the current week"""
        return self.current_date - timedelta(days=(self.current_date.weekday() + 1) % 7)

    def current_week_days(self):
        week_start = self.calculate_week_start()
        return [week_start + timedelta(days=i) for i in range(7)]

    def get_month_names(self):
        return [calendar.month_name[m] for m in range(1, 13)]

    def get_month_range(self):
        return calendar.monthrange(
            self.current_month_date.year, self.current_month_date.month
        )[1]

    def get_month_header(self):
        return self.current_month_date.strftime("%B")
    
    def get_month_nav(self):
        return self.current_month_date.month
    
    def get_year_month_nav(self):
        return self.current_month_date.year

    def get_year(self):
        return self.current_year_date.year

    # ======================== NAVEGACIÓN ===========================

    def go_to_next_week(self):
        if self.current_date <= self.TODAY + timedelta(weeks=1):
            self.current_date += timedelta(weeks=1)
            return True
        logger.warning("It's not possible to go next week")
        return False

    def go_to_previous_week(self):
        if self.tracking_start_date and self.current_date <= self.tracking_start_date:
            logger.warning("It's not possible to go previous week")
            return False
        self.current_date -= timedelta(weeks=1)
        return True

    def go_to_next_month(self):
        if self.current_month_date <= self.TODAY + relativedelta(months=1):
            self.current_month_date += relativedelta(months=1)
            return True
    
        logger.warning("It's not possible to go next month")
        return False
    def go_to_previous_month(self):
        if (
            self.tracking_start_date
            and self.current_month_date <= self.tracking_start_date
        ):
            logger.warning("It's not possible to go previous month")
            return False

        self.current_month_date -= relativedelta(months=1)
        return True
    
    def go_to_next_year(self):
        if self.current_year_date <= self.TODAY + relativedelta(years=1):
            self.current_year_date += relativedelta(years=1)
            logger.info("Year changed to %s", self.current_year_date)
            return True
        
        logger.warning("It's not possible to go next year")
        return False

    def go_to_previous_year(self):
        if (
            self.tracking_start_date
            and self.current_year_date <= self.tracking_start_date
        ):
            logger.warning("It's not possible to go previous year")
            return False

        self.current_year_date -= relativedelta(years=1)
        logger.info("Year changed to %s", self.current_year_date)
        return True

    def habit_is_valid_for_date(self, execution_days, date) -> bool:

        return execution_days[self.get_weekday_index(date)]

    def get_weekday_index(self, date: date) -> int:
        return (date.weekday() + 1 ) % 7
    
    
