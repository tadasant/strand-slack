from threading import Thread

from src.command.SendUserPostTopicDialogCommand import SendUserPostTopicDialogCommand
from src.service.Service import Service


class PostNewTopicService(Service):
    """
        Actions:
        * Send the start discussion dialog to the user
    """

    def __init__(self, slack_client_wrapper, slack_team_id, trigger_id, slack_user_id, slack_channel_id):
        super().__init__(slack_client_wrapper=slack_client_wrapper)
        self.slack_team_id = slack_team_id
        self.trigger_id = trigger_id
        self.slack_user_id = slack_user_id
        self.slack_channel_id = slack_channel_id

    def execute(self):
        command = SendUserPostTopicDialogCommand(slack_client_wrapper=self.slack_client_wrapper,
                                                 trigger_id=self.trigger_id,
                                                 slack_team_id=self.slack_team_id,
                                                 slack_user_id=self.slack_user_id,
                                                 slack_channel_id=self.slack_channel_id)
        Thread(target=command.execute, daemon=True).start()
