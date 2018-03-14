import pytest

from src.models.domain.Agent import Agent
from src.models.domain.User import User
from tests.utils.create_in_db import insert_agent_user_installation


class TestDmFixtures:
    @pytest.fixture(scope='function')
    def installed_user(self, db_session) -> User:
        """Inserts Agent, User, and Installation, returning the inserted user"""
        agent = insert_agent_user_installation(db_session=db_session)
        return agent.users[0]

    @pytest.fixture(scope='function')
    def installed_agent(self, db_session) -> Agent:
        """Inserts Agent, User, and Installation, returning the inserted agent"""
        agent = insert_agent_user_installation(db_session=db_session)
        return agent
