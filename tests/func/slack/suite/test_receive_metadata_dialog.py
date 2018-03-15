import json
from urllib.parse import urlencode

import pytest
from flask import url_for

from src.models.domain.User import User
from src.models.slack.outgoing.dialogs import EditMetadataDialog
from tests.common.PrimitiveFaker import PrimitiveFaker
from tests.factories.slackfactories import SlackTeamFactory, SlackUserFactory
from tests.func.slack.TestSlackFixtures import TestSlackFixtures
from tests.utils.asserting import wait_for_extra_threads_to_die


@pytest.mark.usefixtures('app')
class TestReceiveMetadataDialog(TestSlackFixtures):
    """Test ability of a user to submit the edit metadata dialog"""

    target_endpoint = 'slack.interactivecomponentresource'
    default_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def test_receive_metadata_dialog(self, installed_user: User, slack_client_class, strand_api_client,
                                     slack_interactive_component_request_factory, baseline_thread_count, client,
                                     mocker):
        """Receieve the metadata dialog from user when s/he submits, send info to Strand API, and post ephemeral"""
        target_url = url_for(endpoint=self.target_endpoint)
        fake_strand_id = str(PrimitiveFaker('ean8'))
        fake_slack_interactive_component_request = slack_interactive_component_request_factory(
            type='dialog_submission',
            callback_id=EditMetadataDialog(strand_id=fake_strand_id).callback_id,
            team=SlackTeamFactory.create(id=installed_user.agent_slack_team_id),
            user=SlackUserFactory.create(id=installed_user.slack_user_id),
        )
        payload = json.loads(fake_slack_interactive_component_request.to_json())
        mocker.spy(slack_client_class, 'api_call')
        mocker.spy(strand_api_client, 'mutate')

        response = client.post(path=target_url, headers=self.default_headers,
                               data=urlencode({'payload': json.dumps(payload)}))
        assert wait_for_extra_threads_to_die(baseline_count=baseline_thread_count), 'Extra threads timed out'
        assert 200 <= response.status_code <= 300

        assert slack_client_class.api_call.call_args[1]['method'] == 'chat.postEphemeral'
        assert 'updateStrand' in strand_api_client.mutate.call_args[1]['operation_definition']
        assert fake_strand_id in strand_api_client.mutate.call_args[1]['operation_definition']
