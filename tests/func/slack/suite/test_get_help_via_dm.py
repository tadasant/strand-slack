import json
from copy import deepcopy
from http import HTTPStatus

from flask import url_for

from tests.func.slack.TestEvent import TestEvent
from tests.utils import wait_until


class TestGetHelpViaDM(TestEvent):
    def test_get_help_invalid_channel(self, slack_agent_repository, slack_client_class, slack_client, mocker):
        mocker.spy(slack_client_class, 'api_call')

        target_url = url_for(endpoint=self.target_endpoint)
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_event_request.team_id)

        payload = deepcopy(self.default_payload)
        payload['event']['text'] = 'help'
        payload['event']['channel'] = 'C123ABC'

        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        outcome = wait_until(condition=lambda: slack_client_class.api_call.call_count == 0)
        assert outcome, 'Expected slack_client to have a call'

        assert HTTPStatus.OK == response.status_code
        self.assert_value_in_call_args_list({'method': 'chat.postEphemeral'},
                                            call_args_list=slack_client_class.api_call.call_args_list,
                                            expect_to_succeed=False)

    def test_get_help_valid(self, slack_agent_repository, slack_client_class, slack_client, mocker):
        mocker.spy(slack_client_class, 'api_call')

        target_url = url_for(endpoint=self.target_endpoint)
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_event_request.team_id)

        payload = deepcopy(self.default_payload)
        payload['event']['text'] = 'help'
        payload['event']['channel'] = 'D123ABC'

        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        outcome = wait_until(condition=lambda: slack_client_class.api_call.call_count == 1)
        assert outcome, 'Expected slack_client to have a call'

        assert HTTPStatus.OK == response.status_code
        self.assert_values_in_call_args_list(
            params_to_expecteds=[
                {'method': 'chat.postEphemeral'},  # DM user with help message
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )
