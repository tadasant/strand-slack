from src.domain.models.portal.SlackAgent import SlackAgent
from src.domain.models.portal.SlackAgentStatus import SlackAgentStatus
from src.domain.models.portal.SlackApplicationInstallation import SlackApplicationInstallation
from src.domain.models.portal.SlackTeam import SlackTeam
from src.domain.models.portal.SlackUser import SlackUser
from tests.func.TestFunction import TestFunction


class TestSlackFunction(TestFunction):
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

    def assert_values_in_call_args_list(self, params_to_expecteds, call_args_list):
        params_to_actuals = [x[1] for x in call_args_list]
        remaining_params_to_expecteds = params_to_expecteds.copy()
        for i, expected in enumerate(params_to_expecteds):
            for actual in params_to_actuals:
                if all(item in actual.items() for item in expected.items()):
                    del remaining_params_to_expecteds[i]
        assert len(remaining_params_to_expecteds) == 0, f'Expected {remaining_params_to_expecteds} to be called'
