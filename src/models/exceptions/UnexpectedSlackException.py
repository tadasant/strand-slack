from src.models.exceptions import SlackIntegrationException


class UnexpectedSlackException(SlackIntegrationException):
    """Raised when Slack sends a request with an unexpected (likely mis-modeled) payload"""

    def __init__(self, message):
        super().__init__(message=message)
