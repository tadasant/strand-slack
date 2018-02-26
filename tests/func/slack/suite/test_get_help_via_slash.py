from copy import deepcopy
from http import HTTPStatus
from urllib.parse import urlencode

from flask import url_for

from tests.func.slack.TestSlashCommand import TestSlashCommand
from tests.utils import wait_until


class TestGetHelpViaSlash(TestSlashCommand):
    def test_get_help_valid(self, slack_agent_repository, slack_client_class, slack_client, mocker):
        target_url = url_for(endpoint=self.target_endpoint)
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_slash_command_request.team_id)
        payload = deepcopy(self.default_payload)
        payload['command'] = '/strand'
        payload['text'] = 'help'
        mocker.spy(slack_client_class, 'api_call')

        response = self.client.post(path=target_url, headers=self.default_headers, data=urlencode(payload))

        outcome = wait_until(condition=lambda: slack_client_class.api_call.call_count >= 1)
        assert outcome, 'Expected slack_client to have a call'

        assert HTTPStatus.NO_CONTENT == response.status_code
        self.assert_values_in_call_args_list(
            params_to_expecteds=[
                {'method': 'chat.postEphemeral'},  # DM user with help message
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )
