from collections import namedtuple
from typing import NamedTuple

import pytest


@pytest.mark.usefixtures('app')
class TestInstallFixtures:
    @pytest.fixture(scope='function')
    def slack_oauth_access(self, slack_oauth_access_response_factory) -> NamedTuple:
        """
            Set TestSlackClient to contain a random slack oauth response.
            Yield namedtuple(code, slack_oauth_access_response)
        """
        response = namedtuple('response', 'code slack_oauth_access_response')
        fake_slack_oauth_access_response = slack_oauth_access_response_factory()
        # store faker values in the test Slack client repo w/ random code
        yield response(code='12345', slack_oauth_access_response=fake_slack_oauth_access_response)
        # clear the values
        pass

    @pytest.fixture(scope='function')
    def slack_oauth_response_and_agent_in_db(self, slack_oauth_response_factory) -> NamedTuple:
        """
            Set TestSlackClient to contain a random slack oauth response with the corresponding agent in db.
            Yield namedtuple(code, slack_oauth_response, agent_slack_team_id)
        """
        # store faker values in the test Slack client repo w/ random code
        # yield namedtuple
        # clear the values
        pass

    @pytest.fixture(scope='function')
    def slack_oauth_response_and_agent_and_installer_in_db(self, slack_oauth_response_factory) -> NamedTuple:
        """
            Set TestSlackClient to contain a random slack oauth response with the corresponding agent, installer in db.
            Yield namedtuple(code, slack_oauth_response, agent_slack_team_id, installer_slack_user_id)
        """
        # store faker values in the test Slack client repo w/ random code
        # yield namedtuple
        # clear the values
        pass
