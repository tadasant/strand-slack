from src.commands.Command import Command
from src.models.slack.outgoing.dialogs import EditMetadataDialog


class SendEditMetadataDialogCommand(Command):
    def __init__(self, slack_client_wrapper, slack_team_id, trigger_id, strand_id):
        super().__init__(slack_client_wrapper=slack_client_wrapper)
        self.slack_team_id = slack_team_id
        self.trigger_id = trigger_id
        self.strand_id = strand_id

    def execute(self):
        log_msg = f'Executing SendEditMetadataDialogCommand for {self.slack_team_id} with trigger {self.trigger_id}'
        self.logger.info(log_msg)
        self.slack_client_wrapper.send_dialog(trigger_id=self.trigger_id, slack_team_id=self.slack_team_id,
                                              dialog=EditMetadataDialog(strand_id=self.strand_id))
