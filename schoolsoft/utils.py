from datetime import datetime, timedelta

from .models import Lesson, Theme


def is_dark(theme: Theme) -> bool:
    return True if theme.theme.lower() == "dark" else False


def is_light(theme: Theme) -> bool:
    return True if theme.theme.lower() == "light" else False


def get_previous_lesson(lessons: list[Lesson]) -> Lesson | None:
    lessons.sort(key=lambda lesson: lesson.start_date, reverse=True)
    for lesson in lessons:
        if lesson.end_date < datetime.now():
            return lesson

    return None


def get_current_lesson(lessons: list[Lesson]) -> Lesson | None:
    for lesson in lessons:
        if lesson.start_date <= datetime.now() <= lesson.end_date:
            return lesson

    return None


def get_next_lesson(lessons: list[Lesson]) -> Lesson | None:
    lessons.sort(key=lambda lesson: lesson.start_date)
    for lesson in lessons:
        if lesson.start_date > datetime.now():
            return lesson

    return None


def get_todays_lessons(lessons: list[Lesson]) -> list[Lesson]:
    todays_lessons = [
        lesson
        for lesson in lessons
        if lesson.start_date.date() == datetime.now().date()
    ]

    todays_lessons.sort(key=lambda lesson: lesson.start_date)
    return todays_lessons


# def get_lesson_status(
#     lessons: list[Lesson], lesson_id: int, week: int
# ) -> Lesson | None:
#     lessons.sort(key=lambda lesson: lesson.start_date)

#     for lesson in lessons:
#         if lesson.student_lesson_status:
#             if (
#                 lesson.student_lesson_status.week == week
#                 and lesson.student_lesson_status.lesson_id == lesson_id
#             ):
#                 return lesson

#     return None


def get_lessons_by_id(lessons: list[Lesson], lesson_id: int) -> list[Lesson]:
    lessons.sort(key=lambda lesson: lesson.start_date)
    results = []

    for lesson in lessons:
        if lesson.event_id == lesson_id:
            results.append(lesson)

    return results


def get_lessons_by_name(lessons: list[Lesson], lesson_name: str) -> list[Lesson]:
    lessons.sort(key=lambda lesson: lesson.start_date)
    results = []

    for lesson in lessons:
        if lesson.name.lower() == lesson_name.lower():
            results.append(lesson)

    return results


# def get_event_id_by_name(
#     lessons: list[Lesson], lesson_name: str
# ) -> list[Lesson]:
#     lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
#     results = []
#     for lesson in lessons:
#         if lesson_name in lesson["name"]:
#             if lesson["eventId"] not in results:
#                 results.append(lesson["eventId"])
#     return results


def get_weekly_schedule(lessons: list[Lesson], week: int = None) -> list[list[Lesson]]:
    now = datetime.now()

    if week is not None:
        year_start = datetime(now.year, 1, 1)
        start_of_week = (
            year_start
            + timedelta(weeks=week - 1)
            - timedelta(days=year_start.weekday())
        )
    else:
        start_of_week = datetime(now.year, now.month, now.day) - timedelta(
            days=now.weekday()
        )

    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)

    week_lessons = [
        lesson
        for lesson in lessons
        if start_of_week <= lesson.start_date <= end_of_week
    ]

    week_lessons.sort(key=lambda lesson: lesson.start_date)
    schedule = [[] for _ in range(7)]

    for lesson in week_lessons:
        schedule[lesson.start_date.weekday()].append(lesson)

    return schedule
