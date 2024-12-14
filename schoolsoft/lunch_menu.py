class LunchMenu:
    def __init__(self, api):
        self.api = api

    def fetch_menu(self, week: str) -> dict:
        return self.api._request("get", f"/lunchmenu/week/{week}")
