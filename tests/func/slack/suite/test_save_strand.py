import json
from http import HTTPStatus

import pytest
from flask import url_for

from src.models.domain.User import User
from tests.factories.slackfactories import SlackEventFactory
from tests.func.slack.TestDmFixtures import TestDmFixtures
from tests.utils.asserting import wait_for_extra_threads_to_die


@pytest.mark.usefixtures('app')
class TestSaveStrand(TestDmFixtures):
    """Test the flow for a user copy/pasting a strand into DM"""

    target_endpoint = 'slack.eventresource'
    default_headers = {'Content-Type': 'application/json'}

    def test_save_installed_user(self, installed_user: User, slack_client_class, strand_api_client,
                                 slack_event_request_factory, baseline_thread_count, client, mocker):
        """Forward the pasted message to Strand API, and send the user an ephemeral message to invoke metadata edit"""
        target_url = url_for(endpoint=self.target_endpoint)
        fake_slack_event_request = slack_event_request_factory(
            type='event_callback',
            challenge=None,
            team_id=installed_user.agent_slack_team_id,
            event=SlackEventFactory.create(
                user=installed_user.slack_user_id,
                text='this is some stuff i want saved',
                channel='D12345678',
                type='message'
            )
        )
        payload = json.loads(fake_slack_event_request.to_json())
        mocker.spy(slack_client_class, 'api_call')
        mocker.spy(strand_api_client, 'mutate')

        response = client.post(path=target_url, headers=self.default_headers, data=json.dumps(payload))
        assert wait_for_extra_threads_to_die(baseline_count=baseline_thread_count), 'Extra threads timed out'
        assert HTTPStatus.OK == response.status_code

        assert 'createStrand' in strand_api_client.mutate.call_args[1]['operation_definition']
        assert str(installed_user.strand_user_id) in strand_api_client.mutate.call_args[1]['operation_definition']
        assert str(installed_user.agent.strand_team_id) in strand_api_client.mutate.call_args[1]['operation_definition']
        assert slack_client_class.api_call.call_args[1]['method'] == 'chat.postMessage'
