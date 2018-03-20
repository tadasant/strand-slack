import json
from urllib.parse import urlencode

import pytest
from flask import url_for

from src.models.domain.User import User
from src.models.slack.outgoing.actions import EditMetadataButton
from tests.common.PrimitiveFaker import PrimitiveFaker
from tests.factories.slackfactories import SlackActionFactory, SlackTeamFactory, SlackUserFactory
from tests.func.slack.TestSlackFixtures import TestSlackFixtures
from tests.utils.asserting import wait_for_extra_threads_to_die


@pytest.mark.usefixtures('app')
class TestSendMetadataDialog(TestSlackFixtures):
    """Test ability of a user to trigger the save metadata dialog"""

    target_endpoint = 'slack.interactivecomponentresource'
    default_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def test_send_metadata_dialog(self, installed_user: User, slack_client_class,
                                  slack_interactive_component_request_factory, baseline_thread_count, client, mocker):
        """Send the dialog to the user when s/he clicks the button to prompt it"""
        target_url = url_for(endpoint=self.target_endpoint)
        fake_strand_id = str(PrimitiveFaker('ean8'))
        fake_slack_interactive_component_request = slack_interactive_component_request_factory(
            team=SlackTeamFactory.create(id=installed_user.agent_slack_team_id),
            user=SlackUserFactory.create(id=installed_user.slack_user_id),
            actions=[SlackActionFactory.create(
                name=EditMetadataButton(value=fake_strand_id).name,
                type='dialog_submission',
                value=fake_strand_id
            )]
        )
        fake_trigger_id = fake_slack_interactive_component_request.trigger_id
        payload = json.loads(fake_slack_interactive_component_request.to_json())
        mocker.spy(slack_client_class, 'api_call')

        response = client.post(path=target_url, headers=self.default_headers,
                               data=urlencode({'payload': json.dumps(payload)}))
        assert wait_for_extra_threads_to_die(baseline_count=baseline_thread_count), 'Extra threads timed out'
        assert 200 <= response.status_code <= 300

        assert slack_client_class.api_call.call_args[1]['method'] == 'dialog.open'
        assert slack_client_class.api_call.call_args[1]['trigger_id'] == fake_trigger_id
