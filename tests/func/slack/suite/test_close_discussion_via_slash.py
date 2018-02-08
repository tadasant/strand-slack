from copy import deepcopy
from http import HTTPStatus
from urllib.parse import urlencode

from flask import url_for

from tests.common.PrimitiveFaker import PrimitiveFaker
from tests.func.slack.TestSlashCommand import TestSlashCommand
from tests.utils import wait_until


class TestCloseDiscussionViaSlash(TestSlashCommand):
    def test_close_valid(self, portal_client, slack_agent_repository, slack_client_class, slack_client, mocker):
        target_url = url_for(endpoint=self.target_endpoint)
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_slash_command_request.team_id)
        discussion_channel_id = self.start_discussion_on_channel(slack_team_id=self.fake_slash_command_request.team_id,
                                                                 portal_client=portal_client,
                                                                 slack_agent_repository=slack_agent_repository,
                                                                 slack_client_class=slack_client_class,
                                                                 mocker=mocker)
        self._queue_portal_close_discussion(portal_client=portal_client, discussion_id=str(PrimitiveFaker('bban')))
        payload = deepcopy(self.default_payload)
        payload['command'] = '/codeclippy'
        payload['text'] = 'close'
        payload['channel_id'] = discussion_channel_id
        mocker.spy(portal_client, 'mutate')
        mocker.spy(slack_client_class, 'api_call')

        response = self.client.post(path=target_url, headers=self.default_headers, data=urlencode(payload))

        def wait_condition():
            return portal_client.mutate.call_count == 1 and slack_client_class.api_call.call_count >= 6

        outcome = wait_until(condition=wait_condition)
        assert outcome, 'Expected portal_client to have 1 calls, and slack_client to have 6+'

        assert HTTPStatus.NO_CONTENT == response.status_code
        assert 'closeDiscussionFromSlack' in portal_client.mutate.call_args_list[0][1]['operation_definition']
        assert discussion_channel_id in portal_client.mutate.call_args_list[0][1]['operation_definition']
        self.assert_values_in_call_args_list(
            params_to_expecteds=[
                {'method': 'chat.postMessage'},  # inform channel of closed discussion
                {'method': 'channels.archive'},
                {'method': 'chat.update'},  # update the queue message
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )

    def _queue_portal_close_discussion(self, portal_client, discussion_id):
        portal_client.set_next_response({
            'data': {
                'closeDiscussionFromSlack': {
                    'discussion': {
                        'id': discussion_id,
                    },
                }
            }
        })
