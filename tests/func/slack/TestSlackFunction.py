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
        """
        Asserts that a subset of each item in params_to_expecteds exists in the call args list

        :param params_to_expecteds: e.g. [{'paramname': 'expectedval', 'param2name': 'expected2val}]
        """
        params_to_actuals = [x[1] for x in call_args_list]
        original_params_to_expecteds = params_to_expecteds.copy()
        for i, expected in enumerate(original_params_to_expecteds):
            for actual in params_to_actuals:
                if all(item in actual.items() for item in expected.items()):
                    params_to_expecteds[i] = None
        assert len([x for x in params_to_expecteds if x is not None]) == 0, f'{params_to_expecteds} not called'
