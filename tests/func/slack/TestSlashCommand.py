from copy import deepcopy
from urllib.parse import urlencode

from flask import url_for

from src.config import config
from tests.factories.slackfactories import SlashCommandRequestFactory
from tests.func.slack.TestSlackFunction import TestSlackFunction


class TestSlashCommand(TestSlackFunction):
    # For assertions
    fake_slash_command_request = SlashCommandRequestFactory.create()

    # For setup
    target_endpoint = 'slack.slashcommandresource'
    default_payload = {
        'token': config["SLACK_VERIFICATION_TOKEN"],
        'team_id': fake_slash_command_request.team_id,
        'team_domain': 'doesnt matter',
        'channel_id': 'doesnt matter',
        'channel_name': 'doesnt matter',
        'user_id': fake_slash_command_request.user_id,
        'user_name': 'doesnt matter',
        'command': fake_slash_command_request.command,
        'text': fake_slash_command_request.text,
        'response_url': fake_slash_command_request.response_url,
        'trigger_id': fake_slash_command_request.trigger_id
    }

    def test_post_valid_unauthenticated_slack(self):
        target_url = url_for(endpoint=self.target_endpoint)
        payload = deepcopy(self.default_payload)
        payload['token'] = 'unverified token'

        response = self.client.post(path=target_url, headers=self.default_headers, data=urlencode(payload))
        assert response.json['error'] == 'Invalid slack verification token'
