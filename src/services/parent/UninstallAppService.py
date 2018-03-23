from threading import Thread

from src.commands.database.DeleteAgentCommand import DeleteAgentCommand
from src.services.Service import Service
from src.utilities.database import db_session


class UninstallAppService(Service):
    def __init__(self, slack_team_id):
        super().__init__()
        self.slack_team_id = slack_team_id

    @db_session
    def execute(self, session):
        self.logger.debug(f'Uninstalling Slack application from team {self.slack_team_id}')
        command = DeleteAgentCommand(slack_team_id=self.slack_team_id)
        Thread(target=command.execute, daemon=True).start()
