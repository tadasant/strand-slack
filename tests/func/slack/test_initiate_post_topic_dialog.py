from http import HTTPStatus
from urllib.parse import urlencode

import pytest
from flask import url_for

from src.config import config
from src.domain.models.portal.SlackAgent import SlackAgent
from src.domain.models.portal.SlackAgentStatus import SlackAgentStatus
from src.domain.models.portal.SlackApplicationInstallation import SlackApplicationInstallation
from src.domain.models.portal.SlackTeam import SlackTeam
from src.domain.models.portal.SlackUser import SlackUser
from tests.factories.slackfactories import SlashCommandRequestFactory
from tests.utils import wait_until


@pytest.mark.usefixtures('client_class')  # pytest-flask's client_class adds self.client
class TestInitiatePostTopicDialog:
    # For assertions
    fake_slash_command_request = SlashCommandRequestFactory.create()

    # For setup
    target_endpoint = 'slack.slashcommandresource'
    default_payload = {
        'token': 'unverified-token',
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
    default_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    def test_post_valid_unauthenticated_slack(self):
        target_url = url_for(endpoint=self.target_endpoint)
        response = self.client.post(path=target_url, headers=self.default_headers, data=urlencode(self.default_payload))
        assert 'error' in response.json

    def test_post_valid_authenticated_slack(self, slack_client_class, mocker, slack_agent_repository):
        mocker.spy(slack_client_class, 'api_call')
        target_url = url_for(endpoint=self.target_endpoint)
        payload = self.default_payload.copy()
        payload['command'] = '/codeclippy'
        payload['text'] = ''
        payload['token'] = config["SLACK_VERIFICATION_TOKEN"]

        # Need team's slack agent to be present in memory
        slack_agent_repository.add_slack_agent(slack_agent=SlackAgent(
            status=SlackAgentStatus.ACTIVE,
            slack_team=SlackTeam(id=self.fake_slash_command_request.team_id),
            slack_application_installation=SlackApplicationInstallation(access_token='doesnt matter',
                                                                        installer=SlackUser(id='doesnt matter'),
                                                                        bot_access_token='doesnt matter'))
        )

        response = self.client.post(path=target_url, headers=self.default_headers, data=urlencode(payload))

        assert HTTPStatus.NO_CONTENT == response.status_code
        outcome = wait_until(condition=lambda: slack_client_class.api_call.call_count == 1)
        assert outcome, 'SlackClient api_call was never called'
        assert slack_client_class.api_call.call_args[1]['method'] == 'dialog.open'
        assert slack_client_class.api_call.call_args[1]['trigger_id'] == self.fake_slash_command_request.trigger_id
