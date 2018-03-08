import re

from flask import current_app, request
from flask_restful import Resource

from src.utilities.logging import get_logger
from src.models.exceptions.UnauthorizedException import UnauthorizedException


class CoreApiResource(Resource):

    @classmethod
    def authenticate(cls, func):
        token_regex = r'Token (.*)'

        def wrapper(*args, **kwargs):
            get_logger('Flask').debug(f'Request args: {request.get_json()}')
            authorization_header = request.headers.get('Authorization')
            if authorization_header:
                matches = re.findall(token_regex, authorization_header)
                if len(matches) == 1:
                    token = matches[0]
                    if token == current_app.core_api_verification_token:
                        return func(*args, **kwargs)
            raise UnauthorizedException(message='CoreApi authorization failed.')

        return wrapper
