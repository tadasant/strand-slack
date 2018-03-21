import json
from http import HTTPStatus

import pytest
from flask import url_for

from src.models.domain.Agent import Agent
from src.models.domain.User import User
from tests.common.PrimitiveFaker import PrimitiveFaker
from tests.factories.slackfactories import SlackEventFactory
from tests.func.slack.TestSlackFixtures import TestSlackFixtures
from tests.utils.asserting import wait_for_extra_threads_to_die, assert_values_in_call_args_list


@pytest.mark.usefixtures('app')
class TestHelpDm(TestSlackFixtures):
    """Test the flows for a user receiving an ephemeral Help message"""

    target_endpoint = 'slack.eventresource'
    default_headers = {'Content-Type': 'application/json'}

    def test_help_dm_installed_user(self, installed_user: User, slack_client_class, slack_event_request_factory,
                                    baseline_thread_count, client, mocker):
        """Ensure we send a help message to users who have the app installed when they DM 'help'"""
        target_url = url_for(endpoint=self.target_endpoint)
        fake_slack_event_request = slack_event_request_factory(
            type='event_callback',
            challenge=None,
            team_id=installed_user.agent_slack_team_id,
            event=SlackEventFactory.create(
                user=installed_user.slack_user_id,
                text='HELP',
                channel='D12345678',
                type='message'
            )
        )
        payload = json.loads(fake_slack_event_request.to_json())
        mocker.spy(slack_client_class, 'api_call')

        response = client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))
        assert wait_for_extra_threads_to_die(baseline_count=baseline_thread_count), 'Extra threads timed out'
        assert HTTPStatus.OK == response.status_code

        assert slack_client_class.api_call.call_args[1]['method'] == 'chat.postEphemeral'
        assert 'installing the app' not in slack_client_class.api_call.call_args[1]['text']

    def test_nonhelp_dm_installed_user(self, installed_user: User, slack_client_class, slack_event_request_factory,
                                       baseline_thread_count, client, mocker):
        """Ensure we don't send a help message in 'non-help' DMs"""
        target_url = url_for(endpoint=self.target_endpoint)
        fake_slack_event_request = slack_event_request_factory(
            type='event_callback',
            challenge=None,
            team_id=installed_user.agent_slack_team_id,
            event=SlackEventFactory.create(
                user=installed_user.slack_user_id,
                text='this is not a help dm',
                channel='D12345678',
                type='message'
            )
        )
        payload = json.loads(fake_slack_event_request.to_json())
        mocker.spy(slack_client_class, 'api_call')

        response = client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))
        assert wait_for_extra_threads_to_die(baseline_count=baseline_thread_count), 'Extra threads timed out'
        assert HTTPStatus.OK == response.status_code

        assert_values_in_call_args_list(
            params_to_expecteds=[
                {'method': 'chat.postEphemeral'},  # Ensure help message was not sent
            ],
            call_args_list=slack_client_class.api_call.call_args_list,
            expect_succeed=False
        )

    @pytest.mark.parametrize('dm_message_text', ['help', 'any message', 'any help message'])
    def test_help_dm_new_user(self, installed_agent: Agent, slack_client_class, slack_event_request_factory,
                              baseline_thread_count, client, mocker, dm_message_text):
        """All users who do not have the app installed should receive a help to install DM response to any message"""
        target_url = url_for(endpoint=self.target_endpoint)
        fake_slack_event_request = slack_event_request_factory(
            type='event_callback',
            challenge=None,
            team_id=installed_agent.slack_team_id,
            event=SlackEventFactory.create(
                user=str(PrimitiveFaker('bban')),
                text=dm_message_text,
                channel='D12345678',
                type='message'
            )
        )
        payload = json.loads(fake_slack_event_request.to_json())
        mocker.spy(slack_client_class, 'api_call')

        response = client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))
        assert wait_for_extra_threads_to_die(baseline_count=baseline_thread_count), 'Extra threads timed out'
        assert HTTPStatus.OK == response.status_code

        assert slack_client_class.api_call.call_args[1]['method'] == 'chat.postEphemeral'
        assert 'installing the app' in slack_client_class.api_call.call_args[1]['text']
