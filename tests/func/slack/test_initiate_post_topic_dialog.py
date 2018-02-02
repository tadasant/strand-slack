from copy import deepcopy
from http import HTTPStatus
from urllib.parse import urlencode

from flask import url_for

from src.config import config
from tests.factories.slackfactories import SlashCommandRequestFactory
from tests.func.slack.TestSlackFunction import TestSlackFunction
from tests.utils import wait_until


class TestInitiatePostTopicDialog(TestSlackFunction):
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

    def test_post_valid_authenticated_slack(self, slack_client_class, mocker, slack_agent_repository):
        mocker.spy(slack_client_class, 'api_call')
        target_url = url_for(endpoint=self.target_endpoint)
        payload = deepcopy(self.default_payload)
        payload['command'] = '/codeclippy'
        payload['text'] = ''
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_slash_command_request.team_id)

        response = self.client.post(path=target_url, headers=self.default_headers, data=urlencode(payload))

        assert HTTPStatus.NO_CONTENT == response.status_code
        outcome = wait_until(condition=lambda: slack_client_class.api_call.call_count == 1)
        assert outcome, 'SlackClient api_call was never called'
        self.assert_values_in_call_args_list(
            params_to_expecteds=[
                {
                    'method': 'dialog.open',
                    'trigger_id': self.fake_slash_command_request.trigger_id
                }
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )
