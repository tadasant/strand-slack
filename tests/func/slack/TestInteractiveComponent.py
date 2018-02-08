import json
from copy import deepcopy
from urllib.parse import urlencode

import factory
from flask import url_for

from src.config import config
from tests.factories.slackfactories import InteractiveComponentRequestFactory, ActionFactory, MessageFactory
from tests.func.slack.TestSlackFunction import TestSlackFunction


class TestInteractiveComponent(TestSlackFunction):
    # For assertions
    fake_interactive_component_request = InteractiveComponentRequestFactory.create(
        actions=[ActionFactory.build()],
        original_message=factory.SubFactory(MessageFactory)
    )

    # For setup
    target_endpoint = 'slack.interactivecomponentresource'
    default_payload = {
        "type": fake_interactive_component_request.type,
        "actions": [
            {
                "name": fake_interactive_component_request.actions[0].name,
                "type": "select",
                "selected_options": [
                    {
                        "value": "C1DFRD2GZ"
                    }
                ]
            }
        ],
        "callback_id": fake_interactive_component_request.callback_id,
        "team": {
            "id": fake_interactive_component_request.team.id,
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
            "text": fake_interactive_component_request.original_message.text,
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
                            "name": "topic_channel_list",
                            "text": "What channel should I use for showing discussion topic requests?",
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
        "response_url": fake_interactive_component_request.response_url,
        "trigger_id": fake_interactive_component_request.trigger_id
    }

    def test_post_valid_unauthenticated_slack(self):
        target_url = url_for(endpoint=self.target_endpoint)
        payload = deepcopy(self.default_payload)
        payload['token'] = 'unverified token'

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(payload)}))
        assert response.json['error'] == 'Invalid slack verification token'
