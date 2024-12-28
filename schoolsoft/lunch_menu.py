from .models import Lunch


class LunchMenu:
    """Represents the lunch menu endpoints of the school"""

    def __init__(self, api):
        self.api = api

    def get_menu(self, week: int) -> Lunch:
        """Returns the lunch menu for the provided week

        Args:
            week (int): Week number

        Returns:
            Lunch: Lunch object
        """
        return Lunch.from_dict(self.api._request("get", f"/lunchmenu/week/{week}"))
