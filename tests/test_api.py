import schoolsoft
import pytest
from dotenv import load_dotenv
from os import getenv

load_dotenv()

username = getenv("USER")
password = getenv("PASS")
school = getenv("SCHOOL")


@pytest.fixture(scope="module")
def authenticated_api():
    api = schoolsoft.Api(username, password, school)
    api.authenticate()
    return api


def test_valid_credentials(authenticated_api):
    assert authenticated_api.is_authenticated()


def test_invalid_credentials():
    api = schoolsoft.Api("abc", "abc", "nti")
    with pytest.raises(schoolsoft.InvalidCredentials):
        api.authenticate()


def test_invalid_credentials_and_school():
    api = schoolsoft.Api("abc", "abc", "abc")
    with pytest.raises(schoolsoft.ApiException):
        api.authenticate()


def test_get_session(authenticated_api):
    authenticated_api.get_session()
