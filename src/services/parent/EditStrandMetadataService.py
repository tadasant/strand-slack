from threading import Thread

from src.commands.SendEditMetadataDialogCommand import SendEditMetadataDialogCommand
from src.services.Service import Service
from src.utilities.database import db_session


class EditStrandMetadataService(Service):
    def __init__(self, slack_team_id, trigger_id, slack_client_wrapper, strand_id):
        super().__init__(slack_client_wrapper=slack_client_wrapper)
        self.slack_team_id = slack_team_id
        self.trigger_id = trigger_id
        self.strand_id = strand_id

    @db_session
    def execute(self, session):
        self.logger.debug(f'Providing edit metadata dialog to trigger {self.trigger_id} on team {self.slack_team_id}')
        command = SendEditMetadataDialogCommand(slack_client_wrapper=self.slack_client_wrapper,
                                                strand_id=self.strand_id, slack_team_id=self.slack_team_id,
                                                trigger_id=self.trigger_id)
        Thread(target=command.execute, daemon=True).start()
