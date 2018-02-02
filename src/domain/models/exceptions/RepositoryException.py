from src.domain.models.exceptions.SlackIntegrationException import SlackIntegrationException


class RepositoryException(SlackIntegrationException):
    """Raised by in-memory repository when unexpected operations happen"""

    def __init__(self, object_name, message):
        super().__init__(message=message)

        self.object_name = object_name
