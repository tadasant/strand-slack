import json
from http import HTTPStatus
from urllib.parse import urlencode

import factory
import pytest
from flask import url_for

from src.command.messages.initial_onboarding_dm import INITIAL_ONBOARDING_DM
from src.config import config
from tests.factories.slackfactories import InteractiveComponentRequestFactory, ActionFactory, MessageFactory
from tests.utils import wait_until

# TODO clean this up
@pytest.mark.usefixtures('client_class')  # pytest-flask's client_class adds self.client
class TestUpdateDiscussionChannel:
    # For assertions
    fake_interactive_menu_request = InteractiveComponentRequestFactory.create(
        actions=[ActionFactory.build()],
        original_message=factory.SubFactory(MessageFactory)
    )

    # For setup
    target_endpoint = 'slack.interactivecomponentresource'
    default_payload = {
        "type": fake_interactive_menu_request.type,
        "actions": [
            {
                "name": fake_interactive_menu_request.actions[0].name,
                "type": "select",
                "selected_options": [
                    {
                        "value": "C1DFRD2GZ"
                    }
                ]
            }
        ],
        "callback_id": fake_interactive_menu_request.callback_id,
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
        "message_ts": "1517014969.000145",
        "attachment_id": "1",
        "token": config['SLACK_VERIFICATION_TOKEN'],
        "is_app_unfurl": False,
        "original_message": {
            "text": fake_interactive_menu_request.original_message.text,
            "username": "CodeClippy",
            "bot_id": "B8Y9T3Z3J",
            "attachments": [
                {
                    "callback_id": "onboarding_dm",
                    "fallback": "Upgrade your Slack client to use messages like these.",
                    "id": 1,
                    "color": "3AA3E3",
                    "actions": [
                        {
                            "id": "1",
                            "name": "help_channel_list",
                            "text": "What channel should I use for showing help requests?",
                            "type": "select",
                            "data_source": "channels"
                        }
                    ]
                }
            ],
            "type": "message",
            "subtype": "bot_message",
            "ts": "1517014969.000145"
        },
        "response_url": fake_interactive_menu_request.response_url,
        "trigger_id": "304946943568.10642948979.fde99265c25c102dc631e6cd49ac4535"
    }
    default_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    def test_post_valid_unauthenticated_slack(self):
        target_url = url_for(endpoint=self.target_endpoint)
        payload = self.default_payload.copy()
        payload['token'] = 'unverified token'

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(payload)}))
        assert response.json['error'] == 'Invalid slack verification token'

    def test_post_valid_authenticated_slack(self, slack_client_class, portal_client, mocker):
        mocker.spy(slack_client_class, 'api_call')
        mocker.spy(portal_client, 'mutate')
        target_url = url_for(endpoint=self.target_endpoint)
        payload = self.default_payload.copy()
        payload['type'] = 'interactive_message'
        payload['actions'][0]['name'] = INITIAL_ONBOARDING_DM.action_id
        payload['callback_id'] = INITIAL_ONBOARDING_DM.callback_id

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(payload)}))
        assert HTTPStatus.NO_CONTENT == response.status_code
        outcome = wait_until(condition=lambda: portal_client.mutate.call_count == 1)
        assert outcome, 'PortalClient mutate was never called'
        assert 'helpChannelId:' in portal_client.mutate.call_args[1]['operation_definition']
        # TODO if this test hangs a little, requests.post is called (and ignored) in a thread. Should clean up.
