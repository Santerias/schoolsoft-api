import json
from datetime import datetime, timedelta

# Change path to your json file containing your lessons data
with open("test_lesson_data.json", "r", encoding="UTF-8") as f:
    data = json.load(f)


def get_current_lesson(lessons):
    now = datetime.now()
    for lesson in lessons:
        start_date = datetime.fromisoformat(lesson["startDate"])
        end_date = datetime.fromisoformat(lesson["endDate"])
        if start_date <= now <= end_date:
            return f"{lesson["name"]} in room {lesson["room"]} with {lesson["teacher"]} at {lesson["startDate"]} to {lesson["endDate"]}"
    return None


def get_next_lesson(lessons):
    now = datetime.now()
    lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
    for lesson in lessons:
        start_date = datetime.fromisoformat(lesson["startDate"])
        if start_date > now:
            return f"{lesson["name"]} in room {lesson["room"]} with {lesson["teacher"]} at {lesson["startDate"]} to {lesson["endDate"]}"
    return None


def get_previous_lesson(lessons):
    now = datetime.now()
    lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
    previous_lesson = None
    for lesson in lessons:
        start_date = datetime.fromisoformat(lesson["startDate"])
        end_date = datetime.fromisoformat(lesson["endDate"])
        if end_date < now:
            previous_lesson = lesson
        else:
            break
    return f"{previous_lesson["name"]} in room {previous_lesson["room"]} with {previous_lesson["teacher"]} at {previous_lesson["startDate"]} to {previous_lesson["endDate"]}"
    # return previous_lesson


def get_todays_lessons(lessons):
    now = datetime.now().date()
    todays_lessons = [
        lesson
        for lesson in lessons
        if datetime.fromisoformat(lesson["startDate"]).date() == now
    ]
    todays_lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
    return todays_lessons


def get_lesson_status(lessons, lessonId, week, pp=False):
    lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
    for lesson in lessons:
        if "studentLessonStatus" in lesson:
            student_status = lesson["studentLessonStatus"]
            if (
                student_status["week"] == week
                and student_status["lessonId"] == lessonId
            ):
                if pp:
                    return f"Lesson ID: {student_status["lessonId"]}\nWeek: {student_status["week"]}\nComment: {student_status["comment"]}\nAbsence: {student_status["absence"]}\nAttendance: {student_status["name"]}\nReason: {student_status["reason"]}\n"
                else:
                    return student_status
    return None


def get_lessons_by_id(lessons, lessonId):
    lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
    results = []
    for lesson in lessons:
        if lesson["eventId"] == lessonId:
            results.append(lesson)
    return results


def get_lessons_by_name(lessons, lessonName):
    lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
    results = []
    for lesson in lessons:
        if lessonName in lesson["name"]:
            results.append(lesson)
    return results


def get_event_id_by_name(lessons, lessonName):
    lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
    results = []
    for lesson in lessons:
        if lessonName in lesson["name"]:
            if lesson["eventId"] not in results:
                results.append(lesson["eventId"])
    return results

def get_schedule(lessons):
    now = datetime.now()

    # Set the start of the week (Monday) at midnight (00:00:00) and end of the week (Sunday) at 23:59:59
    start_of_week = datetime(now.year, now.month, now.day) - timedelta(days=now.weekday())  # Monday midnight
    end_of_week = start_of_week + timedelta(days=6, hours=23, minutes=59, seconds=59)  # Sunday 23:59:59

    # Print the start and end of the current week to debug
    print(f"Start of the week: {start_of_week}")
    print(f"End of the week: {end_of_week}")

    # Filter lessons for the current week
    week_lessons = []
    for lesson in lessons:
        lesson_start = datetime.fromisoformat(lesson["startDate"])
        # Debug: print the lesson start date and if it falls in the current week
        print(f"Checking lesson: {lesson['name']} at {lesson_start}")
        if start_of_week <= lesson_start <= end_of_week:
            week_lessons.append(lesson)
        else:
            print(f"Excluded lesson: {lesson['name']} at {lesson_start}")

    week_lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))

    # Create a list for each day of the week (Monday to Sunday)
    schedule = {i: [] for i in range(7)}  # Initialize empty lists for each day (0=Monday, 6=Sunday)

    # Assign lessons to days
    for lesson in week_lessons:
        lesson_date = datetime.fromisoformat(lesson["startDate"])
        day_of_week = lesson_date.weekday()  # Get the day of the week (0=Monday, 6=Sunday)
        schedule[day_of_week].append(lesson)

    return schedule

print(f"Previous Lesson: {get_previous_lesson(data)}")
print(f"Current Lesson: {get_current_lesson(data)}")
print(f"Next Lesson: {get_next_lesson(data)}")
print(f"\nToday's lessons: {get_todays_lessons(data)}")

print("\nToday's lessons (pretty printed):")
for lesson in get_todays_lessons(data):
    print(f"{lesson["name"]} at {lesson["startDate"]} to {lesson["endDate"]}")

print("\nStatus for GYAREE:")
print(get_lesson_status(data, 379377, 35))

print("\nStatus for GYAREE (pretty printed):")
print(get_lesson_status(data, 379377, 35, pp=True))

eventId = 379418

print(f"\nResults for eventId {eventId}:")
amt_lessons1 = get_lessons_by_id(data, eventId)
for lesson in amt_lessons1:
    print(f"{lesson["name"]}: {lesson["startDate"]} - {lesson["endDate"]}")

print(f"\nThere are {len(amt_lessons1)} lessons with eventId {eventId}")

lessonName = "NAKNAK01a"

print(f"\nResults for lesson name: {lessonName} (pretty printed):")
amt_lessons2 = get_lessons_by_name(data, lessonName)
for lesson in amt_lessons2:
    print(f"{lesson["name"]}: {lesson["startDate"]} - {lesson["endDate"]}")

print(f"\nResults for lesson name: {lessonName}:")
print(get_lessons_by_name(data, lessonName))


print(f"\nThere are {len(amt_lessons2)} lessons with the lesson name {lessonName}")

lessonName = "NAKNAK01a"
print(f"\nEvent ID(s) for {lessonName}:")
print(get_event_id_by_name(data, lessonName))

print("\nSchedule of the week (raw):")
print(get_schedule(data))

print("\nSchedule of the week (pretty printed):")
schedule = get_schedule(data)
for day, lessons in schedule.items():
    weekday_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][day]
    print(f"\n{weekday_name}:")
    for lesson in lessons:
        print(f"{lesson["name"]} ({lesson["startDate"]} - {lesson["endDate"]})")