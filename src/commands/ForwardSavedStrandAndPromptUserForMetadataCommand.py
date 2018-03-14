from src.commands.Command import Command
from src.models.slack.outgoing.formats.dialogs import POST_TOPIC_DIALOG_WITH_CHANNEL_OPTION


class ForwardSavedStrandAndPromptUserForMetadataCommand(Command):
    """
        1) Send strand to Strand API
        2) Send metadata dialog to saver user
    """
    def __init__(self, slack_client_wrapper, strand_api_client_wrapper, strand_team_id, saver_strand_user_id, body):
        super().__init__(slack_client_wrapper=slack_client_wrapper, strand_api_client_wrapper=strand_api_client_wrapper)
        self.strand_team_id = strand_team_id
        self.saver_strand_user_id = saver_strand_user_id
        self.body = body

    def execute(self):
        self.logger.info(f'Executing Forwa...Command for {self.strand_team_id} with user {self.saver_strand_user_id}')
        # send to Strand
        # self.slack_client_wrapper.send_dialog(trigger_id=self.trigger_id, slack_team_id=self.slack_team_id,
        #                                       dialog=POST_TOPIC_DIALOG_WITH_CHANNEL_OPTION.value)
