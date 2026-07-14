"""
Module responsible for building the state specific to the analytical performance graphs.
"""

from typing import Dict, Any, List


class GraphStateBuilder:
    """
    Factory class that aggregates and shapes calendar ranges and performance metrics 
    to yield the state payload needed by monthly and yearly graphs.
    """

    def __init__(self, calendar_service: Any, metrics_service: Any) -> None:
        self.calendar_service: Any = calendar_service
        self.metrics_service: Any = metrics_service

    def build(self, month_year: Any, performances: Dict[str, Any]) -> Dict[str, Any]:
        month_range: List[int] = self.calendar_service.get_month_range()
        month_names: List[str] = self.calendar_service.get_month_names()

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