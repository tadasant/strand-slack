from src.commands.Command import Command
from src.models.domain.Installation import Installation
from src.utilities.database import db_session


class DeleteInstallationsCommand(Command):
    def __init__(self, slack_team_id, oauth_tokens):
        super().__init__()
        self.slack_team_id = slack_team_id
        self.oauth_tokens = oauth_tokens

    @db_session
    def execute(self, session):
        self.logger.info(f'Executing DeleteInstallationsCommand {self.oauth_tokens} for {self.slack_team_id}')
        session.query(Installation).filter(
            Installation.installer_agent_slack_team_id == self.slack_team_id,
            Installation.access_token.in_(self.oauth_tokens)
        ).delete(synchronize_session='fetch')
        session.commit()
