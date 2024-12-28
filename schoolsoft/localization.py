class Localization:
    """Represents the localization endpoint of the SchoolSoft API"""

    def __init__(self, api):
        self.api = api

    def get_context(self) -> dict:
        """Gets the current localization context

        Returns:
            dict: JSON response
        """
        return self.api._request("get", "/localization/context")

    def get_text(self, *key_text: str) -> dict:
        """Returns the localized text for the provided keys

        Args:
            key_text (str): Key of the text to get translated

        Returns:
            dict: JSON response
        """
        key_text_str = "&".join([f"keyText={key}" for key in key_text])
        return self.api._request("get", f"/localization/texts/?{key_text_str}")
