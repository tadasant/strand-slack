from src.command.Command import Command
from src.command.message.post_topic_dialog import POST_TOPIC_DIALOG


class SendUserPostTopicDialogCommand(Command):
    def __init__(self, slack_client_wrapper, trigger_id, slack_team_id, slack_user_id):
        super().__init__(slack_client_wrapper=slack_client_wrapper, slack_team_id=slack_team_id)
        self.slack_user_id = slack_user_id
        self.trigger_id = trigger_id

    def execute(self):
        """Send user a dialog box to fill out for a new topic"""
        self.logger.info(f'Executing SendUserPostTopicDialog for {self.slack_team_id} with user {self.slack_user_id}')
        self.slack_client_wrapper.send_dialog(trigger_id=self.trigger_id, slack_team_id=self.slack_team_id,
                                              dialog=POST_TOPIC_DIALOG.value)
