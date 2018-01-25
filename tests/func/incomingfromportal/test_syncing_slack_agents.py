import json

import pytest
from flask import url_for

from src.domain.models.exceptions.RepositoryException import RepositoryException
from tests.factories import SlackAgentFactory


@pytest.mark.usefixtures('client_class')  # pytest-flask's client_class adds self.client
class TestSyncingSlackAgents:
    # For assertions
    fake_slack_agent = SlackAgentFactory.build()
    fake_slack_team_id = fake_slack_agent.slack_team.id
    fake_slack_access_token = fake_slack_agent.slack_application_installation.access_token
    fake_slack_bot_access_token = fake_slack_agent.slack_application_installation.bot_access_token
    fake_installer_id = fake_slack_agent.slack_application_installation.installer.id

    # For setup
    target_endpoint = 'portal.slackagentresource'
    default_payload = {
        'status': fake_slack_agent.status,
        'help_channel_id': fake_slack_agent.help_channel_id,
        'slack_team': {
            'id': fake_slack_team_id
        },
        'slack_application_installation': {
            'access_token': fake_slack_access_token,
            'installer': {
                'id': fake_installer_id,
            },
            'bot_access_token': fake_slack_bot_access_token
        },
    }
    default_headers = {
        'Content-Type': 'application/json',
    }


class TestPostingSlackAgents(TestSyncingSlackAgents):
    def test_post_valid_installation(self, slack_agent_repository):
        with pytest.raises(RepositoryException):
            slack_agent_repository.get_slack_bot_access_token(slack_team_id=self.fake_slack_team_id)

        target_url = url_for(endpoint=self.target_endpoint)

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=json.dumps(self.default_payload))

        data = json.loads(response.data)
        assert data['slack_application_installation']['installer']['id'] == self.fake_installer_id
        assert slack_agent_repository.get_slack_bot_access_token(
            slack_team_id=self.fake_slack_team_id) == self.fake_slack_bot_access_token

    # def test_post_invalid_installation(self):
    #     with pytest.raises(RepositoryException):
    #         slack_agent_repository.get_slack_bot_access_token(slack_team_id=self.fake_slack_team_id)
    #
    #     target_url = url_for(endpoint=self.target_endpoint)
    #
    #     response = self.client.post(path=target_url, headers=self.default_headers,
    #                                 data=json.dumps(self.default_payload))
    #
    #     data = json.loads(response.data)
    #     assert data['slack_application_installation']['installer']['id'] == self.fake_installer_id
    #     assert slack_agent_repository.get_slack_bot_access_token(
    #         slack_team_id=self.fake_slack_team_id) == self.fake_slack_bot_access_token

    # def test_receive_invalid_installation(self):
    #     num_installations_to_start = len(current_app.slack_client_wrapper.installations_by_team_id)
    #     target_url = url_for(endpoint=self.target_endpoint)
    #     payload = self.default_payload.copy()
    #     del payload['installer']
    #
    #     response = self.client.post(path=target_url, headers=self.default_headers,
    #                                 data=json.dumps(payload))
    #
    #     assert response.status_code == 400
    #     assert len(current_app.slack_client_wrapper.installations_by_team_id) == num_installations_to_start
