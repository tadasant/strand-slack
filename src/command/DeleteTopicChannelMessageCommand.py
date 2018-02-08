from src.command.Command import Command
from src.command.messages.formatted_text import block_topic_channel_message
from src.command.messages.post_topic_dialog import POST_TOPIC_DIALOG


class DeleteTopicChannelMessageCommand(Command):
    def __init__(self, slack_client_wrapper, slack_team_id, slack_channel_id, message_ts):
        super().__init__(slack_client_wrapper=slack_client_wrapper, slack_team_id=slack_team_id)
        self.slack_channel_id = slack_channel_id
        self.message_ts = message_ts

    def execute(self):
        self.logger.info(f'Executing SendUserPostTopicDialog for {self.slack_team_id} with user {self.slack_user_id}')
        self.slack_client_wrapper.delete_message(slack_team_id=self.slack_team_id,
                                                 slack_channel_id=self.slack_channel_id, message_ts=self.message_ts)
