class Calendar:
    def __init__(self, api):
        self.api = api

    def fetch_student_lessons(self) -> dict:
        return self.api._request("get", "/calendar/student/lessons")

    def fetch_theme(self) -> dict:
        return self.api._request("get", "/calendar/theme")

    def fetch_student_settings(self) -> dict:
        return self.api._request("get", "/calendar/student/settings")

    def put_calendar_student_settings(self, data) -> dict:
        return self.api._request("put", "/calendar/student/settings", data)

    def fetch_student_stores(self) -> dict:
        return self.api._request("get", "/calendar/student/stores")

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
