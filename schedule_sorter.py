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
        lesson for lesson in lessons
        if datetime.fromisoformat(lesson["startDate"]).date() == now
    ]
    todays_lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
    return todays_lessons

def get_lesson_status(lessons, lessonId, week):
    now = datetime.now().timestamp()
    lessons.sort(key=lambda x: datetime.fromisoformat(x["startDate"]))
    for lesson in lessons:
        if "studentLessonStatus" in lesson:
            student_status = lesson["studentLessonStatus"]
            if student_status["week"] == week and student_status["lessonId"] == lessonId:
                return f"Lesson ID: {student_status["lessonId"]}\nWeek: {student_status["week"]}\nComment: {student_status["comment"]}\nAbsence: {student_status["absence"]}\nAttendance: {student_status["name"]}\nReason: {student_status["reason"]}\n"
    return None


print(f"Previous Lesson: {get_previous_lesson(data)}")
print(f"Current Lesson: {get_current_lesson(data)}")
print(f"Next Lesson: {get_next_lesson(data)}")
print(f"\nToday's lessons: {get_todays_lessons(data)}")

print("\nToday's lessons (pretty printed):")
for lesson in get_todays_lessons(data):
    print(f"{lesson["name"]} at {lesson["startDate"]} to {lesson["endDate"]}\n")

print("Status for GYAREE:\n")
print(get_lesson_status(data, 379377, 35))