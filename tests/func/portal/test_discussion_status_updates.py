import json
from collections import namedtuple
from copy import deepcopy
from http.__init__ import HTTPStatus

from flask import url_for

from src.config import config
from tests.common.PrimitiveFaker import PrimitiveFaker
from tests.func.TestFunction import TestFunction
from tests.utils import wait_until

DiscussionStatusRequest = namedtuple('DiscussionStatusRequest', 'slack_channel_id slack_team_id')


class TestDiscussionStatusUpdates(TestFunction):
    # For assertions
    fake_discussion_status_request = DiscussionStatusRequest(
        slack_channel_id=str(PrimitiveFaker('bban')),
        slack_team_id=str(PrimitiveFaker('bban')),
    )

    # For setup
    default_payload = {
        'slack_channel_id': fake_discussion_status_request.slack_channel_id,
        'slack_team_id': fake_discussion_status_request.slack_team_id,
    }
    default_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {config["PORTAL_VERIFICATION_TOKEN"]}'
    }

    def test_post_unauthorized(self):
        headers = deepcopy(self.default_headers)
        del headers['Authorization']
        target_url = url_for(endpoint='portal.stalediscussionstatusresource')

        # Stale endpoint
        response = self.client.post(path=target_url, headers=headers, data=json.dumps(self.default_payload))
        assert response.status_code == HTTPStatus.UNAUTHORIZED

        target_url = url_for(endpoint='portal.closeddiscussionstatusresource')

        # Closed endpoint
        response = self.client.post(path=target_url, headers=headers, data=json.dumps(self.default_payload))
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_post_valid_stale(self, slack_agent_repository, slack_client_class, portal_client, slack_client, mocker):
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_discussion_status_request.slack_team_id)
        discussion_channel_id = self.start_discussion_on_channel(
            slack_team_id=self.fake_discussion_status_request.slack_team_id,
            portal_client=portal_client,
            slack_agent_repository=slack_agent_repository,
            slack_client_class=slack_client_class,
            mocker=mocker
        )
        mocker.spy(slack_client_class, 'api_call')
        mocker.spy(portal_client, 'mutate')
        target_url = url_for(endpoint='portal.stalediscussionstatusresource')
        payload = deepcopy(self.default_payload)
        payload['slack_channel_id'] = discussion_channel_id

        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        def wait_condition():
            return portal_client.mutate.call_count == 1 and slack_client_class.api_call.call_count >= 1

        outcome = wait_until(condition=wait_condition)
        assert outcome, 'Expected portal_client to have 1 call and slack_client to have 1+ calls'

        assert 200 <= response.status_code <= 300
        assert 'markDiscussionAsPendingClosedFromSlack' in portal_client.mutate.call_args_list[0][1][
            'operation_definition']
        assert discussion_channel_id in portal_client.mutate.call_args_list[0][1]['operation_definition']
        self.assert_values_in_call_args_list(
            params_to_expecteds=[
                {'method': 'chat.postMessage'},  # inform participants of pending closed discussion
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )

    def test_post_valid_closed(self, slack_client_class, mocker, slack_agent_repository, portal_client, slack_client):
        self.add_slack_agent_to_repository(slack_agent_repository=slack_agent_repository,
                                           slack_team_id=self.fake_discussion_status_request.slack_team_id)
        discussion_channel_id = self.start_discussion_on_channel(
            slack_team_id=self.fake_discussion_status_request.slack_team_id,
            portal_client=portal_client,
            slack_agent_repository=slack_agent_repository,
            slack_client_class=slack_client_class,
            mocker=mocker
        )
        mocker.spy(slack_client_class, 'api_call')
        target_url = url_for(endpoint='portal.closeddiscussionstatusresource')
        payload = deepcopy(self.default_payload)
        payload['slack_channel_id'] = discussion_channel_id

        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        outcome = wait_until(condition=lambda: slack_client_class.api_call.call_count >= 3)
        assert outcome, 'Expected slack_client to have 3+ calls'

        assert 200 <= response.status_code <= 300
        self.assert_values_in_call_args_list(
            params_to_expecteds=[
                {'method': 'chat.postMessage'},  # inform channel of closed discussion
                {'method': 'channels.archive'},
                {'method': 'chat.update'},  # update the queue message
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )
