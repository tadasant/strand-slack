from threading import Thread

from src.service.Service import Service
from src.command.SaveMessageAsTopicCommand import SaveMessageAsTopicCommand


class SaveMessageAsTopicService(Service):
    """
        Create topic for message
        Create discussion for topic
        Create message in discussion
        Close discussion
    """

    def __init__(self, slack_client_wrapper, core_api_client_wrapper, slack_team_id=None, slack_channel_id=None,
                 original_poster_slack_user_id=None, slack_message_ts=None):
        super().__init__(slack_client_wrapper=slack_client_wrapper, core_api_client_wrapper=core_api_client_wrapper)
        self.slack_team_id = slack_team_id
        self.slack_channel_id = slack_channel_id
        self.original_poster_slack_user_id = original_poster_slack_user_id
        self.slack_message_ts = slack_message_ts

    def execute(self):
        slack_command = SaveMessageAsTopicCommand(slack_client_wrapper=self.slack_client_wrapper,
                                                  core_api_client_wrapper=self.core_api_client_wrapper,
                                                  slack_team_id=self.slack_team_id,
                                                  slack_channel_id=self.slack_channel_id,
                                                  original_poster_slack_user_id=self.original_poster_slack_user_id,
                                                  slack_message_ts=self.slack_message_ts)
        Thread(target=slack_command.execute, daemon=True).start()
