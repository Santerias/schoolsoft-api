import requests
from .exceptions import ApiException, InvalidCredentials
from bs4 import BeautifulSoup


class Auth:
    def __init__(self, api):
        self.api = api

    def authenticate(self):
        """
        Sends your credentials in plaintext and allows you to access SchoolSoft REST API
        """

        base_url = f"https://sms.schoolsoft.se/{self.api.school}"
        login_url = f"{base_url}/jsp/Login.jsp"
        saml_login_url = f"{base_url}/samlLogin.jsp"

        try:
            self.api.session.get(login_url)
            saml_login_response = self.api.session.get(
                saml_login_url, allow_redirects=False
            )
            location_url = saml_login_response.headers.get("Location", None)
            saml_response = self.api.session.get(location_url, allow_redirects=False)
            return_to_url = saml_response.headers.get("Location", None)

            final_response = self.api.session.get(return_to_url)
            login_url = final_response.url
            login_data = {
                "fc": "",
                "idpPlugin": "true",
                "username": self.api.username,
                "password": self.api.password,
            }

            final_login_response = self.api.session.post(
                login_url, data=login_data, allow_redirects=False
            )

            final_login_soup = BeautifulSoup(final_login_response.text, "html.parser")
            if final_login_soup.find("font", attrs={"weight": 500}) is not None:
                raise InvalidCredentials("Invalid credentials provided")

            saml_final_url = final_login_response.headers.get("Location", None)
            saml_final_response = self.api.session.get(saml_final_url)

            soup = BeautifulSoup(saml_final_response.text, "html.parser")
            _saml_response = soup.find("input", {"name": "SAMLResponse"})["value"]
            _relay_state = soup.find("input", {"name": "RelayState"})["value"]

            post_data = {
                "SAMLResponse": _saml_response,
                "RelayState": _relay_state,
            }

            self.api.session.post(
                "https://sms.schoolsoft.se/Shibboleth.sso/SAML2/POST",
                data=post_data,
                allow_redirects=False,
            )

            self.api.session.get(saml_login_url)
        except requests.exceptions.RequestException as e:
            raise ApiException("Authentication failed") from e
