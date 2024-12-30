from datetime import datetime

from pydantic import ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic.dataclasses import dataclass


def _map_day_id_to_name(day_id: int) -> str:
    """Maps the day_id to a day to add to classes

    Args:
        day_id (int): 0-4 index where 0 is Monday and 4 is Friday

    Returns:
        str: Maps day_id to a str representing a day of the week (e.g. Monday)
    """
    days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    return days[day_id % 7]


@dataclass(config=ConfigDict(alias_generator=to_camel))
class StudentLessonStatus:
    """StudentLessonStatus

    Args:
        lesson_id (int): The same as event_id
        status (int): Random integer that get's returned from REST API, (don't know what it does)
        status_type (int): A value ranging between 1-4
        week (int): What week number the lesson took place on
        comment (str or None): Comment usually added with absence
        absence (int): Absence in minutes
        name (str): Name of status if you were late or on time and so on.
        reason (str or None): The reason for why you were gone or on place, usually empty if you didn't report sick/absence
    """

    lesson_id: int
    status: int
    status_type: int
    week: int
    comment: str | None
    absence: int
    name: str
    reason: str | None


@dataclass(config=ConfigDict(alias_generator=to_camel))
class Lesson:
    """Lesson

    Args:
        event_id (int): ID of the lesson
        name (str): Name of the lesson
        description (str or None): Description of the lesson, usually the same as name or empty
        start_date (datetime.datetime): Datetime object representing start date including time when lesson starts
        end_date (datetime.datetime): Datetime object representing end date including time when lesson ends
        all_day (bool or None): Determines if lesson is all day or not
        event_color (str or None): Some lessons have event_color which determines it's color on the calendar
        editable (boolean): Determines if the lesson is editable in the calendar, usually always False
        room (str or None): Room the lesson takes place in, could also be None (e.g. if you have Lunch in your schedule and there is no room registered for that)
        teaching_group (str): Grade the lesson is meant for
        teacher (str or None): Teacher(s) that holds the lesson, seperated with `,`
        day_id (int): Index indicating day the lesson takes place on, index starting from 0, where 0 is Monday
        status (int): If value equals `-1` indicates there is no StudentLessonStatus, status `2` indicates there is.
        category (str): Usually always `"lesson"` but can also be other categories
        room_booking (bool): Boolean deciding if you can book the room or not
        day (str or None): Day of which the lesson takes place on
        student_lesson_status (StudentLessonStatus or None): Refer to StudentLessonStatus class for reference.
    """

    event_id: int
    name: str
    description: str | None
    start_date: datetime
    end_date: datetime
    all_day: bool | None
    event_color: str | None
    editable: bool
    room: str | None
    teaching_group: str
    teacher: str | None
    day_id: int
    status: int
    category: str
    room_booking: bool
    day: str | None = None
    student_lesson_status: StudentLessonStatus | None = None

    def __post_init__(self):
        """Sets day to a str for convenience instead of having to manually convert day_id to a str representing a day of the week

        Args:
            day (str or None): Sets `day` to a str representing the day with help of `day_id` attribute in Lesson class
        """
        if self.day is None:
            self.day = _map_day_id_to_name(self.day_id)


@dataclass
class Grade:
    """Grade

    Args:
        value (int): The ID of the Grade that can be used later for getting the schedule for a specific grade
        name (str): The name of the Grade
    """

    value: int
    name: str = Field(alias="text")


@dataclass
class Room:
    """Room

    Args:
        value (int): The ID of the Room
        name (str): The name of the Room
    """

    value: int
    name: str = Field(alias="text")


@dataclass
class Teacher:
    """Teacher

    Args:
        value (int): The ID of the teacher, which can be used for getting a teachers schedule
        name (str): The name of the teacher
    """

    value: int
    name: str = Field(alias="text")


@dataclass(config=ConfigDict(alias_generator=to_camel))
class Store:
    """Store that contains all values for teachers, grades, and rooms for easier access
    that you could use later to get e.g. someones schedule/lessons

    Args:
        teachers (list[Teacher]): List of teachers
        grades (list[Grade]): List of grades
        rooms (list[Room]): List of rooms
    """

    teachers: list[Teacher] = Field(alias="teacherItems")
    grades: list[Grade] = Field(alias="classItems")
    rooms: list[Room] = Field(alias="roomItems")


@dataclass
class Theme:
    """Theme object

    Args:
        theme (str): This is either `light` or `dark`
    """

    theme: str


@dataclass(config=ConfigDict(alias_generator=to_camel))
class CalendarSettings:
    """CalendarSettings

    Args:
        user_type (str): Will usually always be `STUDENT`
        user_id (str): Your User ID
        app (bool): True if you're accessing the endpoint via the app, False otherwise
        mode (str): Possible values are: `day`, `week`, `month`
        categories (list): A list with categories you want to filter through and get returned, possible values are: `lesson`, `calendarEvent`, `privateEvent`, `schoolCalendarEvent`, `timeBooking`, `planning`, `test`
        show_weekends (bool): If true it will show if you have any lessons during the weekends
        agenda_range (str): Special calendar viewing mode that you can set to same values as the `mode` attribute
    """

    user_type: str
    user_id: int
    app: bool
    mode: str
    categories: list
    show_weekends: bool
    agenda_range: str


@dataclass
class Language:
    """Language object

    Args:
        language (str): Language currently being used, can be `SV` or `EN`
    """

    language: str


@dataclass(config=ConfigDict(alias_generator=to_camel))
class Dish:
    """Dish

    Args:
        dish_type (str): Usually set to `Dagens Lunch`
        dish (str): The name of the dish being served for lunch
    """

    dish_type: str
    dish: str


@dataclass(config=ConfigDict(alias_generator=to_camel))
class DayMenu:
    """DayMenu

    Args:
        day_id (int): The day the day menu belongs to e.g. 0 means Monday
        dishes (list[Dish]): List of dishes for the day
    """

    day_id: int
    dishes: list[Dish]


@dataclass
class Lunch:
    """Lunch

    Args:
        menu (list[DayMenu]): Lunch menu
    """

    menu: list[DayMenu] = Field(default="")


@dataclass(config=ConfigDict(alias_generator=to_camel))
class School:
    """School

    Args:
        org_id (int): What organization ID the school has
        name (str): Name of the school
        grade (str): What grade you are assigned to
    """

    org_id: int
    name: str = Field(alias="schoolName")
    grade: str = Field(alias="className")


# TODO: Change to Student
@dataclass(config=ConfigDict(alias_generator=to_camel))
class User:
    """User

    Args:
        first_name (str): Students first name
        last_name (str): Students last name
        profile_picture (str): Students profile picture
        unread_messages (int): Number of unread messages
        active (bool): `True` if the account is active otherwise `False`
    """

    first_name: str
    last_name: str
    unread_messages: int
    active: bool
    profile_picture: str = Field(alias="pictureURL")
    # schools: list[School]
