#!/usr/bin/env python3

import logging

import requests
from bs4 import BeautifulSoup

from .calendar import Calendar
from .exceptions import ApiException, InvalidCredentials
from .localization import Localization
from .lunch_menu import LunchMenu
from .student import Student


class Api:
    """Represents a connection to the SchoolSoft REST API.

    Args:
        username (str): Username.
        password (str): Password.
        school (str): School name.
        logger (logging.Logger): Logger to use.

    Example:
        ```python
        from schoolsoft import Api
        api = Api(username, password, school)
        print(api.get_session())
        ```
    """

    def __init__(
        self,
        username: str = "",
        password: str = "",
        school: str = "",
        logger: logging.Logger = None,
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
        """Authenticates the user using the credentials provided when initializing the `Api` class.

        Raises:
            InvalidCredentials: Gets raised if the provided credentials are invalid.
            ApiException: Gets raised if the authentication fails for any other reason.
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

    def _request(
        self, method: str, endpoint: str, data=None, json=None, status=False
    ) -> dict:
        """Private method to make requests to the SchoolSoft REST API.

        Args:
            method (str): HTTP method to use (e.g. `GET`, `POST`).
            endpoint (str): Endpoint to request.
            data (optional): Data to send to the specified endpoint. Default is `None`
            json (optional): JSON data to send to the specified endpoint. Default is `None`
            status (optional, bool): If True, returns entire response instead of just json data. Default is `False`

        Raises:
            ValueError: Gets raised if an unsupported HTTP method is provided.
            ApiException: Gets raised if the request fails.

        Returns:
            dict: Returns the JSON response from the API.
        """
        url = f"{self.rest_url}{endpoint}"
        try:
            if method.lower() == "get":
                response = self.session.get(url)
            elif method.lower() == "put":
                response = self.session.put(url, data=data, json=json)
            else:
                raise ValueError("Unsupported HTTP method")

            response.raise_for_status()

            if status:
                return response

            return response.json()
        except requests.exceptions.RequestException as e:
            raise ApiException(f"Request to {url} failed") from e

    def is_authenticated(self):
        """Checks if the user is authenticated.

        Returns:
            bool: Returns True if the user is authenticated, otherwise False.
        """
        response = self._request("get", "/session", status=True)
        if response.status_code == 401 or response.status_code == 403:
            return False

        return True

    def get_session(self) -> dict:
        """Gets JSON data from the /session endpoint.

        Returns:
            dict: Returns the JSON response from the API.
        """
        return self._request("get", "/session")

    def get_parameters(self) -> dict:
        """Gets JSON data from the /parameters endpoint.

        Returns:
            dict: Returns the JSON response from the API.
        """
        return self._request("get", "/parameters")
