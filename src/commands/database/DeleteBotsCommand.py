from src.commands.Command import Command
from src.models.domain.Bot import Bot
from src.utilities.database import db_session


class DeleteBotsCommand(Command):
    def __init__(self, slack_team_id, bot_tokens):
        super().__init__()
        self.slack_team_id = slack_team_id
        self.bot_oauth_tokens = bot_tokens

    @db_session
    def execute(self, session):
        self.logger.info(f'Executing DeleteBotsCommand {self.bot_oauth_tokens} for {self.slack_team_id}')
        session.query(Bot).filter(
            Bot.agent_slack_team_id == self.slack_team_id,
            Bot.access_token.in_(self.bot_oauth_tokens)
        ).delete(synchronize_session='fetch')
        session.commit()
