import pytest
import schoolsoft
from os import getenv
from dotenv import load_dotenv

load_dotenv()

username = getenv("USER")
password = getenv("PASS")
school = getenv("SCHOOL")


def test_invalid_credentials():
    with pytest.raises(schoolsoft.exceptions.InvalidCredentials):
        schoolsoft.Api("aksodkaopsdkpo", "aksdpkoasdkpoa", "nti")


def test_valid_credentials():
    schoolsoft.Api(username, password, school)
