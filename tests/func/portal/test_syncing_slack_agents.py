import json
from copy import deepcopy
from http.__init__ import HTTPStatus

import pytest
from flask import url_for

from src.config import config
from src.domain.models.exceptions.RepositoryException import RepositoryException
from tests.common.PrimitiveFaker import PrimitiveFaker
from tests.factories.portalfactories import SlackAgentFactory
from tests.func.TestFunction import TestFunction


class TestSyncingSlackAgents(TestFunction):
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
        'topic_channel_id': fake_slack_agent.topic_channel_id,
        'slack_team': {
            'id': fake_slack_team_id
        },
        'slack_application_installation': {
            'access_token': fake_slack_access_token,
            'installer': {
                'id': fake_installer_id,
            },
            'bot_access_token': fake_slack_bot_access_token,
            'bot_user_id': fake_slack_agent.slack_application_installation.bot_user_id
        },
    }
    default_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {config["PORTAL_VERIFICATION_TOKEN"]}'
    }


class TestPostingSlackAgents(TestSyncingSlackAgents):
    def test_post_unauthorized(self, slack_agent_repository, slack_client_class, mocker):
        target_url = url_for(endpoint=self.target_endpoint)
        headers = deepcopy(self.default_headers)
        del headers['Authorization']

        response = self.client.post(path=target_url, headers=headers, data=json.dumps(self.default_payload))
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    def test_post_valid_installation(self, slack_agent_repository, slack_client_class, mocker):
        with pytest.raises(RepositoryException):
            slack_agent_repository.get_slack_bot_access_token(slack_team_id=self.fake_slack_team_id)

        mocker.spy(slack_client_class, 'api_call')
        mocker.spy(slack_client_class, '__init__')
        target_url = url_for(endpoint=self.target_endpoint)

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=json.dumps(self.default_payload))

        # Some data is returned, bot token is stored in repo, and onboarding DM was called w/ correct token
        data = json.loads(response.data)
        assert data['slack_application_installation']['installer']['id'] == self.fake_installer_id
        assert slack_agent_repository.get_slack_bot_access_token(
            slack_team_id=self.fake_slack_team_id) == self.fake_slack_bot_access_token
        assert slack_client_class.api_call.call_count == 2
        assert slack_client_class.__init__.call_args[1]['token'] == self.fake_slack_bot_access_token

    def test_post_valid_installation_extra_params(self, slack_agent_repository):
        with pytest.raises(RepositoryException):
            slack_agent_repository.get_slack_bot_access_token(slack_team_id=self.fake_slack_team_id)

        target_url = url_for(endpoint=self.target_endpoint)
        payload = deepcopy(self.default_payload)
        payload['group_id'] = str(PrimitiveFaker('bban'))

        response = self.client.post(path=target_url, headers=self.default_headers,
                                    data=json.dumps(self.default_payload))

        data = json.loads(response.data)
        assert data['slack_application_installation']['installer']['id'] == self.fake_installer_id
        assert slack_agent_repository.get_slack_bot_access_token(
            slack_team_id=self.fake_slack_team_id) == self.fake_slack_bot_access_token

    def test_post_invalid_installation(self, slack_agent_repository):
        with pytest.raises(RepositoryException):
            slack_agent_repository.get_slack_bot_access_token(slack_team_id=self.fake_slack_team_id)

        payload = deepcopy(self.default_payload)
        del payload['status']
        target_url = url_for(endpoint=self.target_endpoint)

        response = self.client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))
        assert 'error' in response.json


class TestPuttingSlackAgents(TestSyncingSlackAgents):
    def test_put_valid_existing_installation(self, slack_agent_repository):
        target_url = url_for(endpoint=self.target_endpoint)
        # Adding one so it's pre-existing
        self.client.TestPostingSlackAgents(path=target_url, headers=self.default_headers,
                                           data=json.dumps(self.default_payload))
        assert slack_agent_repository.get_slack_bot_access_token(
            slack_team_id=self.fake_slack_team_id) == self.fake_slack_bot_access_token

        new_fake_access_token = str(PrimitiveFaker('md5'))
        payload = deepcopy(self.default_payload)
        payload['slack_application_installation']['access_token'] = new_fake_access_token
        response = self.client.put(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        data = json.loads(response.data)
        assert data['slack_application_installation']['access_token'] == new_fake_access_token
        assert slack_agent_repository.get_slack_access_token(
            slack_team_id=self.fake_slack_team_id) == new_fake_access_token

    def test_put_valid_new_installation(self, slack_agent_repository):
        with pytest.raises(RepositoryException):
            slack_agent_repository.get_slack_bot_access_token(slack_team_id=self.fake_slack_team_id)

        target_url = url_for(endpoint=self.target_endpoint)

        response = self.client.put(path=target_url, headers=self.default_headers, data=json.dumps(self.default_payload))
        assert 'error' in response.json

    def test_put_invalid_installation(self, slack_agent_repository):
        with pytest.raises(RepositoryException):
            slack_agent_repository.get_slack_bot_access_token(slack_team_id=self.fake_slack_team_id)

        payload = deepcopy(self.default_payload)
        del payload['status']
        target_url = url_for(endpoint=self.target_endpoint)

        response = self.client.put(path=target_url, headers=self.default_headers, data=json.dumps(payload))
        assert 'error' in response.json
