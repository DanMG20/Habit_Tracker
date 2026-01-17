from datetime import date, timedelta
import calendar
from dateutil.relativedelta import relativedelta
import locale
from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')


class CalendarService:
    def __init__(self, start_tracking_date: date | None = None):
        self.tracking_start_date = start_tracking_date
        self.reset_vars()
        logger.info("Tracking start date: %s", self.tracking_start_date)

    # ======================== ESTADO ===========================

    def reset_vars(self):
        self.TODAY = date.today()
        self.YESTERDAY = self.TODAY - timedelta(days=1)
        self.current_date = date.today()
        self.current_month_date = date.today()
        self.current_year_date = date.today()

    def get_date_strings(self):
        CURRENT_MONTH = self.TODAY.strftime("%B")
        CURRENT_YEAR = self.TODAY.year

        DAY_STRING = [
            "Domingo", "Lunes", "Martes",
            "Miércoles", "Jueves", "Viernes", "Sábado"
        ]

        weekday_index = (self.TODAY.weekday() + 1) % 7
        today_string = DAY_STRING[weekday_index]
        yesterday_string = DAY_STRING[(weekday_index - 1) % 7]

        week_string = str((self.current_date + timedelta(days=1)).isocalendar().week)

        return (
            f"HOY, {today_string} {self.TODAY.day}",
            f"Semana {week_string}",
            CURRENT_MONTH,
            CURRENT_YEAR,
            f"AYER, {yesterday_string} {self.YESTERDAY.day}",
        )

    def calculate_week_start(self):
        """Returns Sunday of the current week"""
        return self.current_date - timedelta(
            days=(self.current_date.weekday() + 1) % 7
        )

    def current_week_days(self):
        week_start = self.calculate_week_start()
        return [week_start + timedelta(days=i) for i in range(7)]

    def get_month_names(self):
        return [calendar.month_name[m] for m in range(1, 13)]

    def get_month_days_range(self):
        return calendar.monthrange(
            self.current_month_date.year,
            self.current_month_date.month
        )[1]

    def get_month_header(self):
        return self.current_month_date.strftime("%B")

    def get_year_header(self):
        return self.current_year_date.year

    # ======================== NAVEGACIÓN ===========================

    def go_to_next_week(self):
        if self.current_date <= self.TODAY + timedelta(weeks=1):
            self.current_date += timedelta(weeks=1)
            logger.info("Week changed to %s", self.current_date)
        else:
            logger.warning("It's not possible to go next week")

    def go_to_previous_week(self):
        if self.tracking_start_date and self.current_date <= self.tracking_start_date:
            logger.warning("It's not possible to go previous week")
            return

        self.current_date -= timedelta(weeks=1)
        logger.info("Week changed to %s", self.current_date)

    def go_to_next_month(self):
        if self.current_month_date <= self.TODAY + relativedelta(months=1):
            self.current_month_date += relativedelta(months=1)
            logger.info("Month changed to %s", self.current_month_date)
        else:
            logger.warning("It's not possible to go next month")

    def go_to_previous_month(self):
        if self.tracking_start_date and self.current_month_date <= self.tracking_start_date:
            logger.warning("It's not possible to go previous month")
            return

        self.current_month_date -= relativedelta(months=1)
        logger.info("Month changed to %s", self.current_month_date)

    def go_to_next_year(self):
        if self.current_year_date <= self.TODAY + relativedelta(years=1):
            self.current_year_date += relativedelta(years=1)
            logger.info("Year changed to %s", self.current_year_date)
        else:
            logger.warning("It's not possible to go next year")

    def go_to_previous_year(self):
        if self.tracking_start_date and self.current_year_date <= self.tracking_start_date:
            logger.warning("It's not possible to go previous year")
            return

        self.current_year_date -= relativedelta(years=1)
        logger.info("Year changed to %s", self.current_year_date)
