---
hide: navigation
---

# SAW

<img src="https://schoolsoft.se/wp-content/uploads/2023/10/schoolsoft_logo_dark_rounded.svg" align="right"
    alt="Official SchoolSoft logo" width="64" height="64">

<em>Easy Python wrapper for interacting with the SchoolSoft API</em>
<br><br>
![Static Badge](https://img.shields.io/badge/python-3.10_|_3.11_|_3.12_|_3.13-blue)

<!-- ---

**Documentation**: <a href="https://example.com" target="_blank">https://example.com</a>
<br><br>
**Source Code**: <a href="https://github.com/Santerias/schoolsoft-api" target="_blank">https://github.com/Santerias/schoolsoft-api</a>

--- -->

## Features

- **Authentication**: Handles login and session management.
- **Helper functions**: Quickly retrieve your schedule, upcoming lessons, and more.

## Installation

Prerequisites:

- Python 3.10 or higher
- pip 21.3 or higher

You can install SAW with `pip`:

> NOTE: It is not released on PyPI yet so you have to clone the repo and install via source

```bash
git clone https://github.com/Santerias/schoolsoft-api.git
cd schoolsoft-api
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

This will install the package in editable mode meaning you could modify the package to your likings and use that in your code by just simply importing schoolsoft in any file like this:

```python
import schoolsoft
```

## Usage

### Basic Example

Here's a simple example of how to get your next lesson:

```python title="next_lesson.py"
from schoolsoft import Api

api = Api(username, password, school)
api.authenticate()

lessons = api.calendar.get_lessons()
next_lesson = schoolsoft.utils.get_next_lesson(lessons)

print(next_lesson.name)
```

### Authenticating

To authenticate, you just need to pass your username, password, and school name to the `Api` object, then call `api.authenticate()`.

#### Fetching Lessons

The wrapper simplifies retrieving lessons. You can easily fetch all lessons with:

```python
lessons = api.calendar.get_lessons()
```

#### Get upcoming lesson

To get the next lesson, use the helper function:

```python
next_lesson = schoolsoft.utils.get_next_lesson(lessons)
```

## Credits

This project is inspired by Blatzar's repo: [schoolsoft-api](https://github.com/Blatzar/schoolsoft-api) which is not being maintained anymore.

## Contributing

To contribute to this project, clone the repository and install the required dependencies:

```bash
git clone https://github.com/Santerias/schoolsoft-api.git
cd schoolsoft-api
pip install -r requirements-dev.txt
pip install -e .
```

Make your own branch for PRs and dont modify the main or dev branch.

```bash
git checkout -b pr-branch
git add .
git commit -m "your commit message"
git push -u origin pr-branch
```

## License

This project is licensed under the terms of the MIT license.
