import pytest
from flask import url_for

from tests.func.TestInstallFixtures import TestInstallFixtures


class TestDifferentName(TestInstallFixtures):
    """Test the flow for a user installing the Slack application (/install)"""

    target_endpoint = 'install'

    def test_install_new_agent_new_user_with_valid_code(self, slack_oauth_access_response):
        target_url = url_for(endpoint=self.target_endpoint)
        s = slack_oauth_access_response
        print(s.code)
        # fixtures: seed Slack w/ code response

        # hit /install endpoint with a code
        # assert that the slack handshake happens (the right oa
        # assert that API is hit with a new team (using the seeded slack team id)
        # assert that a new agent is added to DB w/ new team ID
        # assert that new installer is added to DB
        assert True
        pass

    def test_install_existing_agent_new_user_with_valid_code(self):
        # fixtures: seed DB with existing agent, Slack w/ code response

        # hit /install endpoint with a code
        # assert that the slack handshake happens
        # assert that API is NOT hit with a new team (already exists)
        # assert that a new agent is NOT added to DB
        # assert that new installer is added to DB
        pass

    def test_install_existing_agent_existing_user_new_scope_with_valid_code(self):
        # fixtures: seed DB with existing agent, installer; Slack w/ code response

        # hit /install endpoint with a code
        # assert that the slack handshake happens
        # assert that API is NOT hit with a new team (already exists)
        # assert that a new agent is NOT added to DB
        # assert that installer's info is added to DB
        pass

    @pytest.mark.skip('TODO (nice-to-have): Don\'t allow users to re-install if they\'re already installed')
    def test_install_existing_agent_existing_user_existing_scope_with_valid_code(self):
        pass

    @pytest.mark.skip('TODO (nice-to-have): Don\'t allow bad code requests to this endpoint')
    def test_install_with_invalid_code(self):
        pass
