from infrastructure.logging.logger import get_logger

logger = get_logger(__name__)


class GraphStateBuilder:

    def __init__(self, calendar_service, metrics_service):
        self.calendar_service = calendar_service
        self.metrics_service = metrics_service

    def build(self, month_year, performances):

        month_range = self.calendar_service.get_month_range()
        month_names = self.calendar_service.get_month_names()

        return {
            "monthly": {
                "month_range": month_range,
                "daily_performance": performances.get("daily_month", {}),
                "year": month_year
            },
            "yearly": {
                "month_names": month_names,
                "monthly_performance": performances["yearly"]["monthly"],
            }
        }
