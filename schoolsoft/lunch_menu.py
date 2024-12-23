from .models import Lunch


class LunchMenu:
    def __init__(self, api):
        self.api = api

    def get_menu(self, week: int) -> Lunch:
        return Lunch.from_dict(self.api._request("get", f"/lunchmenu/week/{week}"))
