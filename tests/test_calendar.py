import pytest

from schoolsoft import Calendar
from schoolsoft.models import (
    CalendarSettings,
    Grade,
    Lesson,
    Room,
    Store,
    Teacher,
    Theme,
)


@pytest.fixture
def calendar(mocker):
    api_mock = mocker.Mock()
    return Calendar(api_mock)


def test_get_lessons(calendar):
    mock_response = [
        {
            "eventId": 379415,
            "name": "Lunch",
            "description": "Lunch",
            "startDate": "2025-01-13T12:40",
            "endDate": "2025-01-13T13:00",
            "allDay": False,
            "eventColor": "",
            "editable": False,
            "room": "",
            "teachingGroup": "Grade 1",
            "teacher": "",
            "dayId": 0,
            "status": -1,
            "category": "lesson",
            "roomBooking": False,
        },
        {
            "eventId": 379415,
            "name": "Lunch",
            "description": "Lunch",
            "startDate": "2025-01-20T12:40",
            "endDate": "2025-01-20T13:00",
            "allDay": False,
            "eventColor": "",
            "editable": False,
            "room": "",
            "teachingGroup": "Grade 1",
            "teacher": "",
            "dayId": 0,
            "status": -1,
            "category": "lesson",
            "roomBooking": False,
        },
    ]

    calendar.api._request.return_value = mock_response
    result = calendar.get_lessons()

    assert isinstance(result, list)

    for index, lesson in enumerate(result):
        assert isinstance(lesson, Lesson)
        assert lesson.day_id == mock_response[index]["dayId"]
        assert lesson.event_id == mock_response[index]["eventId"]


def test_get_theme(calendar):
    mock_response = {"theme": "light"}
    calendar.api._request.return_value = mock_response
    result = calendar.get_theme()

    assert isinstance(result, Theme)
    assert result.theme == "light"


def test_get_settings(calendar):
    mock_response = {
        "userType": "STUDENT",
        "userId": 12345,
        "app": False,
        "mode": "week",
        "categories": [
            "lesson",
            "calendarEvent",
            "privateEvent",
            "schoolCalendarEvent",
            "timeBooking",
            "planning",
            "test",
        ],
        "showWeekends": False,
        "agendaRange": "month",
    }
    calendar.api._request.return_value = mock_response
    result = calendar.get_settings()

    assert isinstance(result, CalendarSettings)
    assert result.user_type == "STUDENT"
    assert result.user_id == 12345


def test_update_settings(calendar):
    mock_response = {
        "userType": "STUDENT",
        "userId": 12345,
        "app": False,
        "mode": "week",
        "categories": [
            "lesson",
            "calendarEvent",
            "privateEvent",
            "schoolCalendarEvent",
            "timeBooking",
            "planning",
            "test",
        ],
        "showWeekends": False,
        "agendaRange": "month",
    }

    calendar.api._request.return_value = mock_response
    result = calendar.get_settings()

    assert isinstance(result, CalendarSettings)
    assert result.user_type == "STUDENT"
    assert result.user_id == 12345

    result.mode = "month"
    result.show_weekends = True

    mock_update_response = result.to_dict(result)
    calendar.api._request.return_value = mock_update_response

    updated_result = calendar.update_settings(result)

    assert isinstance(updated_result, CalendarSettings)
    assert updated_result.mode == "month"
    assert updated_result.show_weekends is True


def test_get_store(calendar):
    mock_response = {
        "scheduleTypes": [
            {"value": "currentStudent", "text": "Visa allt", "placeholder": ""},
            {"value": "scheduleOnly", "text": "Endast schema", "placeholder": ""},
            {"value": "class", "text": "Klass", "placeholder": "Välj klass..."},
            {"value": "room", "text": "Sal", "placeholder": "Välj sal..."},
            {"value": "teacher", "text": "Personal", "placeholder": "Välj personal..."},
        ],
        "teacherItems": [
            {"value": 1234, "text": "John Doe"},
            {"value": 4321, "text": "Jane Doe"},
        ],
        "classItems": [
            {"value": 12345, "text": "Grade 1"},
            {"value": 23456, "text": "Grade 2"},
            {"value": 34567, "text": "Grade 3"},
        ],
        "roomItems": [
            {"value": 1000, "text": "100"},
            {"value": 1001, "text": "101"},
            {"value": 1002, "text": "102"},
        ],
        "studentItems": [],
    }
    calendar.api._request.return_value = mock_response
    result = calendar.get_store()

    assert isinstance(result, Store)

    assert isinstance(result.grades, list)
    for grade in result.grades:
        assert isinstance(grade, Grade)

    assert isinstance(result.teachers, list)
    for teacher in result.teachers:
        assert isinstance(teacher, Teacher)

    assert isinstance(result.rooms, list)
    for room in result.rooms:
        assert isinstance(room, Room)


def test_get_language(calendar):
    mock_response = {"language": "SV"}
    calendar.api._request.return_value = mock_response
    result = calendar.get_language()

    assert result.language == "SV"


# Useless to test to be honest
def test_get_news(calendar):
    mock_response = []
    calendar.api._request.return_value = mock_response
    result = calendar.get_news()

    assert result == mock_response


def test_get_resource(calendar):
    mock_response = []
    calendar.api._request.return_value = mock_response
    result = calendar.get_resource()

    assert result == mock_response


def test_get_version(calendar):
    mock_response = None
    calendar.api._request.return_value = mock_response
    result = calendar.get_version()

    assert result == mock_response


def test_get_plannings(calendar):
    mock_response = []
    calendar.api._request.return_value = mock_response
    result = calendar.get_plannings()

    assert result == mock_response


def test_get_time_bookings(calendar):
    mock_response = []
    calendar.api._request.return_value = mock_response
    result = calendar.get_time_bookings()

    assert result == mock_response
