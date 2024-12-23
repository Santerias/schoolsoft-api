from .models import CalendarSettings, Language, Lesson, Store, Theme


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

    def get_language(self) -> Language:
        return Language.from_dict(
            self.api._request("get", "/calendar/student/language")
        )

    # always returns [] during my testing, can't make data-model unfortunately
    def get_news(self) -> dict:
        return self.api._request("get", "/calendar/student/news")

    # Completely useless in my opinion, no need to make data-models
    # for these endpoints
    def get_resource(self) -> dict:
        return self.api._request("get", "/calendar/student/resource")

    # Doesn't return anything at all
    def get_version(self) -> dict:
        return self.api._request("get", "/calendar/student/version")

    # these endpoints just return []
    def get_plannings(self) -> dict:
        return self.api._request("get", "/calendar/student/plannings")

    def get_time_bookings(self) -> dict:
        return self.api._request("get", "/calendar/student/time_bookings")
