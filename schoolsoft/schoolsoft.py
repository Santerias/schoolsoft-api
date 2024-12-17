#!/usr/bin/env python3

import requests
import logging

from .auth import Auth
from .exceptions import ApiException
from .calendar import Calendar
from .lunch_menu import LunchMenu
from .student import Student
from .localization import Localization
from .utils import Utils


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

        self.authenticate()

        self.calendar = Calendar(self)
        self.lunch_menu = LunchMenu(self)
        self.student = Student(self)
        self.localization = Localization(self)
        self.utils = Utils(self)

    def authenticate(self):
        Auth(self).authenticate()

    def _request(self, method: str, endpoint: str, data=None) -> dict:
        url = f"{self.rest_url}{endpoint}"
        try:
            if method.lower() == "get":
                response = self.session.get(url)
            elif method.lower() == "put":
                response = self.session.put(url, data=data)
            else:
                raise ValueError("Unsupported HTTP method")

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ApiException(f"Request to {url} failed") from e

    # General Endpoints
    def fetch_session(self) -> dict:
        return self.session.get(f"{self.rest_url}/session").json()

    def fetch_parameters(self) -> dict:
        return self.session.get(f"{self.rest_url}/parameters").json()
