from src.commands.Command import Command
from src.models.slack.outgoing.messages import MetadataUpdatedSlackMessage
from src.models.strand.StrandStrand import StrandStrand


class UpdateStrandMetadataAndInformUserCommand(Command):
    """
        1) Send strand updates to Strand API
        2) Send ephemeral success message to user
    """

    def __init__(self, slack_client_wrapper, strand_api_client_wrapper, slack_team_id, strand: StrandStrand,
                 slack_user_id, slack_channel_id, use_bot_token=True):
        super().__init__(slack_client_wrapper=slack_client_wrapper, strand_api_client_wrapper=strand_api_client_wrapper)
        self.slack_team_id = slack_team_id
        self.strand = strand
        self.slack_user_id = slack_user_id
        self.slack_channel_id = slack_channel_id
        self.use_bot_token = use_bot_token

    def execute(self):
        self.logger.info(f'Executing UpdateStrandMetadataAndInformUserCommand for strand {self.strand.id}')
        self.strand_api_client_wrapper.update_strand(strand=self.strand)
        self.slack_client_wrapper.send_ephemeral_message(slack_team_id=self.slack_team_id,
                                                         slack_channel_id=self.slack_channel_id,
                                                         slack_user_id=self.slack_user_id,
                                                         text=MetadataUpdatedSlackMessage().text,
                                                         use_bot_token=self.use_bot_token)
