from datetime import datetime, timedelta


class Utils:
    def __init__(self, api):
        self.api = api

    def get_previous_lesson(self, pretty_print: bool = False) -> dict | str:
        """
        Returns authenticated user's previous lesson as a dict, but can also return
        pretty printed str with minimal information
        """

        now = datetime.now()
        lessons = self.api.calendar.get_calendar_student_lessons()
        lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        previous_lesson = None

        for lesson in lessons:
            end_date = datetime.fromisoformat(lesson["endDate"])
            if end_date < now:
                previous_lesson = lesson
            else:
                break

        if pretty_print:
            return f"{previous_lesson["name"]} in room {previous_lesson["room"]} with {previous_lesson["teacher"]} at {previous_lesson["startDate"]} to {previous_lesson["endDate"]}"
        else:
            return previous_lesson

    def get_current_lesson(self, pretty_print: bool = False) -> dict | str:
        now = datetime.now()
        lessons = self.api.calendar.get_calendar_student_lessons()
        for lesson in lessons:
            start_date = datetime.fromisoformat(lesson["startDate"])
            end_date = datetime.fromisoformat(lesson["endDate"])
            if start_date <= now <= end_date:
                if pretty_print:
                    return f"{lesson["name"]} in room {lesson["room"]} with {lesson["teacher"]} at {lesson["startDate"]} to {lesson["endDate"]}"
                else:
                    return lesson
        return None

    def get_next_lesson(self, pretty_print: bool = False) -> dict | str:
        now = datetime.now()
        lessons = self.api.calendar.get_calendar_student_lessons()
        lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        for lesson in lessons:
            start_date = datetime.fromisoformat(lesson["startDate"])
            if start_date > now:
                if pretty_print:
                    return f"{lesson["name"]} in room {lesson["room"]} with {lesson["teacher"]} at {lesson["startDate"]} to {lesson["endDate"]}"
                else:
                    return lesson
        return None

    def get_todays_lessons(self) -> list:
        now = datetime.now().date()
        lessons = self.api.calendar.get_calendar_student_lessons()
        todays_lessons = [
            lesson
            for lesson in lessons
            if datetime.fromisoformat(lesson["startDate"]).date() == now
        ]
        todays_lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        return todays_lessons

    def get_lesson_status(self, lesson_id: int, week: int) -> dict:
        lessons = self.api.calendar.get_calendar_student_lessons()
        lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        for lesson in lessons:
            if "studentLessonStatus" in lesson:
                student_status = lesson["studentLessonStatus"]
                if (
                    student_status["week"] == week
                    and student_status["lessonId"] == lesson_id
                ):
                    return lesson
        return None

    def get_lessons_by_id(self, lesson_id: int) -> list[dict]:
        lessons = self.api.calendar.get_calendar_student_lessons()
        lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        results = []
        for lesson in lessons:
            if lesson["eventId"] == lesson_id:
                results.append(lesson)
        return results

    def get_lessons_by_name(self, lesson_name: str) -> list[dict]:
        lessons = self.api.calendar.get_calendar_student_lessons()
        lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        results = []
        for lesson in lessons:
            if lesson_name in lesson["name"]:
                results.append(lesson)
        return results

    def get_event_id_by_name(self, lesson_name: str) -> list[dict]:
        lessons = self.api.calendar.get_calendar_student_lessons()
        lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
        results = []
        for lesson in lessons:
            if lesson_name in lesson["name"]:
                if lesson["eventId"] not in results:
                    results.append(lesson["eventId"])
        return results

    def get_weekly_schedule(self) -> list[list]:
        now = datetime.now()
        lessons = self.api.calendar.get_calendar_student_lessons()
        start_of_week = datetime(now.year, now.month, now.day) - timedelta(
            days=now.weekday()
        )
        end_of_week = start_of_week + timedelta(
            days=6, hours=23, minutes=59, seconds=59
        )

        week_lessons = []
        for lesson in lessons:
            lesson_start = datetime.fromisoformat(lesson["startDate"])
            if start_of_week <= lesson_start <= end_of_week:
                week_lessons.append(lesson)

        week_lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))

        schedule = [[] for _ in range(7)]

        for lesson in week_lessons:
            lesson_date = datetime.fromisoformat(lesson["startDate"])
            day_of_week = lesson_date.weekday()
            schedule[day_of_week].append(lesson)

        return schedule
