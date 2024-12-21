# SchoolSoft API Wrapper

<img src="https://schoolsoft.se/wp-content/uploads/2023/10/schoolsoft_logo_dark_rounded.svg" align="right"
    alt="Official SchoolSoft logo" width="64" height="64">

This project is an API wrapper for SchoolSoft's REST API written in Python, useful for easy integration with SchoolSoft and getting your schedule and so on.

- Handles authentication
- Helper functions (e.g. To fetch your next/upcoming lesson)

## Usage

> NOTE: Has only been tested with Python 3.13, you might run into issues otherwise.

Simple example to get your next/upcoming lesson

```python
from schoolsoft import Api

api = Api(username, password, school)
api.authenticate()
lessons = api.calendar.get_lessons()
print(schoolsoft.utils.get_next_lesson(lessons))
```

## Credits

This project is inspired by Blatzar's repo: [schoolsoft-api](https://github.com/Blatzar/schoolsoft-api) which is not being maintained anymore.
