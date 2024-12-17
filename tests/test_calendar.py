import schoolsoft
from os import getenv
from dotenv import load_dotenv

load_dotenv()

username = getenv("USER")
password = getenv("PASS")
school = getenv("SCHOOL")

api = schoolsoft.Api(username, password, school)


def test_fetch_student_lessons():
    lessons = api.calendar.fetch_student_lessons()
    for lesson in lessons:
        print(lesson.name)
