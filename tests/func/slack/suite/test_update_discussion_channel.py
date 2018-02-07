import json
from copy import deepcopy
from http import HTTPStatus
from urllib.parse import urlencode

import factory
from flask import url_for

from src.command.messages.initial_onboarding_dm import INITIAL_ONBOARDING_DM
from src.config import config
from tests.factories.slackfactories import InteractiveComponentRequestFactory, ActionFactory, MessageFactory
from tests.func.slack.TestSlackFunction import TestSlackFunction
from tests.utils import wait_until


class TestUpdateDiscussionChannel(TestSlackFunction):
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
                            "name": "discuss_channel_list",
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
        "trigger_id": "304946943568.10642948979.fde99265c25c102dc631e6cd49ac4535"
    }

    def test_post_valid_unauthenticated_slack(self):
        target_url = url_for(endpoint=self.target_endpoint)
        payload = deepcopy(self.default_payload)
        payload['token'] = 'unverified token'

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(payload)}))
        assert response.json['error'] == 'Invalid slack verification token'

    def test_post_valid_authenticated_slack(self, slack_client_class, portal_client, slack_agent_repository, mocker):
        mocker.spy(slack_client_class, 'api_call')
        mocker.spy(portal_client, 'mutate')
        target_url = url_for(endpoint=self.target_endpoint)
        payload = deepcopy(self.default_payload)
        payload['type'] = 'interactive_message'
        payload['actions'][0]['name'] = INITIAL_ONBOARDING_DM.action_id
        payload['callback_id'] = INITIAL_ONBOARDING_DM.callback_id
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_interactive_component_request.team.id)

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(payload)}))

        def wait_condition():
            return portal_client.mutate.call_count == 1 and slack_client_class.api_call.call_count >= 3

        outcome = wait_until(condition=wait_condition)
        assert outcome, 'Expected portal_client to have a calls and slack_client to have at least 3'

        assert HTTPStatus.NO_CONTENT == response.status_code
        assert 'discussChannelId:' in portal_client.mutate.call_args[1]['operation_definition']
        self.assert_values_in_call_args_list(
            params_to_expecteds=[
                {'method': 'channels.history'},  # validating if the channel is empty
                {'method': 'channels.invite'},  # add bot to channel
                {'method': 'chat.postMessage'},  # introduce channel
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )
        # TODO if this test hangs a little, requests.post is called (and ignored) in a thread. Should clean up w/ mock.
        # TODO this is what is causing an occasional WARNING in pytest
