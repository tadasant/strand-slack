from src.command.Command import Command
from src.command.model.message.formatted_text import block_topic_channel_message
from src.domain.models.portal.SlackUser import SlackUserSchema


class InformTopicChannelMessageDeletedCommand(Command):
    def __init__(self, slack_client_wrapper, slack_team_id, slack_user_id, attempted_text):
        super().__init__(slack_client_wrapper=slack_client_wrapper, slack_team_id=slack_team_id)
        self.slack_user_id = slack_user_id
        self.attempted_text = attempted_text

    def execute(self):
        log_msg = f'Executing InformTopicChannelMessageDeletedCommand for {self.slack_team_id} with user ' \
                  f'{self.slack_user_id}'
        self.logger.info(log_msg)
        user_info = self.slack_client_wrapper.get_user_info(slack_team_id=self.slack_team_id,
                                                            slack_user_id=self.slack_user_id)
        slack_user = SlackUserSchema().load(user_info).data
        if not slack_user.is_bot:
            self.logger.info('Poster was not a bot, so informing them of their deleted message')
            dm_text = block_topic_channel_message(attempted_message=self.attempted_text)
            self.slack_client_wrapper.send_dm_to_user(slack_team_id=self.slack_team_id,
                                                      slack_user_id=self.slack_user_id,
                                                      text=dm_text)
