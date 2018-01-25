from flask import Flask

from src.blueprints import slack, portal
from src.exceptions import BotAlreadyExists, handle_bot_already_exists_usage

from src.domain.repositories.SlackAgentRepository import slack_agent_repository
from src.wrappers.PortalClientWrapper import PortalClientWrapper
from src.wrappers.SlackClientWrapper import SlackClientWrapper


def create_app(portal_client, SlackClientClass):
    app = Flask(__name__)

    app.register_blueprint(portal.blueprint, url_prefix='/portal')
    app.register_blueprint(slack.blueprint, url_prefix='/slack')

    app.register_error_handler(BotAlreadyExists, handle_bot_already_exists_usage)

    init_wrappers(app=app, portal_client=portal_client, SlackClientClass=SlackClientClass)

    return app


def init_wrappers(app, portal_client, SlackClientClass):
    app.portal_client_wrapper = PortalClientWrapper(portal_client=portal_client)
    slack_agents = app.portal_client_wrapper.get_slack_agents()
    slack_agent_repository.set_slack_agents(slack_agents=slack_agents)
    app.slack_client_wrapper = SlackClientWrapper(SlackClientClass=SlackClientClass)
