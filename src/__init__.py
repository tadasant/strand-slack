from http.__init__ import HTTPStatus

from flask import Flask, jsonify
from marshmallow import ValidationError

from src.blueprints import slack, coreapi
from src.utilities.logging import get_logger
from src.models.exceptions.UnauthorizedException import UnauthorizedException
from src.models.exceptions.UnexpectedSlackException import UnexpectedSlackException
from src.models.exceptions.WrapperException import WrapperException
from src.utilities.wrappers.CoreApiClientWrapper import CoreApiClientWrapper
from src.utilities.wrappers.SlackClientWrapper import SlackClientWrapper


def handle_slack_integration_exception(error):
    logger = get_logger('Flask')
    response = jsonify({'error': error.message if error.message else repr(error)})
    response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    logger.error(response.data)
    return response


def handle_validation_exception(error):
    logger = get_logger('Flask')
    response = jsonify({'error': error.messages})
    response.status_code = HTTPStatus.BAD_REQUEST
    logger.error(response.data)
    return response


def handle_authorization_exception(error):
    logger = get_logger('Flask')
    response = jsonify({'error': error.message if error.message else repr(error)})
    response.status_code = HTTPStatus.UNAUTHORIZED
    logger.error(response.data)
    return response


def create_app(core_api_client, SlackClientClass, slack_verification_tokens, core_api_verification_token):
    app = Flask(__name__)

    app.register_blueprint(coreapi.blueprint, url_prefix='/core_api')
    app.register_blueprint(slack.blueprint, url_prefix='/slack')

    app.add_url_rule('/health', None, lambda: 'Ok')

    app.register_error_handler(UnauthorizedException, handle_authorization_exception)
    app.register_error_handler(ValidationError, handle_validation_exception)
    app.register_error_handler(UnexpectedSlackException, handle_slack_integration_exception)
    app.register_error_handler(WrapperException, handle_slack_integration_exception)

    init_wrappers(app=app, core_api_client=core_api_client, SlackClientClass=SlackClientClass)
    init_authentication(app=app, slack_verification_tokens=slack_verification_tokens,
                        core_api_verification_token=core_api_verification_token)

    return app


def init_wrappers(app, core_api_client, SlackClientClass):
    app.core_api_client_wrapper = CoreApiClientWrapper(core_api_client=core_api_client)
    app.slack_client_wrapper = SlackClientWrapper(SlackClientClass=SlackClientClass)


def init_authentication(app, slack_verification_tokens, core_api_verification_token):
    app.slack_verification_tokens = slack_verification_tokens
    app.core_api_verification_token = core_api_verification_token
