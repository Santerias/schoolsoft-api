from .models import DayMenu, Lunch


class LunchMenu:
    """Represents the lunch menu endpoints of the school"""

    def __init__(self, api):
        self.api = api

    def get_menu(self, week: int) -> list[Lunch]:
        """Returns the lunch menu for the provided week

        Args:
            week (int): Week number

        Returns:
            Lunch: Lunch object
        """
        response = self.api._request("get", f"/lunchmenu/week/{week}")
        day_menus = [DayMenu(**day) for day in response]
        return Lunch(menu=day_menus)
