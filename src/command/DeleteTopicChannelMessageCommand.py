from src.command.Command import Command


class DeleteTopicChannelMessageCommand(Command):
    def __init__(self, slack_client_wrapper, slack_team_id, slack_channel_id, message_ts):
        super().__init__(slack_client_wrapper=slack_client_wrapper, slack_team_id=slack_team_id)
        self.slack_channel_id = slack_channel_id
        self.message_ts = message_ts

    def execute(self):
        self.logger.info(f'Executing SendUserPostTopicDialogCommand, {self.slack_team_id} with msg {self.message_ts}')
        self.slack_client_wrapper.delete_message(slack_team_id=self.slack_team_id,
                                                 slack_channel_id=self.slack_channel_id, message_ts=self.message_ts)
