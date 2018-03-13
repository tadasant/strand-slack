import json
from http import HTTPStatus

import pytest
from flask import url_for

from src.config import config
from src.models.domain.User import User
from tests.func.slack.TestHelpDmFixtures import TestHelpDmFixtures
from tests.utils.asserting import wait_for_extra_threads_to_die


@pytest.mark.usefixtures('app')
class TestHelpDm(TestHelpDmFixtures):
    """Test the flow for a user installing the Slack application (/install)"""

    target_endpoint = 'slack.eventresource'
    default_headers = {'Content-Type': 'application/json'}

    def test_help_dm_installed_user(self, installed_user: User, slack_client_class, slack_event_request_factory,
                                    baseline_thread_count, client, mocker):
        """Ensure we send a help message to users who have the app installed when they DM 'help'"""
        target_url = url_for(endpoint=self.target_endpoint)
        fake_slack_event_request = slack_event_request_factory()
        fake_slack_event_request.token = config['SLACK_VERIFICATION_TOKENS'][0]
        fake_slack_event_request.event.user = installed_user.slack_user_id
        fake_slack_event_request.team_id = installed_user.agent_slack_team_id
        payload = json.loads(fake_slack_event_request.to_json())
        mocker.spy(slack_client_class, 'api_call')

        response = client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))
        assert wait_for_extra_threads_to_die(baseline_count=baseline_thread_count), 'Extra threads timed out'
        assert HTTPStatus.OK == response.status_code

        assert slack_client_class.api_call.call_args[0]['method'] == 'chat.postMessage'
        assert 'installing the app' not in slack_client_class.api_call.call_args[0]['text']

    def test_nonhelp_dm_installed_user(self, installed_user, client, slack_client_class, strand_api_client,
                                       db_session, mocker):
        """Ensure we don't send a help message in 'non-help' DMs"""
        pass

    def test_help_dm_new_user(self, client, slack_client_class, strand_api_client, db_session, mocker):
        """All users who do not have the app installed should recieve a help to install DM response"""
        pass
