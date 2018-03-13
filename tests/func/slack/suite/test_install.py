import json

import pytest
from flask import url_for

from src.models.domain.Agent import Agent
from src.models.domain.Installation import Installation
from src.models.domain.User import User
from tests.func.TestInstallFixtures import TestInstallFixtures
from tests.utils import wait_for_extra_threads_to_die, assert_values_in_call_args_list


class TestInstall(TestInstallFixtures):
    """Test the flow for a user installing the Slack application (/install)"""

    target_endpoint = 'configure.installresource'
    default_headers = {'Content-Type': 'application/json'}

    def test_install_new_agent_new_user(self, slack_oauth_access, client, slack_client_class, strand_api_client,
                                        db_session, mocker, baseline_thread_count):
        """
            GIVEN: new agent, new user
            OUTPUT: new Agent, new User, new Installation, new StrandTeam, new StrandUser
        """
        # `slack_oauth_access` sets up state
        target_url = url_for(endpoint=self.target_endpoint)
        f = slack_oauth_access  # faked data
        payload = {'code': f.code}
        mocker.spy(slack_client_class, 'api_call')
        mocker.spy(strand_api_client, 'mutate')

        client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        assert wait_for_extra_threads_to_die(baseline_count=baseline_thread_count), 'Extra threads timed out'
        assert_values_in_call_args_list(
            params_to_expecteds=[
                {'method': 'oauth.access', 'code': f.code},  # Call Slack OAuth
                {'method': 'chat.postMessage'},  # DM user with welcome message
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )
        assert 'createTeam' in strand_api_client.mutate.call_args_list[0][1]['operation_definition']
        assert 'createUserWithTeam' in strand_api_client.mutate.call_args_list[1][1]['operation_definition']
        assert len(strand_api_client.mutate.call_args_list) == 2
        assert db_session.query(Agent).filter(Agent.slack_team_id == f.slack_oauth_access_response.team_id).one()
        assert db_session.query(User).filter(User.agent_slack_team_id == f.slack_oauth_access_response.team_id).one()
        assert db_session.query(Installation).filter(
            Installation.installer_agent_slack_team_id == f.slack_oauth_access_response.team_id).one()

    def test_install_existing_agent_new_user(self, slack_oauth_response_and_agent_in_db, client, slack_client_class,
                                             strand_api_client, db_session, mocker, baseline_thread_count):
        """
            GIVEN: existing agent, new user, existing strand team
            OUTPUT: new User, new Installation, new StrandUser
        """
        # `slack_oauth_access_and_agent_in_db` sets up state with one existing installation
        target_url = url_for(endpoint=self.target_endpoint)
        f = slack_oauth_response_and_agent_in_db  # faked data
        payload = {'code': f.code}
        mocker.spy(slack_client_class, 'api_call')
        mocker.spy(strand_api_client, 'mutate')

        client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        assert wait_for_extra_threads_to_die(baseline_count=baseline_thread_count), 'Extra threads timed out'
        assert_values_in_call_args_list(
            params_to_expecteds=[
                {'method': 'oauth.access', 'code': f.code},  # Call Slack OAuth
                {'method': 'chat.postMessage'},  # DM user with welcome message
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )
        assert 'createUserWithTeam' in strand_api_client.mutate.call_args_list[0][1]['operation_definition']
        assert len(strand_api_client.mutate.call_args_list) == 1
        assert db_session.query(Agent).filter(Agent.slack_team_id == f.slack_oauth_access_response.team_id).one()
        assert len(
            db_session.query(User).filter(User.agent_slack_team_id == f.slack_oauth_access_response.team_id).all()) == 2
        assert len(db_session.query(Installation).filter(
            Installation.installer_agent_slack_team_id == f.slack_oauth_access_response.team_id).all()) == 2

    @pytest.mark.skip
    def test_install_new_agent_new_user_existing_strand_user(self, slack_oauth_response_and_user_in_strand, client,
                                                             slack_client_class, strand_api_client, db_session, mocker,
                                                             baseline_thread_count):
        """
            GIVEN: new agent, new user, existing strand user
            OUTPUT: new Agent, new User, new Installation, new StrandTeam
        """
        # `slack_oauth_response_and_user_in_strand` sets up state with an existing strand user
        target_url = url_for(endpoint=self.target_endpoint)
        f = slack_oauth_response_and_user_in_strand  # faked data
        payload = {'code': f.code}
        mocker.spy(slack_client_class, 'api_call')
        mocker.spy(strand_api_client, 'mutate')

        client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        assert wait_for_extra_threads_to_die(baseline_count=baseline_thread_count), 'Extra threads timed out'
        assert_values_in_call_args_list(
            params_to_expecteds=[
                {'method': 'oauth.access', 'code': f.code},  # Call Slack OAuth
                {'method': 'chat.postMessage'},  # DM user with welcome message
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )
        assert 'createTeam' in strand_api_client.mutate.call_args_list[0][1]['operation_definition']
        assert len(strand_api_client.mutate.call_args_list) == 1
        assert db_session.query(Agent).filter(Agent.slack_team_id == f.slack_oauth_access_response.team_id).one()
        assert db_session.query(User).filter(User.agent_slack_team_id == f.slack_oauth_access_response.team_id).one()
        assert db_session.query(Installation).filter(
            Installation.installer_agent_slack_team_id == f.slack_oauth_access_response.team_id).one()

    @pytest.mark.skip
    def test_install_existing_agent_new_user_existing_strand_user(
            self, slack_oauth_response_and_user_in_strand_and_agent_in_db, client, slack_client_class,
            strand_api_client, db_session, mocker, baseline_thread_count
    ):
        """
            GIVEN: existing agent, new user, existing strand user
            OUTPUT: new User, new Installation
        """
        target_url = url_for(endpoint=self.target_endpoint)
        f = slack_oauth_response_and_user_in_strand_and_agent_in_db  # faked data
        payload = {'code': f.code}
        mocker.spy(slack_client_class, 'api_call')
        mocker.spy(strand_api_client, 'mutate')

        client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))

        assert wait_for_extra_threads_to_die(baseline_count=baseline_thread_count), 'Extra threads timed out'
        assert_values_in_call_args_list(
            params_to_expecteds=[
                {'method': 'oauth.access', 'code': f.code},  # Call Slack OAuth
                {'method': 'chat.postMessage'},  # DM user with welcome message
            ],
            call_args_list=slack_client_class.api_call.call_args_list
        )
        assert 'addUserToTeam' in strand_api_client.mutate.call_args_list[0][1]['operation_definition']
        assert len(strand_api_client.mutate.call_args_list) == 1
        assert db_session.query(Agent).filter(Agent.slack_team_id == f.slack_oauth_access_response.team_id).one()
        assert len(
            db_session.query(User).filter(User.agent_slack_team_id == f.slack_oauth_access_response.team_id).all()) == 2
        assert len(db_session.query(Installation).filter(
            Installation.installer_agent_slack_team_id == f.slack_oauth_access_response.team_id).all()) == 2

    @pytest.mark.skip('TODO (nice-to-have): Don\'t allow users to re-install if they\'re already installed')
    def test_install_existing_agent_existing_user_existing_scope_with_valid_code(self):
        pass

    @pytest.mark.skip('TODO (nice-to-have): Don\'t allow bad code requests to this endpoint')
    def test_install_with_invalid_code(self):
        pass
