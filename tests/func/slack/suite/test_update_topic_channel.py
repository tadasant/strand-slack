import json
from copy import deepcopy
from http import HTTPStatus
from urllib.parse import urlencode

from flask import url_for

from src.command.model.message.initial_onboarding_dm import INITIAL_ONBOARDING_DM
from tests.func.slack.TestInteractiveComponent import TestInteractiveComponent
from tests.testresources.TestSlackClient import SlackRepository
from tests.utils import wait_until


class TestUpdateDiscussionChannel(TestInteractiveComponent):
    def test_post_valid_authenticated_slack(self, slack_client_class, slack_client, core_api_client,
                                            slack_agent_repository, mocker):
        mocker.spy(slack_client_class, 'api_call')
        mocker.spy(core_api_client, 'mutate')
        target_url = url_for(endpoint=self.target_endpoint)
        payload = deepcopy(self.default_payload)
        payload['type'] = 'interactive_message'
        payload['actions'][0]['name'] = INITIAL_ONBOARDING_DM.action_id
        payload['callback_id'] = INITIAL_ONBOARDING_DM.callback_id
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_interactive_component_request.team.id)
        # Add channel_join message as is usually the case for a new channel
        self._add_channel_join_message(channel_id=payload['actions'][0]['selected_options'][0]['value'],
                                       slack_client=slack_client)

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(payload)}))

        def wait_condition():
            return core_api_client.mutate.call_count == 1 and slack_client_class.api_call.call_count >= 4

        outcome = wait_until(condition=wait_condition)
        assert outcome, 'Expected core_api_client to have a calls and slack_client to have at least 4'

        assert HTTPStatus.NO_CONTENT == response.status_code
        assert 'topicChannelId:' in core_api_client.mutate.call_args[1]['operation_definition']
        self.assert_values_in_call_args_list(
            params_to_expecteds=[
                {'method': 'channels.history'},  # checking channel messages for emptiness validation
                {'method': 'chat.delete'},  # deleting existing channel join message
                {'method': 'channels.invite'},  # add bot to channel
                {'method': 'chat.postMessage'},  # introduce channel
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )
        # TODO if this test hangs a little, requests.post is called (and ignored) in a thread. Should clean up w/ mock.
        # TODO this is what is causing an occasional WARNING in pytest

    def _add_channel_join_message(self, channel_id, slack_client):
        channel_join_message = {
            "user": "U9DMMTQTY",
            "inviter": "U9DLEEXHU",
            "text": "<@U9DMMTQTY> has joined the channel",
            "type": "message",
            "subtype": "channel_join",
            "ts": "1519679727.000664"
        }
        SlackRepository['messages_posted_by_channel_id'][channel_id] = [channel_join_message]
