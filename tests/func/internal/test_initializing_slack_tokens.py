from src import create_app
from tests.common.PrimitiveFaker import PrimitiveFaker
from tests.testresources import TestSlackClient


class TestInitializingSlackApplicationInstallations:
    def test_installations_initialized_on_startup(self, mocker, portal_client, slack_application_installation_factory):
        mocker.spy(portal_client, 'query')
        fake_slack_team_id = str(PrimitiveFaker('ean8'))
        fake_installation = slack_application_installation_factory.build()

        # set up SlackInstallations from portal
        portal_client.set_next_response({
            'data': {
                'slackApplicationInstallations': [{
                    'botAccessToken': fake_installation.bot_access_token,
                    'accessToken': fake_installation.access_token,
                    'slackTeam': {
                        'id': fake_slack_team_id
                    }
                }]
            }
        })
        app = create_app(portal_client=portal_client, SlackClientClass=TestSlackClient)
        assert portal_client.query.call_count == 1

        assert len(app.slack_client_wrapper.installations_by_team_id.values()) == 1
        # TODO replace brittle assert above with a call to some flask endpoint that kicks off a slack api call
        # TODO (assert that the call uses the appropriate token)
