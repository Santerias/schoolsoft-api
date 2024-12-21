#!/usr/bin/env python3

import requests
import logging

from bs4 import BeautifulSoup
from .exceptions import ApiException, InvalidCredentials
from .calendar import Calendar
from .lunch_menu import LunchMenu
from .student import Student
from .localization import Localization


class Api:
    """This class is used to interact with the SchoolSoft API"""

    def __init__(
        self, username: str, password: str, school: str, logger: logging.Logger = None
    ) -> None:
        self.username = username
        self.password = password
        self.school = school
        self.session = requests.Session()
        self.base_url = f"https://sms.schoolsoft.se/{self.school}"
        self.rest_url = f"{self.base_url}/rest-api"
        self.logger = logger or logging.getLogger(__name__)

        self.calendar = Calendar(self)
        self.lunch_menu = LunchMenu(self)
        self.student = Student(self)
        self.localization = Localization(self)

    def authenticate(self) -> None:
        """
        Sends your credentials in plaintext and allows you to access SchoolSoft REST API
        """

        try:
            self.session.get(f"{self.base_url}/jsp/Login.jsp")
            saml_login_response = self.session.get(
                f"{self.base_url}/samlLogin.jsp", allow_redirects=False
            )
            location_url = saml_login_response.headers.get("Location", None)
            saml_response = self.session.get(location_url, allow_redirects=False)
            return_to_url = saml_response.headers.get("Location", None)
            final_response = self.session.get(return_to_url)

            login_data = {
                "fc": "",
                "idpPlugin": "true",
                "username": self.username,
                "password": self.password,
            }

            final_login_response = self.session.post(
                final_response.url, data=login_data, allow_redirects=False
            )
            final_login_soup = BeautifulSoup(final_login_response.text, "html.parser")
            if final_login_soup.find("font", attrs={"weight": 500}) is not None:
                raise InvalidCredentials("Invalid credentials provided")

            saml_final_url = final_login_response.headers.get("Location", None)
            saml_final_response = self.session.get(saml_final_url)

            saml_soup = BeautifulSoup(saml_final_response.text, "html.parser")
            _saml_response = saml_soup.find("input", {"name": "SAMLResponse"})["value"]
            _relay_state = saml_soup.find("input", {"name": "RelayState"})["value"]

            post_data = {
                "SAMLResponse": _saml_response,
                "RelayState": _relay_state,
            }

            self.session.post(
                "https://sms.schoolsoft.se/Shibboleth.sso/SAML2/POST",
                data=post_data,
                allow_redirects=False,
            )
            self.session.get(f"{self.base_url}/samlLogin.jsp")
        except requests.exceptions.RequestException as e:
            raise ApiException("Authentication failed") from e

    def _request(self, method: str, endpoint: str, data=None, json=None) -> dict:
        url = f"{self.rest_url}{endpoint}"
        try:
            if method.lower() == "get":
                response = self.session.get(url)
            elif method.lower() == "put":
                response = self.session.put(url, data=data, json=json)
            else:
                raise ValueError("Unsupported HTTP method")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ApiException(f"Request to {url} failed") from e

    def fetch_session(self) -> dict:
        return self._request("get", "/session")

    def fetch_parameters(self) -> dict:
        return self._request("get", "/parameters")
