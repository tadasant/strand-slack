from src.commands.Command import Command
from src.models.slack.outgoing.messages import ErrorSlackMessage


class SendErrorMessageCommand(Command):
    def __init__(self, slack_client_wrapper, slack_team_id, slack_user_id, slack_channel_id, error_title, error_text):
        super().__init__(slack_client_wrapper=slack_client_wrapper)
        self.slack_team_id = slack_team_id
        self.slack_user_id = slack_user_id
        self.slack_channel_id = slack_channel_id
        self.error_title = error_title
        self.error_text = error_text

    def execute(self):
        log_msg = f'Executing SendErrorMessageCommand for {self.slack_team_id} with user {self.slack_user_id}'
        self.logger.info(log_msg)
        error_message = ErrorSlackMessage(error_title=self.error_title, error_text=self.error_text)
        self.slack_client_wrapper.send_ephemeral_message(slack_team_id=self.slack_team_id,
                                                         slack_channel_id=self.slack_channel_id,
                                                         slack_user_id=self.slack_user_id,
                                                         text=error_message.text,
                                                         attachments=error_message.attachments)
