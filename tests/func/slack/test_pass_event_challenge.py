import json
from http import HTTPStatus

from flask import url_for

from src.config import config
from tests.factories.slackfactories import EventRequestFactory
from tests.func.slack.TestSlackFunction import TestSlackFunction


class TestPassSlackEventChallenge(TestSlackFunction):
    # For assertions
    fake_event_request = EventRequestFactory.create(type='url_verification')
    fake_challenge_token = fake_event_request.challenge

    # For setup
    target_endpoint = 'slack.eventresource'
    default_payload = {
        "type": fake_event_request.type,
        "token": config['SLACK_VERIFICATION_TOKEN'],
        "challenge": fake_challenge_token
    }
    default_headers = {
        'Content-Type': 'application/json',
    }

    def test_post_valid_unauthenticated_slack(self):
        target_url = url_for(endpoint=self.target_endpoint)
        payload = self.default_payload.copy()
        payload['token'] = 'unverified token'

        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))
        assert response.json['error'] == 'Invalid slack verification token'

    def test_post_valid_authenticated_slack(self, slack_client_class, portal_client, mocker):
        mocker.spy(slack_client_class, 'api_call')
        mocker.spy(portal_client, 'mutate')
        target_url = url_for(endpoint=self.target_endpoint)

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=json.dumps(self.default_payload))

        assert HTTPStatus.OK == response.status_code
        assert response.json['challenge'] == self.fake_challenge_token
