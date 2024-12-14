class Student:
    def __init__(self, api):
        self.api = api

    def fetch_header_student(self) -> dict:
        return self.api._request("get", "/student/header/student")

    def fetch_header_schools(self) -> dict:
        return self.api._request("get", "/student/header/schools")

    def fetch_header_skolon(self) -> dict:
        return self.api._request("get", "/student/header/skolon")

    def fetch_logo(self) -> dict:
        return self.api._request("get", "/student/logo")

    def fetch_sidebar_sectiongroups(self) -> dict:
        return self.api._request("get", "/student/sidebar/sectiongroups")

    def fetch_sidebar_autocompleteoptions(self) -> dict:
        return self.api._request("get", "/student/sidebar/autocompleteoptions")
