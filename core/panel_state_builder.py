class PanelStateBuilder:

    def __init__(self, calendar_service, executions_service, habit_service):
        self.calendar_service = calendar_service
        self.executions_service = executions_service
        self.habit_service = habit_service

    def build_check_panel(self, date, habits):
        return {
            "habits": [
                h for h in habits
                if self.habit_service.is_habit_scheduled_for_date(h, date)
            ],
            "completed": self.executions_service
                .get_habits_completed_on_date(date),
            "date": date,
        }

    def build_static_panel(self, habits):
        return {
            "habits": habits,
            "completed": []
        }