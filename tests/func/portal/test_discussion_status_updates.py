import json
from collections import namedtuple
from copy import deepcopy
from http.__init__ import HTTPStatus

from flask import url_for

from src.config import config
from tests.common.PrimitiveFaker import PrimitiveFaker
from tests.func.TestFunction import TestFunction

DiscussionStatusRequest = namedtuple('DiscussionStatusRequest',
                                     'slack_channel_id slack_team_id original_poster_slack_user_id')


class TestDiscussionStatusUpdates(TestFunction):
    # For assertions
    fake_discussion_status_request = DiscussionStatusRequest(
        slack_channel_id=str(PrimitiveFaker('bban')),
        slack_team_id=str(PrimitiveFaker('bban')),
        original_poster_slack_user_id=str(PrimitiveFaker('bban'))
    )

    # For setup
    default_payload = {
        'discussion_id': 'doesnt matter',
        'status': 'doesnt matter',
        'slack_channel_id': fake_discussion_status_request.slack_channel_id,
        'slack_team_id': fake_discussion_status_request.slack_team_id,
        'original_poster_slack_user_id': fake_discussion_status_request.original_poster_slack_user_id,
    }
    default_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {config["PORTAL_VERIFICATION_TOKEN"]}'
    }

    def test_post_unauthorized(self, slack_agent_repository, slack_client_class, mocker):
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

    def test_post_valid_stale(self, slack_agent_repository, slack_client_class, mocker):
        pass

    def test_post_valid_closed(self, slack_agent_repository):
        pass
