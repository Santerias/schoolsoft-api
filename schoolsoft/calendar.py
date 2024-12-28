from .models import CalendarSettings, Language, Lesson, Store, Theme


class Calendar:
    """Class representing the calendar endpoint of the SchoolSoft REST API.

    Note:
        This class is not meant to be used on it's own and instead you should create an `Api` object and
        use the calendar attribute since the Api object initializes Calendar for you either way.

    Args:
        api (Api): Api object.
    """

    def __init__(self, api):
        self.api = api

    def get_lessons(self) -> list[Lesson]:
        """Gets a list of all lessons registered in the student's calendar.

        Returns:
            (list[Lesson]): List with Lesson objects, returns all lessons registered in the calendar
        """
        return [
            Lesson.from_dict(lesson_data)
            for lesson_data in self.api._request("get", "/calendar/student/lessons")
        ]

    def get_theme(self) -> Theme:
        """Gets the current theme of the calendar

        Returns:
            Theme: Theme object
        """
        return Theme.from_dict(self.api._request("get", "/calendar/theme"))

    def get_settings(self) -> CalendarSettings:
        """Gets the current settings of the calendar

        Returns:
            CalendarSettings: CalendarSettings object
        """
        return CalendarSettings.from_dict(
            self.api._request("get", "/calendar/student/settings")
        )

    def update_settings(self, settings: CalendarSettings | dict) -> CalendarSettings:
        """Updates the settings of the calendar with the provided data or object

        Args:
            settings (CalendarSettings or dict): Accepts either a CalendarSettings object or a dictionary

        Returns:
            CalendarSettings: Returns a CalendarSettings object
        """
        if isinstance(settings, CalendarSettings):
            data = CalendarSettings.to_dict(settings)
            response = self.api._request("put", "/calendar/student/settings", json=data)
            return CalendarSettings.from_dict(response)

        if isinstance(settings, dict):
            response = self.api._request(
                "put", "/calendar/student/settings", json=settings
            )
            return CalendarSettings.from_dict(response)

    def get_store(self) -> Store:
        """Gets the store of the calendar, containing teachers, grades and rooms

        Returns:
            Store: Store object containing the teachers, grades and rooms
        """
        return Store.from_dict(self.api._request("get", "/calendar/student/stores"))

    def get_language(self) -> Language:
        """Gets the current language of the calendar

        Returns:
            Language: Language object
        """
        return Language.from_dict(
            self.api._request("get", "/calendar/student/language")
        )

    def get_news(self) -> list:
        """Gets the current news of the calendar, usually set by the user themselves (not the same as a lesson in the calendar)

        Returns:
            list: list with news if any
        """
        return self.api._request("get", "/calendar/student/news")

    # Completely useless in my opinion, no need to make data-models
    # for these endpoints
    def get_resource(self) -> list:
        """Gets the current resource of the calendar

        Returns:
            list: list with resources if any
        """
        return self.api._request("get", "/calendar/student/resource")

    # Doesn't return anything at all
    def get_version(self) -> list:
        """Gets the current version of the calendar

        Returns:
            list: list with version if any (should always be empty)
        """
        return self.api._request("get", "/calendar/student/version")

    # these endpoints just return []
    def get_plannings(self) -> list:
        """Gets the current plannings of the calendar

        Returns:
            list: list with plannings if any
        """
        return self.api._request("get", "/calendar/student/plannings")

    def get_time_bookings(self) -> list:
        """Gets time bookings

        Returns:
            list: list with time bookings
        """
        return self.api._request("get", "/calendar/student/time_bookings")
