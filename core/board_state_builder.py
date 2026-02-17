class BoardStateBuilder:

    def __init__(self, calendar_service):
        self.calendar_service = calendar_service

    def build(self, habits, executions, today, week_days):

        return {
            "today": today,
            "habits": habits,
            "executions": executions,
            "week_days": week_days,
            "week_start": self.calendar_service.calculate_week_start()
        }
