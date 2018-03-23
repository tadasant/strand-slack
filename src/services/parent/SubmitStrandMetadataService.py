from threading import Thread

from src.commands.UpdateStrandMetadataAndInformUserCommand import UpdateStrandMetadataAndInformUserCommand
from src.models.strand.StrandStrand import StrandStrand
from src.services.Service import Service
from src.utilities.database import db_session


class SubmitStrandMetadataService(Service):
    def __init__(self, slack_team_id, slack_client_wrapper, strand_api_client_wrapper, slack_user_id, slack_channel_id,
                 strand: StrandStrand):
        super().__init__(slack_client_wrapper=slack_client_wrapper, strand_api_client_wrapper=strand_api_client_wrapper)
        self.slack_team_id = slack_team_id
        self.strand = strand
        self.slack_user_id = slack_user_id
        self.slack_channel_id = slack_channel_id

    @db_session
    def execute(self, session):
        self.logger.debug(f'Sending edit metadata submission to strand {self.strand.id} on team {self.slack_team_id}')
        command = UpdateStrandMetadataAndInformUserCommand(slack_client_wrapper=self.slack_client_wrapper,
                                                           strand_api_client_wrapper=self.strand_api_client_wrapper,
                                                           slack_team_id=self.slack_team_id,
                                                           slack_user_id=self.slack_user_id,
                                                           slack_channel_id=self.slack_channel_id,
                                                           strand=self.strand,
                                                           use_bot_token=False)
        Thread(target=command.execute, daemon=True).start()
