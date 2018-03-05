import json
from copy import deepcopy
from http import HTTPStatus

from flask import url_for

from tests.func.slack.TestEvent import TestEvent
from tests.utils import wait_until


class TestDeleteTopicChannelMessage(TestEvent):
    def test_post_deletable_message(self, slack_client_class, portal_client, slack_client,
                                    slack_agent_repository, mocker):
        target_url = url_for(endpoint=self.target_endpoint)
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_event_request.team_id)
        topic_channel_id = slack_agent_repository.get_topic_channel_id(slack_team_id=self.fake_event_request.team_id)

        payload = deepcopy(self.default_payload)
        payload['event']['channel'] = topic_channel_id
        mocker.spy(slack_client_class, 'api_call')

        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        outcome = wait_until(condition=lambda: slack_client_class.api_call.call_count >= 2)
        assert outcome, 'Expected slack_client.api_call to be called 2+ times'

        assert HTTPStatus.OK == response.status_code
        self.assert_values_in_call_args_list(
            params_to_expecteds=[
                {'method': 'chat.delete'},  # delete the topic channel message
                {'method': 'chat.postMessage'},  # inform the user s/he can't do that
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )
