from src.command.Command import Command
from src.command.model.message.formatted_text import block_topic_channel_message


class InformTopicChannelMessageDeletedCommand(Command):
    def __init__(self, slack_client_wrapper, slack_team_id, slack_user_id, attempted_text):
        super().__init__(slack_client_wrapper=slack_client_wrapper, slack_team_id=slack_team_id)
        self.slack_user_id = slack_user_id
        self.attempted_text = attempted_text

    def execute(self):
        log_msg = f'Executing InformTopicChannelMessageDeletedCommand for {self.slack_team_id} with user ' \
                  '{self.slack_user_id}'
        self.logger.info(log_msg)
        dm_text = block_topic_channel_message(attempted_message=self.attempted_text)
        self.slack_client_wrapper.send_dm_to_user(slack_team_id=self.slack_team_id, slack_user_id=self.slack_user_id,
                                                  text=dm_text)
