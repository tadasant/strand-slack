import os

from slackclient import SlackClient

from src import create_app
from src.clients.PortalClient import PortalClient
from src.config import config


def create_logs_dir_if_not_exists():
    if not os.path.exists('logs'):
        os.mkdir('logs')


if __name__ == '__main__':
    create_logs_dir_if_not_exists()
    app = create_app(
        portal_client=PortalClient(host=config['PORTAL_HOST'], endpoint=config['PORTAL_GRAPHQL_ENDPOINT']),
        SlackClientClass=SlackClient,
        slack_verification_token=config['SLACK_VERIFICATION_TOKEN']
    )
    app.run(debug=config['FLASK_DEBUG'], host=config['HOST'], port=config['PORT'])
