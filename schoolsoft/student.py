from .models import School, User


class Student:
    def __init__(self, api):
        self.api = api

    def get_student(self) -> User:
        return User.from_dict(self.api._request("get", "/student/header/student"))

    def get_schools(self) -> list[School]:
        return [
            School.from_dict(school)
            for school in self.api._request("get", "/student/header/schools")
        ]

    def get_skolon(self) -> dict:
        return self.api._request("get", "/student/header/skolon")

    def get_school_logo(self) -> dict:
        return self.api._request("get", "/student/logo")

    def get_sidebar_sectiongroups(self) -> dict:
        return self.api._request("get", "/student/sidebar/sectiongroups")

    def get_sidebar_autocompleteoptions(self) -> dict:
        return self.api._request("get", "/student/sidebar/autocompleteoptions")
