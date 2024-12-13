class Calendar:
    def __init__(self, api):
        self.api = api

    def get_calendar_student_lessons(self) -> dict:
        return self.api._request("get", "/calendar/student/lessons")

    def get_calendar_theme(self) -> dict:
        return self.api._request("get", "/calendar/theme")

    def get_calendar_student_settings(self) -> dict:
        return self.api._request("get", "/calendar/student/settings")

    def put_calendar_student_settings(self, data) -> dict:
        return self.api._request("put", "/calendar/student/settings", data)

    def get_calendar_student_stores(self) -> dict:
        return self.api._request("get", "/calendar/student/stores")

    def get_calendar_student_resource(self) -> dict:
        return self.api._request("get", "/calendar/student/resource")

    def get_calendar_student_language(self) -> dict:
        return self.api._request("get", "/calendar/student/language")

    def get_calendar_student_news(self) -> dict:
        return self.api._request("get", "/calendar/student/news")

    def get_calendar_student_version(self) -> dict:
        return self.api._request("get", "/calendar/student/version")

    def get_calendar_student_plannings(self) -> dict:
        return self.api._request("get", "/calendar/student/plannings")

    def get_calendar_student_time_bookings(self) -> dict:
        return self.api._request("get", "/calendar/student/time_bookings")
