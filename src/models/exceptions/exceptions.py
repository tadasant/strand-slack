from src.models.exceptions.SLAException import SLAException


class SlackCommunicationException(SLAException):
    """Raise when there's an over-the-wire issue receiving a request/response from Slack"""


class SlackTranslationException(SLAException):
    """Raise when there's a payload-related issue receiving a request/response from Slack"""


class StrandCommunicationException(SLAException):
    """Raise when there's an over-the-wire issue receiving a request/response from Strand"""


class StrandTranslationException(SLAException):
    """Raise when there's a payload-related issue receiving a request/response from Strand"""


class UnexpectedStateException(SLAException):
    """Raise whenever SLA encounters a state that should have been impossible"""


class UnauthorizedException(SLAException):
    """Raise when caller is not an authenticated user with appropriate authorization"""


class InvalidSlashCommandException(SLAException):
    """Raise whenever SLA encounters an invalid slash command"""
