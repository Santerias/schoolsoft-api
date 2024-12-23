import re
from dataclasses import dataclass
from datetime import datetime


def camel_to_snake(camel_case_str: str) -> str:
    """convert camelCase to snake_case"""
    return re.sub(r"([a-z])([A-Z])", r"\1_\2", camel_case_str).lower()


def snake_to_camel(snake_case_str: str) -> str:
    """convert snake_case to camelCase"""
    words = snake_case_str.split("_")
    return words[0] + "".join(word.capitalize() for word in words[1:])


def map_day_id_to_name(day_id: int) -> str:
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


@dataclass
class StudentLessonStatus:
    lesson_id: int
    status: int
    status_type: int
    week: int
    comment: str | None
    absence: int
    name: str
    reason: str | None

    @classmethod
    def from_dict(cls, data: dict) -> "StudentLessonStatus":
        """Creates a StudentLessonStatus instance from a dictionary."""
        converted_data = {camel_to_snake(key): value for key, value in data.items()}
        return cls(**converted_data)


@dataclass
class Lesson:
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
        if self.day is None:
            self.day = map_day_id_to_name(self.day_id)

    @classmethod
    def from_dict(cls, data: dict) -> "Lesson":
        """Creates a Lesson instance from a dictionary."""
        converted_data = {camel_to_snake(key): value for key, value in data.items()}

        converted_data["start_date"] = datetime.fromisoformat(
            converted_data["start_date"]
        )
        converted_data["end_date"] = datetime.fromisoformat(converted_data["end_date"])

        if "day" not in converted_data:
            converted_data["day"] = map_day_id_to_name(converted_data["day_id"])

        if "student_lesson_status" in converted_data:
            converted_data["student_lesson_status"] = StudentLessonStatus.from_dict(
                converted_data["student_lesson_status"]
            )

        return cls(**converted_data)


@dataclass
class Grade:
    value: int
    name: str

    @classmethod
    def from_dict(cls, data: dict) -> "Grade":
        """Creates a Class instance from a dictionary."""
        return cls(value=data["value"], name=" ".join(data["text"].split()))


@dataclass
class Room:
    value: int
    name: str

    @classmethod
    def from_dict(cls, data: dict) -> "Room":
        """Creates a Room instance from a dictionary."""
        return cls(value=data["value"], name=" ".join(data["text"].split()))


@dataclass
class Teacher:
    value: int
    name: str

    @classmethod
    def from_dict(cls, data: dict) -> "Teacher":
        """Creates a Teacher instance from a dictionary."""
        return cls(value=data["value"], name=" ".join(data["text"].split()))


@dataclass
class Store:
    teachers: list[Teacher]
    grades: list[Grade]
    rooms: list[Room]

    @classmethod
    def from_dict(cls, data: dict) -> "Store":
        """Creates a Store instance from a dictionary."""
        teachers = [Teacher.from_dict(item) for item in data["teacherItems"]]
        grades = [Grade.from_dict(item) for item in data["classItems"]]
        rooms = [Room.from_dict(item) for item in data["roomItems"]]

        return cls(teachers=teachers, grades=grades, rooms=rooms)


@dataclass
class Theme:
    theme: str

    @classmethod
    def from_dict(cls, data: dict) -> "Theme":
        return cls(**data)


@dataclass
class CalendarSettings:
    user_type: str
    user_id: int
    app: bool
    mode: str
    categories: list
    show_weekends: bool
    agenda_range: str

    @classmethod
    def from_dict(cls, data: dict) -> "CalendarSettings":
        """Creates a Student instance from a dictionary."""
        converted_data = {camel_to_snake(key): value for key, value in data.items()}
        return cls(**converted_data)

    @classmethod
    def to_dict(cls, settings: "CalendarSettings") -> dict:
        return {snake_to_camel(key): value for key, value in vars(settings).items()}


@dataclass
class Language:
    language: str

    @classmethod
    def from_dict(cls, data: dict) -> "Language":
        return cls(**data)


@dataclass
class Dish:
    dishType: str
    dish: str

    @classmethod
    def from_dict(cls, data: dict) -> "Dish":
        return cls(**data)


@dataclass
class DayMenu:
    dayId: int
    dishes: list[Dish]

    @classmethod
    def from_dict(cls, data: dict) -> "DayMenu":
        return cls(
            dayId=data["dayId"],
            dishes=[Dish.from_dict(dish) for dish in data["dishes"]],
        )


@dataclass
class Lunch:
    menu: list[DayMenu]

    @classmethod
    def from_dict(cls, data: list) -> "Lunch":
        return cls(menu=[DayMenu.from_dict(day) for day in data])


@dataclass
class School:
    org_id: int
    name: str
    grade: str

    @classmethod
    def from_dict(cls, data: dict) -> "School":
        # could use more dynamic way to convert keys
        return cls(
            org_id=data["orgId"], name=data["schoolName"], grade=data["className"]
        )


# TODO: Change to Student
@dataclass
class User:
    first_name: str
    last_name: str
    profile_picture: str
    unread_messages: int
    active: bool
    # schools: list[School]

    @classmethod
    def from_dict(cls, data: list) -> "User":
        converted_data = {camel_to_snake(key): value for key, value in data.items()}
        return cls(
            first_name=converted_data["first_name"],
            last_name=converted_data["last_name"],
            profile_picture=converted_data["picture_url"],
            unread_messages=converted_data["unread_messages"],
            active=converted_data["active"],
        )
