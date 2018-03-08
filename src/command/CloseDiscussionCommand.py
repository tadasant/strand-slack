from src.command.Command import Command


class CloseDiscussionCommand(Command):
    def __init__(self, core_api_client_wrapper, slack_channel_id, slack_team_id, slack_user_id):
        super().__init__(core_api_client_wrapper=core_api_client_wrapper, slack_team_id=slack_team_id)
        self.slack_channel_id = slack_channel_id
        self.slack_user_id = slack_user_id

    def execute(self):
        log_msg = f'Executing CloseDiscussionCommand for {self.slack_team_id} for chan {self.slack_channel_id}'
        self.logger.info(log_msg)
        self.core_api_client_wrapper.close_discussion_from_slack(slack_channel_id=self.slack_channel_id,
                                                                 slack_user_id=self.slack_user_id)
