from datetime import datetime, timedelta

import pytest

from schoolsoft import Calendar, Student, Theme, utils
from schoolsoft.models import Lesson


@pytest.fixture
def mock_lessons_data():
    current_time = datetime.now()
    return [
        {
            # next lesson
            "eventId": 123456,
            "name": "Activity day",
            "description": "Actitvity day for all students",
            "startDate": (current_time + timedelta(days=10)).isoformat(),
            "endDate": (current_time + timedelta(days=10, hours=1)).isoformat(),
            "allDay": False,
            "eventColor": "",
            "editable": False,
            "room": "",
            "teachingGroup": "Grade 1,Grade 2,Grade 3",
            "teacher": "John Doe,Jane Doe,John Smith",
            "dayId": 2,
            "status": 2,
            "studentLessonStatus": {
                "lessonId": 123456,
                "status": 9,
                "statusType": 4,
                "week": 36,
                "comment": "",
                "absence": 0,
                "name": "Frånvarande",
                "reason": "Föranmäld",
            },
            "category": "lesson",
            "roomBooking": False,
        },
        {
            # previous lesson
            "eventId": 654321,
            "name": "End of school",
            "description": "End of school before holidays",
            "startDate": (current_time - timedelta(days=10, hours=1)).isoformat(),
            "endDate": (current_time - timedelta(days=10)).isoformat(),
            "allDay": False,
            "eventColor": "",
            "editable": False,
            "room": "",
            "teachingGroup": "Grade 1,Grade 2,Grade 3",
            "teacher": "John Doe,Jane Doe,John Smith",
            "dayId": 2,
            "status": -1,
            "category": "lesson",
            "roomBooking": False,
        },
        {
            # current lesson
            "eventId": 321123,
            "name": "Math",
            "description": "Math",
            "startDate": current_time.isoformat(),
            "endDate": (current_time + timedelta(hours=1, minutes=30)).isoformat(),
            "allDay": False,
            "eventColor": "",
            "editable": False,
            "room": "214",
            "teachingGroup": "Grade 1",
            "teacher": "John Doe",
            "dayId": 2,
            "status": -1,
            "category": "lesson",
            "roomBooking": False,
        },
    ]


@pytest.fixture
def calendar(mocker):
    api_mock = mocker.Mock()
    return Calendar(api_mock)


@pytest.fixture
def student(mocker):
    api_mock = mocker.Mock()
    return Student(api_mock)


def test_is_dark(calendar):
    mock_response = {"theme": "dark"}

    calendar.api._request.return_value = mock_response
    result = utils.is_dark(calendar.get_theme())

    assert isinstance(calendar.get_theme(), Theme)
    assert result is True


def test_is_light(calendar):
    mock_response = {"theme": "light"}

    calendar.api._request.return_value = mock_response
    result = utils.is_light(calendar.get_theme())

    assert isinstance(calendar.get_theme(), Theme)
    assert result is True


# could use xfail but this is not locked to a specific version
# or failing because of different platforms e.g. darwin, win32
def test_is_not_valid_theme(calendar):
    mock_response = {"theme": "blue"}

    calendar.api._request.return_value = mock_response
    dark = utils.is_dark(calendar.get_theme())
    light = utils.is_light(calendar.get_theme())

    assert dark is False
    assert light is False


def test_get_previous_lesson(calendar, mock_lessons_data):
    calendar.api._request.return_value = mock_lessons_data
    lessons = calendar.get_lessons()
    result = utils.get_previous_lesson(lessons)

    assert isinstance(lessons, list)
    assert isinstance(result, Lesson)


def test_get_current_lesson(calendar, mock_lessons_data):
    calendar.api._request.return_value = mock_lessons_data
    lessons = calendar.get_lessons()
    result = utils.get_current_lesson(lessons)

    assert isinstance(lessons, list)
    assert isinstance(result, Lesson)


def test_get_next_lesson(calendar, mock_lessons_data):
    calendar.api._request.return_value = mock_lessons_data
    lessons = calendar.get_lessons()
    result = utils.get_next_lesson(lessons)

    assert isinstance(lessons, list)
    assert isinstance(result, Lesson)


def test_get_todays_lessons(calendar, mock_lessons_data):
    calendar.api._request.return_value = mock_lessons_data
    lessons = calendar.get_lessons()
    result = utils.get_todays_lessons(lessons)

    assert isinstance(lessons, list)
    assert isinstance(result, list)

    for lesson in result:
        assert isinstance(lesson, Lesson)


def test_get_lessons_by_id(calendar, mock_lessons_data):
    calendar.api._request.return_value = mock_lessons_data
    lessons = calendar.get_lessons()
    result = utils.get_lessons_by_id(lessons, 123456)

    assert isinstance(lessons, list)
    assert isinstance(result, list)

    for lesson in result:
        assert isinstance(lesson, Lesson)


def test_get_lessons_by_name(calendar, mock_lessons_data):
    calendar.api._request.return_value = mock_lessons_data
    lessons = calendar.get_lessons()
    result = utils.get_lessons_by_name(lessons, "Math")

    assert isinstance(lessons, list)
    assert isinstance(result, list)

    for lesson in result:
        assert isinstance(lesson, Lesson)


def test_get_weekly_schedule(calendar, mock_lessons_data):
    calendar.api._request.return_value = mock_lessons_data
    lessons = calendar.get_lessons()

    now = datetime.now()
    week_number = now.isocalendar()[1]

    result_current = utils.get_weekly_schedule(lessons)
    assert len(result_current) == 7
    assert all(isinstance(day, list) for day in result_current)

    result_specific = utils.get_weekly_schedule(lessons, week_number)
    assert len(result_specific) == 7

    for day_index, day_lessons in enumerate(result_specific):
        for lesson in day_lessons:
            assert lesson.start_date.weekday() == day_index

    for day_lessons in result_specific:
        for lesson in day_lessons:
            assert (
                lesson.start_date.isocalendar()[1] == datetime.now().isocalendar().week
            )
