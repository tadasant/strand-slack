from src.commands.Command import Command
from src.models.domain.Agent import Agent
from src.utilities.database import db_session


class DeleteAgentCommand(Command):
    def __init__(self, slack_team_id):
        super().__init__()
        self.slack_team_id = slack_team_id

    @db_session
    def execute(self, session):
        self.logger.info(f'Executing DeleteAgentCommand for {self.slack_team_id}')
        agent = session.query(Agent).filter_by(slack_team_id=self.slack_team_id).one_or_none()
        session.delete(agent)
        session.commit()
