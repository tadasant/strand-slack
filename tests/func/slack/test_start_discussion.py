import json
from http import HTTPStatus
from urllib.parse import urlencode

import pytest
from flask import url_for

from src.command.messages.initial_onboarding_dm import INITIAL_ONBOARDING_DM
from src.config import config
from tests.factories.slackfactories import InteractiveComponentRequestFactory
from tests.utils import wait_until


@pytest.mark.usefixtures('client_class')  # pytest-flask's client_class adds self.client
class TestStartDiscussion:
    # For assertions
    fake_interactive_menu_request = InteractiveComponentRequestFactory.create()

    # For setup
    target_endpoint = 'slack.interactivecomponentresource'
    default_payload = {
        "type": fake_interactive_menu_request.type,
        "callback_id": fake_interactive_menu_request.callback_id,
        "sub"
        "team": {
            "id": fake_interactive_menu_request.team.id,
            "domain": "solutionloft"
        },
        "channel": {
            "id": "D8YS0A9D1",
            "name": "directmessage"
        },
        "user": {
            "id": "U7JH1V2PP",
            "name": "tadas"
        },
        "action_ts": "1517014983.191305",
        "token": 'unverifiedtoken',
        # "trigger_id": fake_interactive_menu_request.trigger_id
    }
    default_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    def test_post_valid_unauthenticated_slack(self):
        target_url = url_for(endpoint=self.target_endpoint)
        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(self.default_payload)}))
        assert 'error' in response.json

    def test_post_valid_authenticated_slack(self, slack_client_class, portal_client, mocker):
        mocker.spy(slack_client_class, 'api_call')
        mocker.spy(portal_client, 'mutate')
        target_url = url_for(endpoint=self.target_endpoint)
        payload = self.default_payload.copy()
        payload['type'] = 'interactive_message'
        payload['actions'][0]['name'] = INITIAL_ONBOARDING_DM.action_id
        payload['callback_id'] = INITIAL_ONBOARDING_DM.callback_id
        payload['token'] = config['SLACK_VERIFICATION_TOKEN']

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(payload)}))
        assert HTTPStatus.NO_CONTENT == response.status_code
        outcome = wait_until(condition=lambda: portal_client.mutate.call_count == 1)
        assert outcome, 'PortalClient mutate was never called'
        assert 'helpChannelId:' in portal_client.mutate.call_args[1]['operation_definition']
