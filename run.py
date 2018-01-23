import os

from slackclient import SlackClient

from src import create_app
from src.config import config
from src.clients.PortalClient import PortalClient


def create_logs_dir_if_not_exists():
    if not os.path.exists('logs'):
        os.mkdir('logs')


if __name__ == '__main__':
    create_logs_dir_if_not_exists()
    app = create_app(
        portal_client=PortalClient(host=config['PORTAL_HOST'], endpoint=config['PORTAL_GRAPHQL_ENDPOINT']),
        SlackClientClass=SlackClient
    )
    app.run(debug=True, host='0.0.0.0')
