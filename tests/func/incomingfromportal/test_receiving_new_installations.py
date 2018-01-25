import json

import pytest
from flask import url_for, current_app

from tests.common.PrimitiveFaker import PrimitiveFaker


@pytest.mark.usefixtures('client_class')  # pytest-flask's client_class adds self.client
class TestReceivingNewInstallations:
    # For assertions
    bot_access_token = str(PrimitiveFaker('md5'))
    access_token = str(PrimitiveFaker('md5'))
    slack_team_id = str(PrimitiveFaker('ean8'))
    installer_id = str(PrimitiveFaker('ean8'))

    # For setup
    target_endpoint = 'slackapps.slackapplicationinstallation'
    default_payload = {
        'bot_access_token': bot_access_token,
        'access_token': access_token,
        'slack_team_id': slack_team_id,
        'is_active': False,
        'installer_id': installer_id,
    }
    default_headers = {
        'Content-Type': 'application/json',
    }

    def test_receive_valid_installation(self):
        assert len(current_app.slack_client_wrapper.tokens_by_team_id) == 0
        target_url = url_for(endpoint=self.target_endpoint)

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=json.dumps(self.default_payload))

        data = json.loads(response.data)
        assert data['bot_access_token'] == self.bot_access_token
        assert data['access_token'] == self.access_token
        assert len(current_app.slack_client_wrapper.tokens_by_team_id) == 1

    def test_receive_invalid_installation(self):
        num_tokens_to_start = len(current_app.slack_client_wrapper.tokens_by_team_id)
        target_url = url_for(endpoint=self.target_endpoint)
        payload = self.default_payload.copy()
        del payload['installer_id']

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=json.dumps(payload))

        assert response.status_code == 400
        assert len(current_app.slack_client_wrapper.tokens_by_team_id) == num_tokens_to_start
