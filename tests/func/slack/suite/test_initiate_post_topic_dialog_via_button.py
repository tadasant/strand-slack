import json
from copy import deepcopy
from urllib.parse import urlencode

from flask import url_for

from src.command.model.attachment.attachments import TOPIC_CHANNEL_ACTIONS_ATTACHMENT
from tests.func.slack.TestButton import TestButton
from tests.func.slack.TestInteractiveComponent import TestInteractiveComponent
from tests.utils import wait_until


class TestInitiatePostTopicDialogViaButton(TestButton):
    default_payload = deepcopy(TestInteractiveComponent.default_payload)
    default_payload['callback_id'] = TOPIC_CHANNEL_ACTIONS_ATTACHMENT.callback_id

    def test_valid_post_command(self, slack_client_class, mocker, slack_agent_repository):
        mocker.spy(slack_client_class, 'api_call')
        target_url = url_for(endpoint=self.target_endpoint)
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_interactive_component_request.team.id)

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(self.default_payload)}))

        assert 200 <= response.status_code <= 300
        outcome = wait_until(condition=lambda: slack_client_class.api_call.call_count == 1)
        assert outcome, 'SlackClient api_call was never called'
        self.assert_values_in_call_args_list(
            params_to_expecteds=[
                {
                    'method': 'dialog.open',
                    'trigger_id': self.fake_interactive_component_request.trigger_id
                }
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )
