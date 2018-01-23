from flask import Flask

from src.blueprints import hooks, slackapps
from src.exceptions import BotAlreadyExists, handle_bot_already_exists_usage
from src.wrappers.PortalClientWrapper import PortalClientWrapper
from src.wrappers.SlackClientWrapper import SlackClientWrapper
from src.config import config


def create_app(portal_client, SlackClientClass):
    app = Flask(__name__)

    app.register_blueprint(slackapps.blueprint, url_prefix='/slackapps')
    app.register_blueprint(hooks.blueprint, url_prefix='/hooks')

    app.register_error_handler(BotAlreadyExists, handle_bot_already_exists_usage)

    init_wrappers(app=app, portal_client=portal_client, SlackClientClass=SlackClientClass)

    return app


def init_wrappers(app, portal_client, SlackClientClass):
    app._portal_client_wrapper = PortalClientWrapper(portal_client=portal_client)
    tokens_by_team_id = app._portal_client_wrapper.get_slack_tokens_by_slack_team_id()
    app._slack_client_wrapper = SlackClientWrapper(tokens_by_team_id=tokens_by_team_id,
                                                   SlackClientClass=SlackClientClass)
