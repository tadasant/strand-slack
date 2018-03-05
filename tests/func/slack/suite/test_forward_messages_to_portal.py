import json
from copy import deepcopy
from http import HTTPStatus

from flask import url_for

from tests.common.PrimitiveFaker import PrimitiveFaker
from tests.func.slack.TestEvent import TestEvent
from tests.utils import wait_until


class TestForwardMessagesToPortal(TestEvent):
    def test_post_valid_message_authenticated_slack(self, slack_client_class, portal_client, slack_client,
                                                    slack_agent_repository, mocker):
        target_url = url_for(endpoint=self.target_endpoint)
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_event_request.team_id)
        discussion_channel_id = self.start_discussion_on_channel(slack_team_id=self.fake_event_request.team_id,
                                                                 portal_client=portal_client,
                                                                 slack_agent_repository=slack_agent_repository,
                                                                 slack_client_class=slack_client_class,
                                                                 mocker=mocker)
        payload = deepcopy(self.default_payload)
        payload['event']['channel'] = discussion_channel_id
        print(discussion_channel_id)
        self._queue_portal_message_creation(portal_client=portal_client)
        mocker.spy(portal_client, 'mutate')

        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        outcome = wait_until(condition=lambda: portal_client.mutate.call_count == 1)
        assert outcome, 'Expected portal_client.mutate be called'

        assert HTTPStatus.OK == response.status_code
        assert 'createMessageFromSlack' in portal_client.mutate.call_args_list[0][1]['operation_definition']
        assert discussion_channel_id in portal_client.mutate.call_args_list[0][1]['operation_definition']

    def test_post_valid_message_new_user_authenticated_slack(self, slack_client_class, portal_client, slack_client,
                                                             slack_agent_repository, mocker):
        target_url = url_for(endpoint=self.target_endpoint)
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_event_request.team_id)
        discussion_channel_id = self.start_discussion_on_channel(slack_team_id=self.fake_event_request.team_id,
                                                                 portal_client=portal_client,
                                                                 slack_agent_repository=slack_agent_repository,
                                                                 slack_client_class=slack_client_class,
                                                                 mocker=mocker)
        payload = deepcopy(self.default_payload)
        payload['event']['channel'] = discussion_channel_id
        portal_client.set_next_response(None)  # To raise error on attempt w/out user
        self._queue_portal_message_and_user_creation(portal_client=portal_client)
        mocker.spy(portal_client, 'mutate')

        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        outcome = wait_until(condition=lambda: portal_client.mutate.call_count == 2)
        assert outcome, 'Expected portal_client.mutate be called twice'

        assert HTTPStatus.OK == response.status_code
        assert 'createMessageFromSlack' in portal_client.mutate.call_args_list[0][1]['operation_definition']
        assert discussion_channel_id in portal_client.mutate.call_args_list[0][1]['operation_definition']
        assert 'createUserAndMessageFromSlack' in portal_client.mutate.call_args_list[1][1]['operation_definition']
        assert discussion_channel_id in portal_client.mutate.call_args_list[1][1]['operation_definition']

    def test_post_valid_reply_authenticated_slack(self, slack_client_class, portal_client, slack_client,
                                                  slack_agent_repository, mocker):
        target_url = url_for(endpoint=self.target_endpoint)
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_event_request.team_id)
        discussion_channel_id = self.start_discussion_on_channel(slack_team_id=self.fake_event_request.team_id,
                                                                 portal_client=portal_client,
                                                                 slack_agent_repository=slack_agent_repository,
                                                                 slack_client_class=slack_client_class,
                                                                 mocker=mocker)
        payload = deepcopy(self.default_payload)
        payload['event']['channel'] = discussion_channel_id
        payload['event']['thread_ts'] = str(PrimitiveFaker('msisdn'))
        self._queue_portal_message_creation(portal_client=portal_client)
        mocker.spy(portal_client, 'mutate')

        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        outcome = wait_until(condition=lambda: portal_client.mutate.call_count == 1)
        assert outcome, 'Expected portal_client.mutate be called'

        assert HTTPStatus.OK == response.status_code
        assert 'createReplyFromSlack' in portal_client.mutate.call_args_list[0][1]['operation_definition']
        assert discussion_channel_id in portal_client.mutate.call_args_list[0][1]['operation_definition']

    def test_post_valid_reply_new_user_authenticated_slack(self, slack_client_class, portal_client, slack_client,
                                                           slack_agent_repository, mocker):
        target_url = url_for(endpoint=self.target_endpoint)
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_event_request.team_id)
        discussion_channel_id = self.start_discussion_on_channel(slack_team_id=self.fake_event_request.team_id,
                                                                 portal_client=portal_client,
                                                                 slack_agent_repository=slack_agent_repository,
                                                                 slack_client_class=slack_client_class,
                                                                 mocker=mocker)
        payload = deepcopy(self.default_payload)
        payload['event']['channel'] = discussion_channel_id
        payload['event']['thread_ts'] = str(PrimitiveFaker('msisdn'))
        portal_client.set_next_response(None)  # To raise error on attempt w/out user
        self._queue_portal_reply_and_user_creation(portal_client=portal_client)
        mocker.spy(portal_client, 'mutate')

        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        outcome = wait_until(condition=lambda: portal_client.mutate.call_count == 2)
        assert outcome, 'Expected portal_client.mutate be called twice'

        assert HTTPStatus.OK == response.status_code
        assert 'createReplyFromSlack' in portal_client.mutate.call_args_list[0][1]['operation_definition']
        assert discussion_channel_id in portal_client.mutate.call_args_list[0][1]['operation_definition']
        assert 'createUserAndReplyFromSlack' in portal_client.mutate.call_args_list[1][1]['operation_definition']
        assert discussion_channel_id in portal_client.mutate.call_args_list[1][1]['operation_definition']

    def test_post_valid_message_with_file_authenticated_slack(self, slack_client_class, portal_client, slack_client,
                                                              slack_agent_repository, mocker):
        target_url = url_for(endpoint=self.target_endpoint)
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_event_request.team_id)
        discussion_channel_id = self.start_discussion_on_channel(slack_team_id=self.fake_event_request.team_id,
                                                                 portal_client=portal_client,
                                                                 slack_agent_repository=slack_agent_repository,
                                                                 slack_client_class=slack_client_class,
                                                                 mocker=mocker)
        payload = deepcopy(self.default_payload)
        payload['event']['channel'] = discussion_channel_id
        payload['event']['subtype'] = 'file_share'
        payload['event']['file'] = {
            'id': self.fake_event_request.event.file.id,
            'public_url_shared': False,
        }
        self._queue_portal_message_creation(portal_client=portal_client)
        mocker.spy(portal_client, 'mutate')
        mocker.spy(slack_client_class, 'api_call')

        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        outcome = wait_until(condition=lambda: portal_client.mutate.call_count == 1)
        assert outcome, 'Expected portal_client.mutate be called'

        assert HTTPStatus.OK == response.status_code
        assert 'createMessageFromSlack' in portal_client.mutate.call_args_list[0][1]['operation_definition']
        assert discussion_channel_id in portal_client.mutate.call_args_list[0][1]['operation_definition']
        self.assert_values_in_call_args_list(
            params_to_expecteds=[
                {
                    'method': 'files.sharedPublicURL',
                    'file': self.fake_event_request.event.file.id
                }
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )

    def test_post_message_irrelevant_channel(self, portal_client, mocker):
        target_url = url_for(endpoint=self.target_endpoint)
        payload = deepcopy(self.default_payload)
        self._queue_portal_message_creation(portal_client=portal_client)
        mocker.spy(portal_client, 'mutate')

        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        outcome = wait_until(condition=lambda: portal_client.mutate.call_count >= 1, timeout=1)
        assert not outcome, 'Expected portal_client.mutate not to be called'

        assert HTTPStatus.OK == response.status_code

    def _queue_portal_message_creation(self, portal_client):
        portal_client.set_next_response({
            'data': {
                'createMessageFromSlack': {
                    'message': {
                        'id': str(PrimitiveFaker('random_int')),
                    },
                }
            }
        })

    def _queue_portal_message_and_user_creation(self, portal_client):
        portal_client.set_next_response({
            'data': {
                'createUserAndMessageFromSlack': {
                    'message': {
                        'id': str(PrimitiveFaker('random_int')),
                    },
                }
            }
        })

    def _queue_portal_reply_and_user_creation(self, portal_client):
        portal_client.set_next_response({
            'data': {
                'createUserAndReplyFromSlack': {
                    'reply': {
                        'id': str(PrimitiveFaker('random_int')),
                    },
                }
            }
        })
