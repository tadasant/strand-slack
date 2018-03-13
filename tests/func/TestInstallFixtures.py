from collections import namedtuple
from typing import NamedTuple

import pytest

from src.models.domain.Agent import Agent, AgentStatus
from src.models.domain.Installation import Installation
from src.models.domain.User import User
from tests.common.PrimitiveFaker import PrimitiveFaker
from tests.testresources.TestSlackClient import SlackRepository, clear_slack_state


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
        fake_code = str(PrimitiveFaker('md5'))

        # Plant fake response in Slack state
        SlackRepository['oauth_access_responses_by_code'][fake_code] = fake_slack_oauth_access_response

        yield response(code=fake_code, slack_oauth_access_response=fake_slack_oauth_access_response)
        clear_slack_state(keys=['oauth_access_responses_by_code'])

    @pytest.fixture(scope='function')
    def slack_oauth_response_and_agent_in_db(self, slack_oauth_access_response_factory, db_session) -> NamedTuple:
        """
            Set TestSlackClient to contain a random slack oauth response with the corresponding agent in db.
            Also has an installer and installation in db.
            Yield namedtuple(code, slack_oauth_response, agent_slack_team_id)
        """
        response = namedtuple('response', 'code slack_oauth_access_response')
        fake_slack_oauth_access_response = f = slack_oauth_access_response_factory()
        fake_code = str(PrimitiveFaker('md5'))

        # Plant fake response in Slack state
        SlackRepository['oauth_access_responses_by_code'][fake_code] = fake_slack_oauth_access_response
        # Plant existing objects in DB
        agent = Agent(slack_team_id=f.team_id, strand_team_id=0, status=AgentStatus.ACTIVE.name)
        fake_user_id = str(PrimitiveFaker('bban'))
        user = User(slack_user_id=fake_user_id, strand_user_id=0, agent_slack_team_id=f.team_id)
        installation = Installation(access_token=f.access_token, scope=f.scope, installer_slack_user_id=fake_user_id,
                                    installer_agent_slack_team_id=f.team_id)
        db_session.add_all([agent, user, installation])
        db_session.commit()

        yield response(code=fake_code, slack_oauth_access_response=fake_slack_oauth_access_response)
        clear_slack_state(keys=['oauth_access_responses_by_code'])
