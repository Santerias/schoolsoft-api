from dataclasses import dataclass
from datetime import datetime


@dataclass
class StudentLessonStatus:
    lessonId: int
    status: int
    statusType: int
    week: int
    comment: str | None
    absence: int
    name: str
    reason: str | None


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
    studentLessonStatus: StudentLessonStatus | None = None

    @classmethod
    def from_dict(cls, data: dict) -> "Lesson":
        """Creates a Lesson instance from a dictionary."""
        data["startDate"] = datetime.fromisoformat(data["startDate"])
        data["endDate"] = datetime.fromisoformat(data["endDate"])

        if "studentLessonStatus" in data:
            data["studentLessonStatus"] = StudentLessonStatus(
                **data["studentLessonStatus"]
            )

        return cls(**data)
