class ApiException(Exception):
    """Gets raised when the API returns an error."""

    pass


class InvalidCredentials(Exception):
    """Gets raised when the provided credentials are invalid."""

    pass
