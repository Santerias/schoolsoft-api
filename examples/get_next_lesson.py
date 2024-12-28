from os import getenv

from dotenv import load_dotenv

from schoolsoft import Api
from schoolsoft.utils import get_next_lesson

load_dotenv()

username = getenv("USER")
password = getenv("PASS")
school = getenv("SCHOOL")

api = Api(username, password, school)
api.authenticate()

lessons = api.calendar.get_lessons()
next_lesson = get_next_lesson(lessons)

print(
    f"Name: {next_lesson.name}\nStarts: {next_lesson.start_date}\nEnds: {next_lesson.end_date}"
)
