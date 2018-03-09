from src.models.exceptions.SlackCommunicationException import SlackCommunicationException


class UnexpectedSlackException(SlackCommunicationException):
    """Raised when Slack sends a request with an unexpected (likely mis-modeled) payload"""

    def __init__(self, message):
        super().__init__(message=message)
