import pytest

from schoolsoft import School, Student, User


@pytest.fixture
def student(mocker):
    api_mock = mocker.Mock()
    return Student(api_mock)


def test_get_student(student):
    mock_response = {
        "firstName": "John",
        "lastName": "Doe",
        "pictureURL": "/path/to/picture",
        "unreadMessages": 0,
        "active": True,
    }

    student.api._request.return_value = mock_response
    result = student.get_student()

    assert isinstance(result, User)
    assert result.first_name == "John"
    assert result.last_name == "Doe"


def test_get_schools(student):
    mock_response = [
        {"orgId": 10, "schoolName": "School 1", "className": "Grade 1"},
        {"orgId": 20, "schoolName": "School 2", "className": "Grade 1"},
    ]

    student.api._request.return_value = mock_response
    result = student.get_schools()

    assert isinstance(result, list)

    for index, school in enumerate(result):
        assert isinstance(school, School)
        assert school.org_id == mock_response[index]["orgId"]
        assert school.name == mock_response[index]["schoolName"]
        assert school.grade == mock_response[index]["className"]


def test_get_skolon(student):
    mock_response = {"skolon": "data"}

    student.api._request.return_value = mock_response
    result = student.get_skolon()

    assert isinstance(result, dict)
    assert result == mock_response


def test_get_school_logo(student):
    mock_response = {
        "src": "/path/jsp/logoFile.jsp?logoname=logo.png",
        "url": "http://example.com/",
    }

    student.api._request.return_value = mock_response
    result = student.get_school_logo()

    assert isinstance(result, dict)
    assert result == mock_response


