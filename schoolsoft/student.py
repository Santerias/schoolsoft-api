from .models import School, User


class Student:
    """Class representing the student endpoint of the SchoolSoft REST API.

    Note:
        Needs to be used together with `Api` class, otherwise none of the functions will work
        since it requires you to be authenticated

    Args:
        api (Api): Api object.
    """

    def __init__(self, api):
        self.api = api

    def get_student(self) -> User:
        """Get student information such as first and last name and etc.

        Returns:
            User: Returns an object which contains first, name, pfp and etc.
        """

        return User(**self.api._request("get", "/student/header/student"))

    def get_schools(self) -> list[School]:
        """Get schools the Student is assigned to

        Returns:
            list[School]: Returns a list of schools the user is registered in
        """

        return [
            School(**school)
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
