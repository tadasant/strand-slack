from copy import deepcopy

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

    def add_slack_agent_to_repository(self, slack_agent_repository, slack_team_id, installer_user_id='doesnt matter'):
        slack_agent_repository.add_slack_agent(slack_agent=SlackAgent(
            status=SlackAgentStatus.ACTIVE,
            slack_team=SlackTeam(id=slack_team_id),
            slack_application_installation=SlackApplicationInstallation(access_token='doesnt matter',
                                                                        installer=SlackUser(id=installer_user_id),
                                                                        bot_access_token='doesnt matter',
                                                                        bot_user_id='doesnt matter'))
        )

    def assert_values_in_call_args_list(self, params_to_expecteds, call_args_list, expect_succeed=True):
        """
        Asserts that a subset of each item in params_to_expecteds exists in the call args list.

        If expect_succeed is False, will return the inverse. Useful when checking to make sure calls DIDN'T happen.

        :param params_to_expecteds: e.g. [{'paramname': 'expectedval', 'param2name': 'expected2val}]
        """
        params_to_actuals = [x[1] for x in call_args_list]
        original_params_to_expecteds = deepcopy(params_to_expecteds)
        for i, expected in enumerate(original_params_to_expecteds):
            for j, actual in enumerate(params_to_actuals):
                if all(item in actual.items() for item in expected.items()):
                    params_to_expecteds[i] = None
                    params_to_actuals[j] = {}
                    break

        condition = len([x for x in params_to_expecteds if x is not None]) == 0
        assert condition if expect_succeed else not condition, f'{params_to_expecteds} vs. {params_to_actuals}'
