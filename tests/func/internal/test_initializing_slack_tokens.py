from src import create_app, slack_agent_repository
from tests.factories.portalfactories import SlackAgentFactory
from tests.testresources import TestSlackClient


class TestInitializingSlackApplicationInstallations:
    fake_slack_agent = SlackAgentFactory.build()
    fake_slack_team_id = fake_slack_agent.slack_team.id
    fake_slack_access_token = fake_slack_agent.slack_application_installation.access_token
    fake_slack_bot_access_token = fake_slack_agent.slack_application_installation.bot_access_token

    def test_installations_initialized_on_startup(self, mocker, portal_client):
        mocker.spy(portal_client, 'query')

        self._queue_response_from_portal(portal_client=portal_client)

        create_app(portal_client=portal_client, SlackClientClass=TestSlackClient, slack_verification_token='anything')

        assert portal_client.query.call_count == 1
        assert slack_agent_repository.get_slack_access_token(
            slack_team_id=self.fake_slack_team_id) == self.fake_slack_access_token
        assert slack_agent_repository.get_slack_bot_access_token(
            slack_team_id=self.fake_slack_team_id) == self.fake_slack_bot_access_token

    def _queue_response_from_portal(self, portal_client):
        portal_client.set_next_response({
            'data': {
                'slackAgents': [{
                    'status': self.fake_slack_agent.status,
                    'discussChannelId': self.fake_slack_agent.discuss_channel_id,
                    'slackTeam': {
                        'id': self.fake_slack_team_id
                    },
                    'slackApplicationInstallation': {
                        'accessToken': self.fake_slack_access_token,
                        'installer': {
                            'id': self.fake_slack_agent.slack_application_installation.installer.id,
                        },
                        'botAccessToken': self.fake_slack_bot_access_token
                    },
                }]
            }
        })
