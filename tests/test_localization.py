import pytest

from schoolsoft import Localization

# from schoolsoft.models import


@pytest.fixture
def localization(mocker):
    api_mock = mocker.Mock()
    return Localization(api_mock)


def test_get_context(localization):
    mock_response = {
        "orgId": 10,
        "langCode": "sv",
        "textVersion": 1733888982,
        "context": "nti",
    }

    localization.api._request.return_value = mock_response
    result = localization.get_context()

    assert isinstance(result, dict)

    assert result["orgId"] == 10
    assert result["langCode"] == "sv"


def test_get_text(localization):
    mock_response = {
        "MES_Lunch_Empty_Placeholder_2": "Vänligen kom tillbaka senare.",
        "MES_Lunch_Empty_Placeholder_1": "Det finns ännu ingen matsedel inlagd för denna vecka.",
    }

    localization.api._request.return_value = mock_response
    result = localization.get_text(
        "MES_Lunch_Empty_Placeholder_2", "MES_Lunch_Empty_Placeholder_1"
    )

    assert isinstance(result, dict)
    assert result["MES_Lunch_Empty_Placeholder_2"] == "Vänligen kom tillbaka senare."
    assert (
        result["MES_Lunch_Empty_Placeholder_1"]
        == "Det finns ännu ingen matsedel inlagd för denna vecka."
    )
