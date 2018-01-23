from flask import Flask, g

from src.blueprints import slack, factory
from src.exceptions import BotAlreadyExists, handle_bot_already_exists_usage
from src.wrappers.PortalClientWrapper import PortalClientWrapper
from src.wrappers.SlackClientWrapper import SlackClientWrapper
from src.config import config


def create_app():
    app = Flask(__name__)

    app.register_blueprint(factory.blueprint, url_prefix='/factory')
    app.register_blueprint(slack.blueprint, url_prefix='/slack')

    app.register_error_handler(BotAlreadyExists, handle_bot_already_exists_usage)

    init_wrappers(app=app)

    return app


def init_wrappers(app):
    with app.app_context():
        g._portal_client_wrapper = PortalClientWrapper(log_file='logs/PortalClientWrapper.log',
                                                       host=config['PORTAL_HOST'],
                                                       endpoint=config['PORTAL_GRAPHQL_ENDPOINT'])
        tokens_by_team_id = g._portal_client_wrapper.get_slack_tokens_by_slack_team_id()
        g._slack_client_wrapper = SlackClientWrapper(tokens_by_team_id=tokens_by_team_id,
                                                     log_file='logs/SlackClientWrapper.log')
