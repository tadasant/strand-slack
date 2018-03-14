from threading import Thread

from src.commands.SendPleaseInstallMessageCommand import SendPleaseInstallMessageCommand
from src.models.domain.User import User
from src.services.Service import Service
from src.utilities.database import db_session


class InitiateSaveStrandService(Service):
    def __init__(self, slack_team_id, slack_user_id, slack_channel_id, text, slack_client_wrapper):
        super().__init__(slack_client_wrapper=slack_client_wrapper)
        self.slack_team_id = slack_team_id
        self.slack_user_id = slack_user_id
        self.slack_channel_id = slack_channel_id
        self.text = text

    @db_session
    def execute(self, session):
        log_msg = f'Saving Strand with body {self.text} for user {self.slack_user_id} on team {self.slack_team_id}'
        self.logger.debug(log_msg)
        if User.is_installer(session, self.slack_user_id, self.slack_team_id):
            # TODO implement saving strands
            pass
        else:
            command = SendPleaseInstallMessageCommand(slack_client_wrapper=self.slack_client_wrapper,
                                                      slack_team_id=self.slack_team_id,
                                                      slack_user_id=self.slack_user_id,
                                                      slack_channel_id=self.slack_channel_id)
            Thread(target=command.execute, daemon=True).start()
