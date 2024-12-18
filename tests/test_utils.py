from schoolsoft import Api
from schoolsoft.models import Lesson
from json import load
from os import getenv
from dotenv import load_dotenv
import random

load_dotenv()

username = getenv("USER")
password = getenv("PASS")
school = getenv("SCHOOL")

# api = Api(username, password, school)
# api.authenticate()
# lessons = api.calendar.fetch_student_lessons()

api = Api("abc", "abc", "abc")

with open("lessons_data.json", "r", encoding="utf-8") as f:
    lessons = [Lesson.from_dict(lesson_data) for lesson_data in load(f)]


def test_get_previous_lesson():
    api.utils.get_previous_lesson(lessons)


def test_get_current_lesson():
    api.utils.get_current_lesson(lessons)


def test_get_next_lesson():
    api.utils.get_next_lesson(lessons)


def test_get_todays_lessons():
    api.utils.get_todays_lessons(lessons)


# Will throw an error if StudentLessonStatus doesn't exist.
# def test_get_lesson_status():
#     rand_lesson = random.choice(lessons)
#     print(
#         api.utils.get_lesson_status(
#             lessons, rand_lesson.event_id, rand_lesson.student_lesson_status.week
#         )
#     )


def test_get_lessons_by_id():
    rand_lesson = random.choice(lessons)
    api.utils.get_lessons_by_id(lessons, rand_lesson.event_id)


def test_get_lessons_by_name():
    rand_lesson = random.choice(lessons)
    api.utils.get_lessons_by_name(lessons, rand_lesson.name)


def test_get_weekly_schedule():
    api.utils.get_weekly_schedule(lessons)
