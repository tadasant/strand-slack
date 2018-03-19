from src.models.domain.Agent import Agent, AgentStatus
from src.models.domain.Bot import Bot
from src.models.domain.Installation import Installation
from src.models.domain.User import User
from tests.common.PrimitiveFaker import PrimitiveFaker


def insert_agent_user_installation(db_session, access_token='', scope='',
                                   slack_team_id=str(PrimitiveFaker('bban'))) -> Agent:
    """Creates Agent, User, and Installation from provided arguments. Returns Agent aggregate."""
    agent = Agent(slack_team_id=slack_team_id, strand_team_id=int(str(PrimitiveFaker('ean8'))),
                  status=AgentStatus.ACTIVE.name)
    fake_user_id = str(PrimitiveFaker('bban'))
    bot = Bot(access_token=str(PrimitiveFaker('md5')), user_id=str(PrimitiveFaker('bban')),
              agent_slack_team_id=slack_team_id, agent=agent)
    user = User(slack_user_id=fake_user_id, strand_user_id=int(str(PrimitiveFaker('ean8'))),
                agent_slack_team_id=slack_team_id, agent=agent)
    installation = Installation(access_token=access_token, scope=scope, installer_slack_user_id=fake_user_id,
                                installer_agent_slack_team_id=slack_team_id, installer=user)
    db_session.add_all([agent, user, installation, bot])
    db_session.commit()
    return agent
