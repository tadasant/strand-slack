from flask import current_app
from flask_restful import Resource

from src.utilities.logging import get_logger
from src.models.exceptions.SlackCommunicationException import SlackCommunicationException


class SlackResource(Resource):
    """Parent for all Slack callback resources"""
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def _authenticate(self, payload):
        """Check if the Slack payload has the verification token"""
        self.logger.debug(f'Request payload: {payload}')
        if payload['token'] not in current_app.slack_verification_tokens:
            message = 'Invalid slack verification token'
            self.logger.error(message)
            raise SlackCommunicationException(message=message)
