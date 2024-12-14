# Specific modules like calendar should be able to return array of Lesson
# Instead of just returning a dict for better OOP

from dataclasses import dataclass
from datetime import datetime
import enum


@dataclass
class Lesson:
    eventId: int
    name: str
    description: str | None
    startDate: datetime
    endDate: datetime
    allDay: bool | None
    eventColor: str | None
    editable: bool
    room: str | None
    teachingGroup: str
    teacher: str | None
    dayId: int
    status: int
    category: str
    roomBooking: bool


class LessonCategory(enum.Enum):
    lesson = "lesson"
    exam = "exam"
