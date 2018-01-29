import json
from http import HTTPStatus
from urllib.parse import urlencode

import factory
import pytest
from flask import url_for

from src.command.messages.initial_onboarding_dm import INITIAL_ONBOARDING_DM
from src.command.messages.post_topic_dialog import POST_TOPIC_DIALOG
from src.config import config
from tests.factories.slackfactories import InteractiveComponentRequestFactory, SubmissionFactory
from tests.utils import wait_until


@pytest.mark.usefixtures('client_class')  # pytest-flask's client_class adds self.client
class TestStartDiscussion:
    # For assertions
    fake_interactive_component_request = InteractiveComponentRequestFactory.create(
        submission=factory.SubFactory(SubmissionFactory)
    )

    # For setup
    target_endpoint = 'slack.interactivecomponentresource'
    default_payload = {
        "type": fake_interactive_component_request.type,
        "callback_id": fake_interactive_component_request.callback_id,
        "submission": {
            "title": fake_interactive_component_request.submission.title,
            "description": fake_interactive_component_request.submission.description,
            "tags": fake_interactive_component_request.submission.tags
        },
        "team": {
            "id": fake_interactive_component_request.team.id,
            "domain": "solutionloft"
        },
        "channel": {
            "id": "D8YS0A9D1",
            "name": "directmessage"
        },
        "user": {
            "id": fake_interactive_component_request.user.id,
            "name": "tadas"
        },
        "action_ts": "1517014983.191305",
        "token": config['SLACK_VERIFICATION_TOKEN'],
    }
    default_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    def test_post_valid_unauthenticated_slack(self):
        target_url = url_for(endpoint=self.target_endpoint)
        payload = self.default_payload.copy()
        payload['token'] = 'unverified-token'
        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(payload)}))
        assert response.json['error'] == 'Invalid slack verification token'

    def test_post_valid_authenticated_slack(self):
        target_url = url_for(endpoint=self.target_endpoint)
        payload = self.default_payload.copy()
        payload['type'] = 'dialog_submission'
        payload['callback_id'] = POST_TOPIC_DIALOG.callback_id

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=urlencode({'payload': json.dumps(payload)}))
        assert HTTPStatus.OK == response.status_code
