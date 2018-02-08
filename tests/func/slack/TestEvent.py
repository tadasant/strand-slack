import json
from copy import deepcopy

from flask import url_for

from src.config import config
from tests.factories.slackfactories import EventRequestFactory
from tests.func.slack.TestSlackFunction import TestSlackFunction


class TestEvent(TestSlackFunction):
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
