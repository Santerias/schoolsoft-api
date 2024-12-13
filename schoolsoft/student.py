class Student:
    def __init__(self, api):
        self.api = api

    def get_student_header_student(self) -> dict:
        return self.api._request("get", "/student/header/student")

    def get_student_header_schools(self) -> dict:
        return self.api._request("get", "/student/header/schools")

    def get_student_header_skolon(self) -> dict:
        return self.api._request("get", "/student/header/skolon")

    def get_student_logo(self) -> dict:
        return self.api._request("get", "/student/logo")

    def get_student_sidebar_sectiongroups(self) -> dict:
        return self.api._request("get", "/student/sidebar/sectiongroups")

    def get_student_sidebar_autocompleteoptions(self) -> dict:
        return self.api._request("get", "/student/sidebar/autocompleteoptions")