def test_get_sidebar_sectiongroups(student):
    mock_response = [
        {
            "label": "MIN SKOLA",
            "key": "MY_SCHOOL",
            "sections": [
                {
                    "label": "Skolinfo",
                    "items": [
                        {
                            "label": "Skolinformation",
                            "url": "right_student_school.jsp",
                            "id": "schoolInformation",
                            "target": "_self",
                        },
                        {
                            "label": "Nyheter",
                            "url": "right_student_news.jsp",
                            "id": "news",
                            "target": "_self",
                        },
                        {
                            "label": "Matsedel",
                            "url": "../../react/#/student/lunchmenu",
                            "id": "lunchmenu",
                            "target": "_self",
                        },
                        {
                            "label": "Kontaktlistor",
                            "url": "right_student_staff.jsp",
                            "id": "contactlist",
                            "target": "_self",
                        },
                        {
                            "label": "Verksamhetslogg",
                            "url": "right_student_blogpost.jsp",
                            "id": "blogpost",
                            "target": "_self",
                        },
                        {
                            "label": "Forum",
                            "url": "right_student_forum_list.jsp?objectpage=1",
                            "id": "forum_list",
                            "target": "_self",
                        },
                    ],
                    "key": "SCHOOL_INFO",
                },
                {
                    "label": "Schema",
                    "items": [
                        {
                            "label": "Schema & Kalender",
                            "url": "../../react/#/student/calendar",
                            "id": "bryntum",
                            "target": "_self",
                        },
                        {
                            "label": "Bokningar",
                            "url": "right_student_timebooking.jsp",
                            "id": "timebooking",
                            "target": "_self",
                        },
                        {
                            "label": "Provschema",
                            "url": "right_student_test_schedule.jsp",
                            "id": "test_schedule",
                            "target": "_self",
                        },
                    ],
                    "key": "SCHEDULE",
                },
                {
                    "label": "Närvaro",
                    "items": [
                        {
                            "label": "Frånvaroanmälan",
                            "url": "right_student_absence.jsp",
                            "id": "absence",
                            "target": "_self",
                        },
                        {
                            "label": "Översikt",
                            "url": "right_student_lesson_status.jsp",
                            "id": "lesson_status",
                            "target": "_self",
                        },
                        {
                            "label": "Rapport",
                            "url": "right_student_absence_student.jsp",
                            "id": "absence_student",
                            "target": "_self",
                        },
                    ],
                    "key": "PRESENCE",
                },
            ],
        },
        {
            "label": "MITT BIBLIOTEK",
            "key": "MY_LIBRARY",
            "sections": [
                {
                    "label": "Kurs",
                    "items": [
                        {
                            "label": "Kurs 1",
                            "url": "right_student_subject.jsp?requestid=10000",
                            "id": "gradesubject10000",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 2",
                            "url": "right_student_subject.jsp?requestid=10001",
                            "id": "gradesubject10001",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 3",
                            "url": "right_student_subject.jsp?requestid=10002",
                            "id": "gradesubject10002",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 4",
                            "url": "right_student_subject.jsp?requestid=10003",
                            "id": "gradesubject10003",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 5",
                            "url": "right_student_subject.jsp?requestid=10004",
                            "id": "gradesubject10004",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 6",
                            "url": "right_student_subject.jsp?requestid=10005",
                            "id": "gradesubject10005",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 7",
                            "url": "right_student_subject.jsp?requestid=10006",
                            "id": "gradesubject10006",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 8",
                            "url": "right_student_subject.jsp?requestid=10007",
                            "id": "gradesubject10007",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 9",
                            "url": "right_student_subject.jsp?requestid=10008",
                            "id": "gradesubject10008",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 10",
                            "url": "right_student_subject.jsp?requestid=10009",
                            "id": "gradesubject10009",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 11",
                            "url": "right_student_subject.jsp?requestid=10010",
                            "id": "gradesubject10010",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 12",
                            "url": "right_student_subject.jsp?requestid=10011",
                            "id": "gradesubject10011",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 13",
                            "url": "right_student_subject.jsp?requestid=10012",
                            "id": "gradesubject10012",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 14",
                            "url": "right_student_subject.jsp?requestid=10013",
                            "id": "gradesubject10013",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 15",
                            "url": "right_student_subject.jsp?requestid=10014",
                            "id": "gradesubject10014",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 16",
                            "url": "right_student_subject.jsp?requestid=10015",
                            "id": "gradesubject10015",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 17",
                            "url": "right_student_subject.jsp?requestid=10016",
                            "id": "gradesubject10016",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 18",
                            "url": "right_student_subject.jsp?requestid=10017",
                            "id": "gradesubject10017",
                            "target": "_self",
                        },
                        {
                            "label": "Kurs 19",
                            "url": "right_student_subject.jsp?requestid=10018",
                            "id": "gradesubject10018",
                            "target": "_self",
                        },
                    ],
                    "key": "SUBJECT",
                },
                {
                    "label": "Undervisning",
                    "items": [
                        {
                            "label": "Planeringar & uppgifter",
                            "url": "right_student_planning.jsp?objectpage=1",
                            "id": "planning",
                            "target": "_self",
                        },
                        {
                            "label": "Uppgifter & resultat",
                            "url": "right_student_test.jsp?objectpage=1",
                            "id": "test_results",
                            "target": "_self",
                        },
                    ],
                    "key": "LESSON",
                },
                {
                    "label": "Elevdokument",
                    "items": [
                        {
                            "label": "Elevdokument",
                            "url": "right_student_review.jsp",
                            "id": "review",
                            "target": "_self",
                        },
                        {
                            "label": "Sammantagen bedömning",
                            "url": "right_student_ability.jsp?objectpage=1&schooltype=9",
                            "id": "student_ability2",
                            "target": "_self",
                        },
                        {
                            "label": "Individuell studieplan",
                            "url": "right_student_course.jsp",
                            "id": "course",
                            "target": "_self",
                        },
                    ],
                    "key": "REVIEW",
                },
                {
                    "label": "Filer & länkar",
                    "items": [
                        {
                            "label": "Alla filer & länkar",
                            "url": "right_student_library.jsp",
                            "id": "library",
                            "target": "_self",
                        }
                    ],
                    "key": "FILE",
                },
            ],
        },
    ]

    student.api._request.return_value = mock_response
    result = student.get_sidebar_sectiongroups()

    assert isinstance(result, list)
    assert result == mock_response


