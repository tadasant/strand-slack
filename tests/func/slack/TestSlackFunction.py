import pytest

from src.domain.models.portal.SlackAgent import SlackAgent
from src.domain.models.portal.SlackAgentStatus import SlackAgentStatus
from src.domain.models.portal.SlackApplicationInstallation import SlackApplicationInstallation
from src.domain.models.portal.SlackTeam import SlackTeam
from src.domain.models.portal.SlackUser import SlackUser


@pytest.mark.usefixtures('client_class')  # pytest-flask's client_class adds self.client
class TestSlackFunction:
    default_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    def add_slack_agent_to_repository(self, slack_agent_repository, slack_team_id):
        slack_agent_repository.add_slack_agent(slack_agent=SlackAgent(
            status=SlackAgentStatus.ACTIVE,
            slack_team=SlackTeam(id=slack_team_id),
            slack_application_installation=SlackApplicationInstallation(access_token='doesnt matter',
                                                                        installer=SlackUser(id='doesnt matter'),
                                                                        bot_access_token='doesnt matter'))
        )
