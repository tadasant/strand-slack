from src.command.Command import Command
from src.command.messages.formatted_text import close_discussion


class CloseChannelCommand(Command):
    def __init__(self, slack_client_wrapper, slack_channel_id, slack_team_id, slack_user_id):
        super().__init__(slack_client_wrapper=slack_client_wrapper, slack_team_id=slack_team_id)
        self.slack_channel_id = slack_channel_id
        self.slack_user_id = slack_user_id

    def execute(self):
        log_msg = f'Executing CloseChannelCommand for {self.slack_team_id} for chan {self.slack_channel_id}'
        self.logger.info(log_msg)
        self.slack_client_wrapper.send_message(slack_team_id=self.slack_team_id, slack_channel_id=self.slack_channel_id,
                                               text=close_discussion(closer_slack_user_id=self.slack_user_id))
        self.slack_client_wrapper.archive_channel(slack_team_id=self.slack_team_id,
                                                  slack_channel_id=self.slack_channel_id)
