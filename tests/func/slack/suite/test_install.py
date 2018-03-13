import json
import threading

import pytest
from flask import url_for

from tests.func.TestInstallFixtures import TestInstallFixtures
from tests.utils import wait_until, wait_for_extra_threads_to_die, assert_values_in_call_args_list


class TestInstall(TestInstallFixtures):
    """Test the flow for a user installing the Slack application (/install)"""

    target_endpoint = 'configure.installresource'
    default_headers = {'Content-Type': 'application/json'}

    def test_install_new_agent_new_user_with_valid_code(self, slack_oauth_access, client, slack_client_class, mocker):
        target_url = url_for(endpoint=self.target_endpoint)
        f = slack_oauth_access
        payload = {'code': f.code}
        mocker.spy(slack_client_class, 'api_call')

        client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        assert wait_for_extra_threads_to_die(timeout=100), 'Extra threads timed out'
        assert_values_in_call_args_list(
            params_to_expecteds=[
                {'method': 'oauth.access', 'code': f.code},  # Call Slack OAuth
                {'method': 'chat.postMessage'},  # DM user with welcome message
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )
        # assert slack_client_class.api_call.call_args_list[0][1]['code'] == s.code
        # assert that API is hit with a new team (using the seeded slack team id)
        # assert that a new agent is added to DB w/ new team ID
        # assert that new installer is added to DB

    def test_install_existing_agent_new_user_with_valid_code(self):
        # fixtures: seed DB with existing agent, Slack w/ code response

        # hit /install endpoint with a code
        # assert that the slack handshake happens
        # assert that API is NOT hit with a new team (already exists)
        # assert that a new agent is NOT added to DB
        # assert that new installer is added to DB
        pass

    @pytest.mark.skip('TODO (nice-to-have): Don\'t allow users to re-install if they\'re already installed')
    def test_install_existing_agent_existing_user_existing_scope_with_valid_code(self):
        pass

    @pytest.mark.skip('TODO (nice-to-have): Don\'t allow bad code requests to this endpoint')
    def test_install_with_invalid_code(self):
        pass
