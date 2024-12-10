#!/usr/bin/env python3
import requests
import json
import time
import os
from datetime import datetime
from sys import exit
from urllib.parse import urlparse, parse_qs, quote
from dotenv import load_dotenv

class Api:
    def __init__(self, username, password, school):
        self.username = username
        self.password = password
        self.school = school
        self.session = requests.Session()
        self.base_url = f"https://sms.schoolsoft.se/{self.school}"
        self.login_url = f"{self.base_url}/jsp/Login.jsp"
        self.saml_login_url = f"{self.base_url}/samlLogin.jsp"
        self.rest_url = f"{self.base_url}/rest-api"

        self.authenticate()

    def write_json(self, file, data):
        with open(file, "w") as f:
            json.dump(data, f, indent=4)

    def authenticate(self):
        """
        Authenticates using Schoolsoft SAML SSO and saves cookies for future use until cookies expire
        """

        login_response = self.session.get(self.login_url)
        
        jsessionid = self.session.cookies.get("JSESSIONID", None)

        saml_login_response = self.session.get(
            self.saml_login_url, allow_redirects=False
        )

        location_url = saml_login_response.headers.get("Location", None)
        
        if location_url:
            parsed_url = urlparse(location_url)
            query_params = parse_qs(parsed_url.query)
            saml_request = query_params.get("SAMLRequest", [None])[0]
            relay_state = query_params.get("RelayState", [None])[0]

            if relay_state and not relay_state.startswith("cookie:"):
                relay_state = f"cookie:{relay_state}"
        else:
            print("Something went wrong.")
            exit()
        
        saml_request_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?SAMLRequest={quote(saml_request)}&RelayState={quote(relay_state)}"
        saml_response = self.session.get(saml_request_url, allow_redirects=False)
        simple_saml_session_id = self.session.cookies.get("SimpleSAMLSessionID")
        
        return_to_url = saml_response.headers.get("Location", None)

        if return_to_url:
            sessionid = parse_qs(urlparse(return_to_url).query).get("sessionid", [None])[0]

            if sessionid:
                final_url = f"{return_to_url}&sessionid={sessionid}"
            else:
                print("Something went wrong.")
                exit()
        else:
            print("Something went wrong.")
            exit()
        
        final_response = self.session.get(final_url)
        login_url = final_response.url
        login_data = {
            "fc": "",
            "idpPlugin": "true",
            "username": self.username,
            "password": self.password,
        }

        self.session.cookies.set("PHPSESSID", sessionid)
        
        request_headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": f"https://login.grandid.com/?sessionid={sessionid}&ReturnTo={quote(return_to_url)}",
        }

        final_login_response = self.session.post(login_url, data=login_data, headers=request_headers, allow_redirects=False)

        if final_login_response.status_code != 302:
            print("Something went wrong.")
            exit()

        saml_final_url = final_login_response.headers.get("Location", None)
        self.session.cookies.set("SimpleSAMLSessionID", simple_saml_session_id)
        saml_final_response = self.session.get(saml_final_url)

        simple_saml_auth_token = self.session.cookies.get("SimpleSAMLAuthToken")

        from bs4 import BeautifulSoup

        soup = BeautifulSoup(saml_final_response.text, "html.parser")
        _saml_response = soup.find("input", {"name": "SAMLResponse"})["value"]
        _relay_state = soup.find("input", {"name": "RelayState"})["value"]

        post_data = {
            "SAMLResponse": _saml_response,
            "RelayState": _relay_state,
        }

        shibboleth_url = "https://sms.schoolsoft.se/Shibboleth.sso/SAML2/POST"
        shibboleth_response = self.session.post(
            shibboleth_url,
            data=post_data,
            allow_redirects=False,
        )

        cookie_prefixes = ["_shibsession_", "_shibsealed_"]
        extracted_cookies = {}

        for cookie_name, cookie_value in self.session.cookies.items():
            for prefix in cookie_prefixes:
                if cookie_name.startswith(prefix):
                    extracted_cookies[cookie_name] = cookie_value

        self.session.cookies.set(
            "Humany__clientId", "963d69d2-2ed3-3a71-6553-f62fa55d0e02"
        )

        for cookie_name, cookie_value in extracted_cookies.items():
            self.session.cookies.set(cookie_name, cookie_value)

        login = self.session.get(self.saml_login_url, allow_redirects=False)


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

    # Example data:
    # {
    #   "userType": "STUDENT",
    #   "userId": 12345,
    #   "app": false,
    #   "mode": "agenda",
    #   "categories": [
    #       "lesson",
    #       "calendarEvent",
    #       "privateEvent",
    #       "schoolCalendarEvent",
    #       "timeBooking",
    #       "planning",
    #       "test"
    #   ],
    #   "showWeekends": true,
    #   "agendaRange": "day"
    # }
    def put_calendar_student_settings(self, data) -> dict:
        return self.session.put(f"{self.rest_url}/calendar/student/settings", data=data).json()

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
        return self.session.get(f"{self.rest_url}/calendar/student/time_bookings").json()

    def get_calendar_student_stores(self) -> dict:
        return self.session.get(f"{self.rest_url}/calendar/student/stores").json()


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
        return self.session.get(f"{self.rest_url}/student/sidebar/autocompleteoptions").json()


    # Lunch menu endpoints
    def get_lunch_menu(self, week: str) -> dict:
        return self.session.get(f"{self.rest_url}/lunchmenu/week/{str(week)}").json()


    # Localization endpoints
    def get_localization_context(self) -> dict:
        return self.session.get(f"{self.rest_url}/localization/context").json()

    # This function should allow for as many as possible key_texts since the api can do that as well
    def get_localization_text(self, key_text: str) -> dict:
        return self.session.get(f"{self.rest_url}/localization/texts/?keyText={key_text}").json()

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
            start_date = datetime.fromisoformat(lesson["startDate"])
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
            lesson for lesson in lessons
            if datetime.fromisoformat(lesson["startDate"]).date() == now
        ]
        todays_lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        return todays_lessons

    def get_lesson_status(self, lesson_id: int, week: int):
        lessons = self.get_calendar_student_lessons()
        lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        for lesson in lessons:
            if "studentLessonStatus" in lesson:
                student_status = lesson["studentLessonStatus"]
                if student_status["week"] == week and student_status["lessonId"] == lesson_id:
                    return lesson
        return None
    
    def get_lessons_by_id(self, lesson_id: int):
        lessons = self.get_calendar_student_lessons()
        lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        results = []
        for lesson in lessons:
            if lesson["eventId"] == lesson_id:
                results.append(lesson)
        return results

    def get_lessons_by_name(self, lesson_name: str):
        lessons = self.get_calendar_student_lessons()
        lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        results = []
        for lesson in lessons:
            if lesson_name in lesson["name"]:
                results.append(lesson)
        return results
    
    def get_event_id_by_name(self, lesson_name: str):
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