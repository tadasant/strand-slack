from flask import current_app, request
from flask_restful import Resource

from src.models.exceptions.exceptions import UnauthorizedException
from src.utilities.logging import get_logger


class SlackResource(Resource):
    """Parent for all Slack callback resources"""

    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    @classmethod
    def authenticate(cls, func):
        """Check if the Slack payload has the verification token"""

        def wrapper(*args, **kwargs):
            get_logger('Flask').debug(f'Request args: {request.get_json()}')
            payload = request.get_json()
            if payload['token'] not in current_app.slack_verification_tokens:
                message = 'Invalid slack verification token'
                get_logger('Flask').error(message)
                raise UnauthorizedException(message=message)
            return func(*args, **kwargs)

        return wrapper
