from os import getenv
from rich.pretty import pprint

from dotenv import load_dotenv

import schoolsoft.utils
from schoolsoft import Api

load_dotenv()

username = getenv("USER")
password = getenv("PASS")
school = getenv("SCHOOL")

api = Api(username, password, school)
api.authenticate()
lessons = api.calendar.get_lessons()

pprint(schoolsoft.utils.get_weekly_schedule(lessons), expand_all=True)
