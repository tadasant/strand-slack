from http.__init__ import HTTPStatus

from flask import Flask, jsonify
from flask_cors import CORS
from marshmallow import ValidationError

from src.blueprints import slack, configure
from src.models.exceptions.SLAException import SLAException
from src.models.exceptions.WrapperException import WrapperException
from src.utilities.database import metadata, engine
from src.utilities.logging import get_logger
from src.utilities.wrappers.SlackClientWrapper import SlackClientWrapper
from src.utilities.wrappers.StrandApiClientWrapper import StrandApiClientWrapper


def handle_local_exception(error):
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


def create_app(strand_api_client, SlackClientClass, slack_verification_tokens, strand_api_verification_token):
    app = Flask(__name__)
    CORS(app=app)

    app.register_blueprint(slack.blueprint, url_prefix='/slack')
    app.register_blueprint(configure.blueprint, url_prefix='/configure')

    app.add_url_rule('/health', None, lambda: 'Ok')

    app.register_error_handler(ValidationError, handle_validation_exception)
    app.register_error_handler(SLAException, handle_local_exception)
    app.register_error_handler(WrapperException, handle_local_exception)

    init_wrappers(app=app, strand_api_client=strand_api_client, SlackClientClass=SlackClientClass)
    init_authentication(app=app, slack_verification_tokens=slack_verification_tokens,
                        strand_api_verification_token=strand_api_verification_token)
    init_database()

    return app


def init_wrappers(app, strand_api_client, SlackClientClass):
    app.strand_api_client_wrapper = StrandApiClientWrapper(strand_api_client=strand_api_client)
    app.slack_client_wrapper = SlackClientWrapper(SlackClientClass=SlackClientClass)


def init_authentication(app, slack_verification_tokens, strand_api_verification_token):
    app.slack_verification_tokens = slack_verification_tokens
    app.strand_api_verification_token = strand_api_verification_token


def init_database():
    metadata.create_all(engine)
