from threading import Thread
from typing import List

from src.commands.database.DeleteBotsCommand import DeleteBotsCommand
from src.commands.database.DeleteInstallationsCommand import DeleteInstallationsCommand
from src.services.Service import Service
from src.utilities.database import db_session


class RevokeTokensService(Service):
    def __init__(self, slack_team_id, oauth_tokens: List[str], bot_tokens: List[str]):
        super().__init__()
        self.slack_team_id = slack_team_id
        self.oauth_tokens = oauth_tokens
        self.bot_tokens = bot_tokens

    @db_session
    def execute(self, session):
        self.logger.debug(f'Removing tokens {self.oauth_tokens} and {self.bot_tokens} from team {self.slack_team_id}')
        command = DeleteBotsCommand(slack_team_id=self.slack_team_id, bot_tokens=self.bot_tokens)
        Thread(target=command.execute, daemon=True).start()
        command = DeleteInstallationsCommand(slack_team_id=self.slack_team_id, oauth_tokens=self.oauth_tokens)
        Thread(target=command.execute, daemon=True).start()
