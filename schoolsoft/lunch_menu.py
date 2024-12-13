class LunchMenu:
    def __init__(self, api):
        self.api = api

    def get_lunch_menu(self, week: str) -> dict:
        return self.api._request("get", f"/lunchmenu/week/{week}")
