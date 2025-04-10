class HubAPIError(Exception):
    """Base class for all Giskard Hub API errors."""

    def __init__(
        self, message: str, status_code: int = None, response_text: str = None
    ):
        self.message = message
        self.status_code = status_code
        self.response_text = response_text
        super().__init__(self.message)


class HubConnectionError(HubAPIError):
    """Error raised when a connection to Giskard Hub fails."""


class HubValidationError(HubAPIError):
    """Error raised when the API request validation fails."""


class HubJSONDecodeError(HubAPIError):
    """Error raised when the API response cannot be decoded as JSON."""


class HubAuthenticationError(HubAPIError):
    """Error raised when authentication with the Hub fails."""


class HubForbiddenError(HubAPIError):
    """Error raised when the user is not authorized to access a resource."""
