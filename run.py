import os

from slackclient import SlackClient

from src import create_app
from src.utilities.clients.StrandApiClient import StrandApiClient
from src.config import config


def create_logs_dir_if_not_exists():
    if not os.path.exists('logs'):
        os.mkdir('logs')


if __name__ == '__main__':
    create_logs_dir_if_not_exists()
    app = create_app(
        strand_api_client=StrandApiClient(host=config['STRAND_API_HOST'], endpoint=config['STRAND_API_GRAPHQL_ENDPOINT'],
                                        email=config['STRAND_API_USER_EMAIL'], password=config['STRAND_API_USER_PASSWORD']),
        SlackClientClass=SlackClient,
        slack_verification_tokens=config['SLACK_VERIFICATION_TOKENS'],
        strand_api_verification_token=config['STRAND_API_VERIFICATION_TOKEN']
    )
    app.run(debug=config['FLASK_DEBUG'], host=config['HOST'], port=config['PORT'])
