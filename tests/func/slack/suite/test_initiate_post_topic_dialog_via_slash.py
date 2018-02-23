from copy import deepcopy
from http import HTTPStatus
from urllib.parse import urlencode

from flask import url_for

from tests.func.slack.TestSlashCommand import TestSlashCommand
from tests.utils import wait_until


class TestInitiatePostTopicDialogViaSlash(TestSlashCommand):
    default_payload = deepcopy(TestSlashCommand.default_payload)
    default_payload['command'] = '/strand'

    def test_valid_post_command(self, slack_client_class, mocker, slack_agent_repository):
        mocker.spy(slack_client_class, 'api_call')
        target_url = url_for(endpoint=self.target_endpoint)
        payload = deepcopy(self.default_payload)
        payload['text'] = 'post'
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
