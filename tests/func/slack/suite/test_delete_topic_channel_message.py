import json
from copy import deepcopy
from http import HTTPStatus

from flask import url_for

from tests.func.slack.TestSlackFunction import TestSlackFunction
from tests.utils import wait_until


class TestDeleteTopicChannelMessage(TestSlackFunction):
    def test_post_valid_unauthenticated_slack(self):
        target_url = url_for(endpoint=self.target_endpoint)
        payload = deepcopy(self.default_payload)
        payload['token'] = 'unverified token'

        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))
        assert response.json == {}

    def test_post_valid_message_authenticated_slack(self, slack_client_class, portal_client, slack_client,
                                                    slack_agent_repository, mocker):
        target_url = url_for(endpoint=self.target_endpoint)
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_event_request.team_id)
        discussion_channel_id = self.start_discussion_on_channel(slack_team_id=self.fake_event_request.team_id,
                                                                 portal_client=portal_client,
                                                                 slack_agent_repository=slack_agent_repository,
                                                                 slack_client_class=slack_client_class,
                                                                 mocker=mocker)
        payload = deepcopy(self.default_payload)
        payload['event']['channel'] = discussion_channel_id
        self._queue_portal_message_creation(portal_client=portal_client)
        mocker.spy(portal_client, 'mutate')

        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        outcome = wait_until(condition=lambda: portal_client.mutate.call_count == 1)
        assert outcome, 'Expected portal_client.mutate be called'

        assert HTTPStatus.OK == response.status_code
        assert 'createMessageFromSlack' in portal_client.mutate.call_args_list[0][1]['operation_definition']
        assert discussion_channel_id in portal_client.mutate.call_args_list[0][1]['operation_definition']
