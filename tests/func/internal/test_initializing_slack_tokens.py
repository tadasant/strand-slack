from factory import Faker

from src import create_app
from tests.testresources import TestSlackClient


class TestInitializingSlackTokens:
    def test_slack_tokens_used_in_requests(self, mocker, portal_client, slack_tokens_factory):
        mocker.spy(portal_client, 'query')
        fake_slack_team_id = Faker('ean8')
        fake_tokens = slack_tokens_factory.build()

        # set up SlackInstallations from portal
        portal_client.set_next_response({
            'data': {
                'slackTeamInstallations': [{
                    'botAccessToken': fake_tokens.bot_access_token,
                    'accessToken': fake_tokens.access_token,
                    'slackTeam': {
                        'id': fake_slack_team_id
                    }
                }]
            }
        })
        app = create_app(portal_client=portal_client, SlackClientClass=TestSlackClient)
        assert portal_client.query.call_count == 1

        assert len(app.slack_client_wrapper.tokens_by_team_id.values()) == 1
        # TODO replace brittle assert above with a call to some flask endpoint that kicks off a slack api call
        # TODO (assert that the call uses the appropriate token)
