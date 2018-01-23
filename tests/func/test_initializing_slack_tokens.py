from flask import g, Flask

from src import create_app


class TestInitializingSlackTokens:
    def test_slack_tokens_used_in_requests(self, mocker, portal_client, slack_client_class):
        mocker.spy(portal_client, 'query')

        # set up SlackInstallations from portal
        portal_client.set_next_response({
            'slackTeamInstallations': [{
                'botAccessToken': 'token',
                'accessToken': 'token',
                'slackTeam': {
                    'id': 1
                }
            }]
        })
        app = create_app(portal_client=portal_client, SlackClientClass=slack_client_class)
        assert portal_client.query.call_count == 1

        assert len(app._slack_client_wrapper.tokens_by_team_id.values()) == 1
        # TODO replace brittle assert above with a call to some flask endpoint that kicks off a slack api call
        # TODO (assert that the call uses the appropriate token)
