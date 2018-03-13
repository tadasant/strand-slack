from src.models.domain.Agent import Agent, AgentStatus
from src.models.domain.Installation import Installation
from src.models.domain.User import User
from tests.common.PrimitiveFaker import PrimitiveFaker


def insert_agent_user_installation(slack_team_id, access_token, scope, db_session):
    agent = Agent(slack_team_id=slack_team_id, strand_team_id=0, status=AgentStatus.ACTIVE.name)
    fake_user_id = str(PrimitiveFaker('bban'))
    user = User(slack_user_id=fake_user_id, strand_user_id=0, agent_slack_team_id=slack_team_id)
    installation = Installation(access_token=access_token, scope=scope, installer_slack_user_id=fake_user_id,
                                installer_agent_slack_team_id=slack_team_id)
    db_session.add_all([agent, user, installation])
    db_session.commit()
