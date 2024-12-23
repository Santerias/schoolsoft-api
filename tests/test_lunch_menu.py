import pytest

from schoolsoft import LunchMenu
from schoolsoft.models import Lunch


@pytest.fixture
def lunch_menu(mocker):
    api_mock = mocker.Mock()
    return LunchMenu(api_mock)


def test_get_menu_success(lunch_menu):
    mock_response = [
        {
            "dayId": 1,
            "dishes": [
                {
                    "dishType": "Dagens Lunch",
                    "dish": "Kycklinggryta med kokos, röd curry och lime serveras med ris.\r\nGrönsaksgryta med kokos, röd curry och lime serveras med ris.",
                }
            ],
        },
        {
            "dayId": 2,
            "dishes": [
                {
                    "dishType": "Dagens Lunch",
                    "dish": "Panerad fisk med kokt potatis och remouladsås.\r\nGrönsaksbiff med kokt potatis remouladsås.",
                }
            ],
        },
        {
            "dayId": 3,
            "dishes": [
                {
                    "dishType": "Dagens Lunch",
                    "dish": "Pasta med kalkon och ostsås.\r\nPasta med ost och broccolisås.",
                }
            ],
        },
        {
            "dayId": 4,
            "dishes": [
                {
                    "dishType": "Dagens Lunch",
                    "dish": "Falafel serveras med ris och vitlöksås.\r\n",
                }
            ],
        },
        {
            "dayId": 5,
            "dishes": [
                {
                    "dishType": "Dagens Lunch",
                    "dish": "Pasta Bolognese.\r\nPasta & sojafärssås.",
                }
            ],
        },
    ]
    lunch_menu.api._request.return_value = mock_response
    result = lunch_menu.get_menu(40)

    assert isinstance(result, Lunch)
    assert len(result.menu) == 5
    assert result.menu[0].dayId == 1
    assert result.menu[0].dishes[0].dishType == "Dagens Lunch"
    assert (
        result.menu[0].dishes[0].dish
        == "Kycklinggryta med kokos, röd curry och lime serveras med ris.\r\nGrönsaksgryta med kokos, röd curry och lime serveras med ris."
    )


def test_get_empty_menu(lunch_menu):
    lunch_menu.api._request.return_value = []
    result = lunch_menu.get_menu(40)

    assert isinstance(result, Lunch)
    assert len(result.menu) == 0
