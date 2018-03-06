import json
from copy import deepcopy
from http import HTTPStatus

from flask import url_for

from tests.func.slack.TestEvent import TestEvent
from tests.testresources.TestSlackClient import SlackRepository
from tests.utils import wait_until


class TestSaveMessageAsTopic(TestEvent):
    def test_post_invalid_reaction(self, slack_client_class, portal_client,
                                   slack_agent_repository, mocker):
        mocker.spy(slack_client_class, 'api_call')
        mocker.spy(portal_client, 'mutate')
        target_url = url_for(endpoint=self.target_endpoint)
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_event_request.team_id)
        self._add_channel_message(channel_id='C9CQUPX42')
        payload = deepcopy(self.default_payload)
        payload['event'] = {'type': 'reaction_added',
                            'user': 'U9D4VV8HG',
                            'item': {'type': 'message',
                                     'channel': 'C9CQUPX42',
                                     'ts': '1520374293.000544'},
                            'reaction': 'brain',
                            'item_user': 'U9D4VV8HG',
                            'event_ts': '1520374298.000104'}
        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        outcome = wait_until(condition=lambda: slack_client_class.api_call.call_count == 0)
        assert outcome, 'Expected slack_client_class.api_call not to be called'

        assert HTTPStatus.OK == response.status_code
        assert not portal_client.mutate.call_args_list, portal_client.mutate.call_args_list

    def test_post_valid_reaction(self, slack_client_class, portal_client,
                                 slack_agent_repository, mocker):
        mocker.spy(slack_client_class, 'api_call')
        mocker.spy(portal_client, 'mutate')
        target_url = url_for(endpoint=self.target_endpoint)
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_event_request.team_id)
        self._add_channel_message(channel_id='C9CQUPX42')
        payload = deepcopy(self.default_payload)
        payload['event'] = {'type': 'reaction_added',
                            'user': 'U9D4VV8HG',
                            'item': {'type': 'message',
                                     'channel': 'C9CQUPX42',
                                     'ts': '1520374293.000544'},
                            'reaction': 'floppy_disk',
                            'item_user': 'U9D4VV8HG',
                            'event_ts': '1520374298.000104'}
        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        outcome = wait_until(condition=lambda: slack_client_class.api_call.call_count >= 1)
        assert outcome, 'Expected slack_client_class.api_call to be called at least once'

        assert HTTPStatus.OK == response.status_code
        assert 'createTopicFromSlack' in portal_client.mutate.call_args_list[0][1]['operation_definition']
        assert 'U9D4VV8HG' in portal_client.mutate.call_args_list[0][1]['operation_definition']

    def _add_channel_message(self, channel_id):
        channel_join_message = {
            "user": "U9DMMTQTY",
            "inviter": "U9DLEEXHU",
            "text": "Check out my very interesting message!!",
            "type": "message",
            "ts": "1519679727.000664"
        }
        SlackRepository['messages_posted_by_channel_id'][channel_id] = [channel_join_message]
