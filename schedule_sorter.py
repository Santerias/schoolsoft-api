import json
from datetime import datetime

# Change path to your json file containing your lessons data
with open("test_lesson_data.json", "r") as f:
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


print(f"Previous Lesson: {get_previous_lesson(data)}")
print(f"Current Lesson: {get_current_lesson(data)}")
print(f"Next Lesson: {get_next_lesson(data)}")