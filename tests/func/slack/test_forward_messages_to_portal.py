import json
from copy import deepcopy
from http import HTTPStatus

from flask import url_for

from src.config import config
from tests.common.PrimitiveFaker import PrimitiveFaker
from tests.factories.slackfactories import EventRequestFactory
from tests.func.slack.TestSlackFunction import TestSlackFunction
from tests.testresources.TestSlackClient import SlackRepository
from tests.utils import wait_until


class TestForwardMessagesToPortal(TestSlackFunction):
    # For assertions
    fake_event_request = EventRequestFactory.create(type='event_callback', challenge=None)
    fake_event_request.event.type = 'message'

    # For setup
    target_endpoint = 'slack.eventresource'
    default_payload = {
        'token': config['SLACK_VERIFICATION_TOKEN'],
        'team_id': fake_event_request.team_id,
        'api_app_id': 'A8YTKNNMQ',
        'event': {
            'type': fake_event_request.event.type,
            'user': fake_event_request.event.user,
            'text': fake_event_request.event.text,
            'ts': fake_event_request.event.ts,
            'channel': fake_event_request.event.channel,
            'event_ts': '1517591017.000275'
        },
        'type': fake_event_request.type,
        'event_id': 'Ev92G3E5UH',
        'event_time': 1517591017,
        'authed_users': [fake_event_request.event.user]
    }
    default_headers = {
        'Content-Type': 'application/json',
    }

    def test_post_valid_unauthenticated_slack(self):
        target_url = url_for(endpoint=self.target_endpoint)
        payload = deepcopy(self.default_payload)
        payload['token'] = 'unverified token'

        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))
        assert response.json == {}

    def test_post_valid_message_authenticated_slack(self, slack_client_class, portal_client, slack_client,
                                                    slack_agent_repository, mocker):
        target_url = url_for(endpoint=self.target_endpoint)
        discussion_channel_id = self._start_discussion_on_channel(portal_client=portal_client,
                                                                  slack_agent_repository=slack_agent_repository,
                                                                  slack_client_class=slack_client_class,
                                                                  mocker=mocker)
        payload = deepcopy(self.default_payload)
        payload['event']['channel'] = discussion_channel_id
        self._queue_portal_message_creation(portal_client=portal_client)
        mocker.spy(portal_client, 'mutate')

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=json.dumps(payload))

        outcome = wait_until(condition=lambda: portal_client.mutate.call_count == 1, timeout=1000)
        assert outcome, 'Expected portal_client.mutate be called'

        assert HTTPStatus.OK == response.status_code
        assert 'createMessageFromSlack' in portal_client.mutate.call_args_list[0][1]['operation_definition']
        assert discussion_channel_id in portal_client.mutate.call_args_list[0][1]['operation_definition']

    def test_post_valid_reply_authenticated_slack(self):
        pass

    def test_post_message_irrelevant_channel(self):
        pass

    def _start_discussion_on_channel(self, portal_client, slack_agent_repository, slack_client_class, mocker):
        self.start_discussion(slack_agent_repository=slack_agent_repository,
                              slack_team_id=self.fake_event_request.team_id,
                              slack_client_class=slack_client_class,
                              portal_client=portal_client,
                              mocker=mocker)
        assert 1 == len(SlackRepository['created_channels_by_id'].items())
        # return created channel id
        return next(iter(SlackRepository['created_channels_by_id'].values()))['id']

    def _queue_portal_message_creation(self, portal_client):
        portal_client.set_next_response({
            'data': {
                'createMessageFromSlack': {
                    'message': {
                        'id': str(PrimitiveFaker('random_int')),
                    },
                }
            }
        })
