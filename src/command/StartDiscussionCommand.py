from src.command.Command import Command


class StartDiscussionCommand(Command):
    def __init__(self, slack_client_wrapper, portal_client_wrapper, slack_team_id):
        super().__init__(slack_team_id=slack_team_id, slack_client_wrapper=slack_client_wrapper,
                         portal_client_wrapper=portal_client_wrapper)

    def execute(self):
        self.logger.info(f'Executing StartDiscussionCommand for {self.slack_team_id}')
