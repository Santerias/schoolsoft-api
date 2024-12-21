from .models import Lesson, Store, Theme, CalendarSettings


class Calendar:
    def __init__(self, api):
        self.api = api

    def get_lessons(self) -> list[Lesson]:
        return [
            Lesson.from_dict(lesson_data)
            for lesson_data in self.api._request("get", "/calendar/student/lessons")
        ]

    def get_theme(self) -> Theme:
        return Theme.from_dict(self.api._request("get", "/calendar/theme"))

    def get_settings(self) -> CalendarSettings:
        return CalendarSettings.from_dict(
            self.api._request("get", "/calendar/student/settings")
        )

    def update_settings(self, settings: CalendarSettings | dict) -> CalendarSettings:
        if isinstance(settings, CalendarSettings):
            data = CalendarSettings.to_dict(settings)
            response = self.api._request("put", "/calendar/student/settings", json=data)
            return CalendarSettings.from_dict(response)

        if isinstance(settings, dict):
            response = self.api._request(
                "put", "/calendar/student/settings", json=settings
            )
            return CalendarSettings.from_dict(response)

        return None

    def get_store(self) -> Store:
        return Store.from_dict(self.api._request("get", "/calendar/student/stores"))

    def fetch_student_resource(self) -> dict:
        return self.api._request("get", "/calendar/student/resource")

    def fetch_student_language(self) -> dict:
        return self.api._request("get", "/calendar/student/language")

    def fetch_student_news(self) -> dict:
        return self.api._request("get", "/calendar/student/news")

    def fetch_student_version(self) -> dict:
        return self.api._request("get", "/calendar/student/version")

    def fetch_student_plannings(self) -> dict:
        return self.api._request("get", "/calendar/student/plannings")

    def fetch_student_time_bookings(self) -> dict:
        return self.api._request("get", "/calendar/student/time_bookings")
