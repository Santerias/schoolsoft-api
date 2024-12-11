#!/usr/bin/env python3
import requests
import os
from sys import exit
from datetime import datetime
from dotenv import load_dotenv
from bs4 import BeautifulSoup


class Api:
    def __init__(self, username, password, school):
        self.username = username
        self.password = password
        self.school = school
        self.session = requests.Session()
        self.base_url = f"https://sms.schoolsoft.se/{self.school}"
        self.rest_url = f"{self.base_url}/rest-api"

        self.authenticate()

    def authenticate(self):
        """
        Sends your credentials in plaintext and allows you to access SchoolSoft REST API
        """

        base_url = f"https://sms.schoolsoft.se/{school}"
        login_url = f"{base_url}/jsp/Login.jsp"
        saml_login_url = f"{base_url}/samlLogin.jsp"

        self.session.get(login_url)
        saml_login_response = self.session.get(saml_login_url, allow_redirects=False)
        location_url = saml_login_response.headers.get("Location", None)
        saml_response = self.session.get(location_url, allow_redirects=False)
        return_to_url = saml_response.headers.get("Location", None)

        final_response = self.session.get(return_to_url)
        login_url = final_response.url
        login_data = {
            "fc": "",
            "idpPlugin": "true",
            "username": self.username,
            "password": self.password,
        }

        final_login_response = self.session.post(
            login_url, data=login_data, allow_redirects=False
        )

        saml_final_url = final_login_response.headers.get("Location", None)
        saml_final_response = self.session.get(saml_final_url)

        soup = BeautifulSoup(saml_final_response.text, "html.parser")
        _saml_response = soup.find("input", {"name": "SAMLResponse"})["value"]
        _relay_state = soup.find("input", {"name": "RelayState"})["value"]

        post_data = {
            "SAMLResponse": _saml_response,
            "RelayState": _relay_state,
        }

        self.session.post(
            "https://sms.schoolsoft.se/Shibboleth.sso/SAML2/POST",
            data=post_data,
            allow_redirects=False,
        )

        self.session.get(saml_login_url)

    # General Endpoints
    def get_session(self) -> dict:
        return self.session.get(f"{self.rest_url}/session").json()

    def get_parameters(self) -> dict:
        return self.session.get(f"{self.rest_url}/parameters").json()

    # Calendar endpoints
    def get_calendar_student_lessons(self) -> dict:
        return self.session.get(f"{self.rest_url}/calendar/student/lessons").json()

    def get_calendar_theme(self) -> dict:
        return self.session.get(f"{self.rest_url}/calendar/theme").json()

    def get_calendar_student_settings(self) -> dict:
        return self.session.get(f"{self.rest_url}/calendar/student/settings").json()

    def put_calendar_student_settings(self, data) -> dict:
        return self.session.put(
            f"{self.rest_url}/calendar/student/settings", data=data
        ).json()

    def get_calendar_student_stores(self) -> dict:
        return self.session.get(f"{self.rest_url}/calendar/student/stores").json()

    def get_calendar_student_resource(self) -> dict:
        return self.session.get(f"{self.rest_url}/calendar/student/resource").json()

    def get_calendar_student_language(self) -> dict:
        return self.session.get(f"{self.rest_url}/calendar/student/language").json()

    def get_calendar_student_news(self) -> dict:
        return self.session.get(f"{self.rest_url}/calendar/student/news").json()

    def get_calendar_student_version(self) -> dict:
        return self.session.get(f"{self.rest_url}/calendar/student/version").json()

    def get_calendar_student_plannings(self) -> dict:
        return self.session.get(f"{self.rest_url}/calendar/student/plannings").json()

    def get_calendar_student_time_bookings(self) -> dict:
        return self.session.get(
            f"{self.rest_url}/calendar/student/time_bookings"
        ).json()

    # Student endpoints
    def get_student_header_student(self) -> dict:
        return self.session.get(f"{self.rest_url}/student/header/student").json()

    def get_student_header_schools(self) -> dict:
        return self.session.get(f"{self.rest_url}/student/header/schools").json()

    def get_student_header_skolon(self) -> dict:
        return self.session.get(f"{self.rest_url}/student/header/skolon").json()

    def get_student_logo(self) -> dict:
        return self.session.get(f"{self.rest_url}/student/logo").json()

    def get_student_sidebar_sectiongroups(self) -> dict:
        return self.session.get(f"{self.rest_url}/student/sidebar/sectiongroups").json()

    def get_student_sidebar_autocompleteoptions(self) -> dict:
        return self.session.get(
            f"{self.rest_url}/student/sidebar/autocompleteoptions"
        ).json()

    # Lunch menu endpoints
    def get_lunch_menu(self, week: str) -> dict:
        return self.session.get(f"{self.rest_url}/lunchmenu/week/{str(week)}").json()

    # Localization endpoints
    def get_localization_context(self) -> dict:
        return self.session.get(f"{self.rest_url}/localization/context").json()

    # This function should allow for as many as possible key_texts since the api can do that as well
    def get_localization_text(self, key_text: str) -> dict:
        return self.session.get(
            f"{self.rest_url}/localization/texts/?keyText={key_text}"
        ).json()

    # Get previous, current, and next lesson functions
    def get_previous_lesson(self, pretty_print: bool = False) -> dict | str:
        """
        Returns authenticated user's previous lesson as a dict, but can also return
        pretty printed str with minimal information
        """

        now = datetime.now()
        lessons = self.get_calendar_student_lessons()
        lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        previous_lesson = None

        for lesson in lessons:
            end_date = datetime.fromisoformat(lesson["endDate"])
            if end_date < now:
                previous_lesson = lesson
            else:
                break

        if pretty_print:
            return f"{previous_lesson["name"]} in room {previous_lesson["room"]} with {previous_lesson["teacher"]} at {previous_lesson["startDate"]} to {previous_lesson["endDate"]}"
        else:
            return previous_lesson

    def get_current_lesson(self, pretty_print: bool = False) -> dict | str:
        now = datetime.now()
        lessons = self.get_calendar_student_lessons()
        for lesson in lessons:
            start_date = datetime.fromisoformat(lesson["startDate"])
            end_date = datetime.fromisoformat(lesson["endDate"])
            if start_date <= now <= end_date:
                if pretty_print:
                    return f"{lesson["name"]} in room {lesson["room"]} with {lesson["teacher"]} at {lesson["startDate"]} to {lesson["endDate"]}"
                else:
                    return lesson
        return None

    def get_next_lesson(self, pretty_print: bool = False) -> dict | str:
        now = datetime.now()
        lessons = self.get_calendar_student_lessons()
        lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        for lesson in lessons:
            start_date = datetime.fromisoformat(lesson["startDate"])
            if start_date > now:
                if pretty_print:
                    return f"{lesson["name"]} in room {lesson["room"]} with {lesson["teacher"]} at {lesson["startDate"]} to {lesson["endDate"]}"
                else:
                    return lesson
        return None

    def get_todays_lessons(self) -> list:
        now = datetime.now().date()
        lessons = self.get_calendar_student_lessons()
        todays_lessons = [
            lesson
            for lesson in lessons
            if datetime.fromisoformat(lesson["startDate"]).date() == now
        ]
        todays_lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        return todays_lessons

    def get_lesson_status(self, lesson_id: int, week: int) -> dict:
        lessons = self.get_calendar_student_lessons()
        lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        for lesson in lessons:
            if "studentLessonStatus" in lesson:
                student_status = lesson["studentLessonStatus"]
                if (
                    student_status["week"] == week
                    and student_status["lessonId"] == lesson_id
                ):
                    return lesson
        return None

    def get_lessons_by_id(self, lesson_id: int) -> list[dict]:
        lessons = self.get_calendar_student_lessons()
        lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        results = []
        for lesson in lessons:
            if lesson["eventId"] == lesson_id:
                results.append(lesson)
        return results

    def get_lessons_by_name(self, lesson_name: str) -> list[dict]:
        lessons = self.get_calendar_student_lessons()
        lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        results = []
        for lesson in lessons:
            if lesson_name in lesson["name"]:
                results.append(lesson)
        return results

    def get_event_id_by_name(self, lesson_name: str) -> list[dict]:
        lessons = self.get_calendar_student_lessons()
        lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        results = []
        for lesson in lessons:
            if lesson_name in lesson["name"]:
                if lesson["eventId"] not in results:
                    results.append(lesson["eventId"])
        return results


if __name__ == "__main__":
    load_dotenv()

    username = os.getenv("USER")
    password = os.getenv("PASS")
    school = os.getenv("SCHOOL")

    api = Api(username, password, school)
