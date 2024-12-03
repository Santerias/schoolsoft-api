#!/usr/bin/env python3
import requests
import json
import time
import datetime
import os
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


if __name__ == "__main__":
    load_dotenv()

    username = os.getenv("USER")
    password = os.getenv("PASS")
    school = os.getenv("SCHOOL")

    api = Api(username, password, school)
    print(api.get_session())