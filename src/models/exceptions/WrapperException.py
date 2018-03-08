from src.models.exceptions.SlackIntegrationException import SlackIntegrationException


class WrapperException(SlackIntegrationException):
    """Raised when a Wrapper fails to perform an operation due to errors (either unexpected states or HTTP issues)"""

    def __init__(self, wrapper_name, message, errors=None):
        super().__init__(message=message)

        self.wrapper_name = wrapper_name
        self.errors = errors
