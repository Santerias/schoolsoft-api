class Localization:
    def __init__(self, api):
        self.api = api

    def get_context(self) -> dict:
        return self.api._request("get", "/localization/context")

    def get_text(self, *key_text: str) -> dict:
        key_text_str = "&".join([f"keyText={key}" for key in key_text])
        return self.api._request("get", f"/localization/texts/?{key_text_str}")
