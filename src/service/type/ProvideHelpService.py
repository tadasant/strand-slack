from threading import Thread

from src.command.SendHelpMessageCommand import SendHelpMessageCommand
from src.service.Service import Service


class ProvideHelpService(Service):
    """
        Sends the invoker an ephemeral help message

        Actions:
        * Send an ephemeral message
    """

    def __init__(self, slack_client_wrapper, slack_team_id, slack_user_id, slack_channel_id):
        super().__init__(slack_client_wrapper=slack_client_wrapper)
        self.slack_team_id = slack_team_id
        self.slack_user_id = slack_user_id
        self.slack_channel_id = slack_channel_id

    def execute(self):
        slack_command = SendHelpMessageCommand(slack_client_wrapper=self.slack_client_wrapper,
                                               slack_channel_id=self.slack_channel_id,
                                               slack_team_id=self.slack_team_id,
                                               slack_user_id=self.slack_user_id)
        Thread(target=slack_command.execute, daemon=True).start()
