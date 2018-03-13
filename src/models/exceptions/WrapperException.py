from src.models.exceptions.exceptions import SlackCommunicationException


# TODO: DEPRECATED. Use something from exceptions.py

class WrapperException(SlackCommunicationException):
    """Raised when a Wrapper fails to perform an operation due to errors (either unexpected states or HTTP issues)"""

    def __init__(self, wrapper_name, message, errors=None):
        super().__init__(message=message)

        self.wrapper_name = wrapper_name
        self.errors = errors
