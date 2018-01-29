from flask import current_app
from flask_restful import Resource

from src.common.logging import get_logger
from src.domain.models.exceptions.UnexpectedSlackException import UnexpectedSlackException


class SlackResource(Resource):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def _authenticate(self, payload):
        if payload['token'] != current_app.slack_verification_token:
            message = 'Invalid slack verification token'
            self.logger.error(message)
            raise UnexpectedSlackException(message=message)