def test_get_sidebar_autocompleteoptions(student):
    mock_response = [
        {
            "itemLabel": "Skolinformation",
            "sectionLabel": "Skolinfo",
            "url": "right_student_school.jsp",
        },
        {
            "itemLabel": "Nyheter",
            "sectionLabel": "Skolinfo",
            "url": "right_student_news.jsp",
        },
        {
            "itemLabel": "Matsedel",
            "sectionLabel": "Skolinfo",
            "url": "../../react/#/student/lunchmenu",
        },
        {
            "itemLabel": "Kontaktlistor",
            "sectionLabel": "Skolinfo",
            "url": "right_student_staff.jsp",
        },
        {
            "itemLabel": "Verksamhetslogg",
            "sectionLabel": "Skolinfo",
            "url": "right_student_blogpost.jsp",
        },
        {
            "itemLabel": "Forum",
            "sectionLabel": "Skolinfo",
            "url": "right_student_forum_list.jsp?objectpage=1",
        },
        {
            "itemLabel": "Schema & Kalender",
            "sectionLabel": "Schema",
            "url": "../../react/#/student/calendar",
        },
        {
            "itemLabel": "Bokningar",
            "sectionLabel": "Schema",
            "url": "right_student_timebooking.jsp",
        },
        {
            "itemLabel": "Provschema",
            "sectionLabel": "Schema",
            "url": "right_student_test_schedule.jsp",
        },
        {
            "itemLabel": "Frånvaroanmälan",
            "sectionLabel": "Närvaro",
            "url": "right_student_absence.jsp",
        },
        {
            "itemLabel": "Översikt",
            "sectionLabel": "Närvaro",
            "url": "right_student_lesson_status.jsp",
        },
        {
            "itemLabel": "Rapport",
            "sectionLabel": "Närvaro",
            "url": "right_student_absence_student.jsp",
        },
        {
            "itemLabel": "Kurs 1",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10000",
        },
        {
            "itemLabel": "Kurs 2",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10001",
        },
        {
            "itemLabel": "Kurs 3",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10002",
        },
        {
            "itemLabel": "Kurs 4",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10003",
        },
        {
            "itemLabel": "Kurs 5",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10004",
        },
        {
            "itemLabel": "Kurs 6",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10005",
        },
        {
            "itemLabel": "Kurs 7",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10006",
        },
        {
            "itemLabel": "Kurs 8",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10007",
        },
        {
            "itemLabel": "Kurs 9",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10008",
        },
        {
            "itemLabel": "Kurs 10",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10009",
        },
        {
            "itemLabel": "Kurs 11",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10010",
        },
        {
            "itemLabel": "Kurs 12",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10011",
        },
        {
            "itemLabel": "Kurs 13",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10012",
        },
        {
            "itemLabel": "Kurs 14",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10013",
        },
        {
            "itemLabel": "Kurs 15",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10014",
        },
        {
            "itemLabel": "Kurs 16",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10015",
        },
        {
            "itemLabel": "Kurs 17",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10016",
        },
        {
            "itemLabel": "Kurs 18",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10017",
        },
        {
            "itemLabel": "Kurs 19",
            "sectionLabel": "Kurs",
            "url": "right_student_subject.jsp?requestid=10018",
        },
        {
            "itemLabel": "Planeringar & uppgifter",
            "sectionLabel": "Undervisning",
            "url": "right_student_planning.jsp?objectpage=1",
        },
        {
            "itemLabel": "Uppgifter & resultat",
            "sectionLabel": "Undervisning",
            "url": "right_student_test.jsp?objectpage=1",
        },
        {
            "itemLabel": "Elevdokument",
            "sectionLabel": "Elevdokument",
            "url": "right_student_review.jsp",
        },
        {
            "itemLabel": "Sammantagen bedömning",
            "sectionLabel": "Elevdokument",
            "url": "right_student_ability.jsp?objectpage=1&schooltype=9",
        },
        {
            "itemLabel": "Individuell studieplan",
            "sectionLabel": "Elevdokument",
            "url": "right_student_course.jsp",
        },
        {
            "itemLabel": "Alla filer & länkar",
            "sectionLabel": "Filer & länkar",
            "url": "right_student_library.jsp",
        },
    ]

    student.api._request.return_value = mock_response
    result = student.get_sidebar_autocompleteoptions()

    assert isinstance(result, list)
    assert result == mock_response
