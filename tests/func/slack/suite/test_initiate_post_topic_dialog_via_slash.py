from copy import deepcopy
from http import HTTPStatus
from urllib.parse import urlencode

from flask import url_for

from src.command.model.message.post_topic_dialog import POST_TOPIC_DIALOG, POST_TOPIC_DIALOG_WITH_CHANNEL_OPTION
from tests.func.slack.TestSlashCommand import TestSlashCommand
from tests.utils import wait_until


class TestInitiatePostTopicDialogViaSlash(TestSlashCommand):
    default_payload = deepcopy(TestSlashCommand.default_payload)
    default_payload['command'] = '/strand'

    def validate_post_command(self, slack_client_class, mocker, slack_agent_repository, channel_id, dialog):
        mocker.spy(slack_client_class, 'api_call')
        target_url = url_for(endpoint=self.target_endpoint)
        payload = deepcopy(self.default_payload)
        payload['text'] = 'post'
        payload['channel_id'] = channel_id
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_slash_command_request.team_id)

        response = self.client.post(path=target_url, headers=self.default_headers, data=urlencode(payload))

        assert HTTPStatus.NO_CONTENT == response.status_code
        outcome = wait_until(condition=lambda: slack_client_class.api_call.call_count == 1)
        assert outcome, 'SlackClient api_call was never called'
        self.assert_values_in_call_args_list(
            params_to_expecteds=[
                {
                    'method': 'dialog.open',
                    'trigger_id': self.fake_slash_command_request.trigger_id,
                    'dialog': dialog
                }
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )

    def test_valid_post_command_without_channel_option(self, slack_client_class, mocker, slack_agent_repository):
        self.validate_post_command(slack_client_class, mocker, slack_agent_repository, 'D0G9QPY56',
                                   POST_TOPIC_DIALOG.value)

    def test_valid_post_command_with_channel_option(self, slack_client_class, mocker, slack_agent_repository):
        self.validate_post_command(slack_client_class, mocker, slack_agent_repository, 'C0G9QPY56',
                                   POST_TOPIC_DIALOG_WITH_CHANNEL_OPTION.value)
