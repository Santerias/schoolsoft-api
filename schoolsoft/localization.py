class Localization:
    def __init__(self, api):
        self.api = api

    def get_localization_context(self) -> dict:
        return self.api._request("get", "/localization/context")

    # TODO: Allow for as many as possible key_text parameters, since that's how the API works
    def get_localization_text(self, key_text: str) -> dict:
        return self.api._request("get", f"/localization/texts/?keyText={key_text}")
