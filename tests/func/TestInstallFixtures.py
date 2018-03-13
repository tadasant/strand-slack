from collections import namedtuple
from typing import NamedTuple

import pytest

from tests.common.PrimitiveFaker import PrimitiveFaker
from tests.testresources.TestSlackClient import SlackRepository, clear_slack_state
from tests.testresources.TestStrandApiClient import StrandRepository, clear_strand_state
from tests.utils.create_in_db import insert_agent_user_installation


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
            Yield namedtuple(code, slack_oauth_response)
        """
        response = namedtuple('response', 'code slack_oauth_access_response')
        fake_slack_oauth_access_response = f = slack_oauth_access_response_factory()
        fake_code = str(PrimitiveFaker('md5'))

        # Plant fake response in Slack state
        SlackRepository['oauth_access_responses_by_code'][fake_code] = fake_slack_oauth_access_response
        # Plant existing objects in DB
        insert_agent_user_installation(slack_team_id=f.team_id, access_token=f.access_token, scope=f.scope,
                                       db_session=db_session)

        yield response(code=fake_code, slack_oauth_access_response=fake_slack_oauth_access_response)
        clear_slack_state(keys=['oauth_access_responses_by_code'])

    @pytest.fixture(scope='function')
    def slack_oauth_response_and_user_in_strand(self, slack_oauth_access_response_factory,
                                                slack_user_factory) -> NamedTuple:
        """
            Set TestSlackClient to contain a random slack oauth response with the same user email in Strand's state.
            Yield namedtuple(code, slack_oauth_response)
        """
        response = namedtuple('response', 'code slack_oauth_access_response')
        fake_slack_oauth_access_response = slack_oauth_access_response_factory()
        fake_code = str(PrimitiveFaker('md5'))

        # Plant fake response in Slack state
        SlackRepository['oauth_access_responses_by_code'][fake_code] = fake_slack_oauth_access_response
        # Plant fake user (same ID as the requestor) in Slack state
        fake_slack_user = slack_user_factory()
        fake_slack_user.id = fake_slack_oauth_access_response.user_id
        SlackRepository['users_by_slack_user_id'][fake_slack_user.id] = fake_slack_user
        # Plant fake user in Strand state (same email as the requestor)
        StrandRepository['users_by_email'][fake_slack_user.profile.email] = {'id': str(PrimitiveFaker('ean8'))}

        yield response(code=fake_code, slack_oauth_access_response=fake_slack_oauth_access_response)
        clear_slack_state(keys=['oauth_access_responses_by_code', 'users_by_slack_user_id'])
        clear_strand_state(keys=['users_by_email'])

    @pytest.fixture(scope='function')
    def slack_oauth_response_and_user_in_strand_and_agent_in_db(self, slack_oauth_access_response_factory,
                                                                slack_user_factory, db_session) -> NamedTuple:
        """
            Set TestSlackClient to contain a random slack oauth response with the same user email in Strand's state.
            Also set an existing agent for the slack team in the db.
            Yield namedtuple(code, slack_oauth_response)
        """
        response = namedtuple('response', 'code slack_oauth_access_response')
        fake_slack_oauth_access_response = f = slack_oauth_access_response_factory()
        fake_code = str(PrimitiveFaker('md5'))

        # Plant fake response in Slack state
        SlackRepository['oauth_access_responses_by_code'][fake_code] = fake_slack_oauth_access_response
        # Plant fake user (same ID as the requestor) in Slack state
        fake_slack_user = slack_user_factory()
        fake_slack_user.id = f.user_id
        SlackRepository['users_by_slack_user_id'][fake_slack_user.id] = fake_slack_user
        # Plant fake user in Strand state (same email as the requestor)
        StrandRepository['users_by_email'][fake_slack_user.profile.email] = {'id': str(PrimitiveFaker('ean8'))}
        # Plant existing objects in DB
        insert_agent_user_installation(slack_team_id=f.team_id, access_token=f.access_token, scope=f.scope,
                                       db_session=db_session)

        yield response(code=fake_code, slack_oauth_access_response=f)
        clear_slack_state(keys=['oauth_access_responses_by_code', 'users_by_slack_user_id'])
        clear_strand_state(keys=['users_by_email'])
