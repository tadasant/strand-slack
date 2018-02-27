from src.command.Command import Command
from src.command.model.message.formatted_text import unauthorized_message


class InformUserUnauthorizedCommand(Command):
    def __init__(self, slack_client_wrapper, slack_team_id, slack_user_id, slack_channel_id):
        super().__init__(slack_client_wrapper=slack_client_wrapper, slack_team_id=slack_team_id)
        self.slack_user_id = slack_user_id
        self.slack_channel_id = slack_channel_id

    def execute(self):
        log_msg = f'Executing InformUserUnauthorizedCommand for {self.slack_team_id} with user {self.slack_user_id}'
        self.logger.info(log_msg)
        self.slack_client_wrapper.send_ephemeral_message(slack_team_id=self.slack_team_id,
                                                         slack_channel_id=self.slack_channel_id,
                                                         slack_user_id=self.slack_user_id,
                                                         text=unauthorized_message())
