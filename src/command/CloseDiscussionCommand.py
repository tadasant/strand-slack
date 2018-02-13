from src.command.Command import Command


class CloseDiscussionCommand(Command):
    def __init__(self, portal_client_wrapper, slack_channel_id, slack_team_id, slack_user_id):
        super().__init__(portal_client_wrapper=portal_client_wrapper, slack_team_id=slack_team_id)
        self.slack_channel_id = slack_channel_id
        self.slack_user_id = slack_user_id

    def execute(self):
        log_msg = f'Executing CloseDiscussionCommand for {self.slack_team_id} for chan {self.slack_channel_id}'
        self.logger.info(log_msg)
        self.portal_client_wrapper.close_discussion(slack_channel_id=self.slack_channel_id,
                                                    slack_user_id=self.slack_user_id)
