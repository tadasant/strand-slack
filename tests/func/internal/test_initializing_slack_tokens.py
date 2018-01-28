from src import create_app, slack_agent_repository
from tests.testresources import TestSlackClient


class TestInitializingSlackApplicationInstallations:
    def test_installations_initialized_on_startup(self, mocker, portal_client, slack_agent_factory):
        mocker.spy(portal_client, 'query')
        fake_slack_agent = slack_agent_factory.build()
        fake_slack_team_id = fake_slack_agent.slack_team.id
        fake_slack_access_token = fake_slack_agent.slack_application_installation.access_token
        fake_slack_bot_access_token = fake_slack_agent.slack_application_installation.bot_access_token

        # set up SlackInstallations from portal
        portal_client.set_next_response({
            'data': {
                'slackAgents': [{
                    'status': fake_slack_agent.status,
                    'helpChannelId': fake_slack_agent.help_channel_id,
                    'slackTeam': {
                        'id': fake_slack_team_id
                    },
                    'slackApplicationInstallation': {
                        'accessToken': fake_slack_access_token,
                        'installer': {
                            'id': fake_slack_agent.slack_application_installation.installer.id,
                        },
                        'botAccessToken': fake_slack_bot_access_token
                    },
                }]
            }
        })
        create_app(portal_client=portal_client, SlackClientClass=TestSlackClient, slack_verification_token='anything')

        assert portal_client.query.call_count == 1
        assert slack_agent_repository.get_slack_access_token(
            slack_team_id=fake_slack_team_id) == fake_slack_access_token
        assert slack_agent_repository.get_slack_bot_access_token(
            slack_team_id=fake_slack_team_id) == fake_slack_bot_access_token
