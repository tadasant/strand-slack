from threading import Thread

from src.command.DeleteTopicChannelMessageCommand import DeleteTopicChannelMessageCommand
from src.command.InformTopicChannelMessageDeletedCommand import InformTopicChannelMessageDeletedCommand
from src.service.Service import Service


class TopicChannelMessageService(Service):
    """
        event_request in constructor must represent a topic channel message

        Actions:
        * Delete the message if it's not from the bot
        * DM the user that they can't post there
    """

    def __init__(self, slack_client_wrapper, portal_client_wrapper, event_request, bot_user_id):
        # TODO [CCS-81] assert event_request.is_topic_channel_message
        super().__init__(slack_client_wrapper=slack_client_wrapper, portal_client_wrapper=portal_client_wrapper)
        self.event_request = event_request
        self.bot_user_id = bot_user_id

    def execute(self):
        if self.event_request.event.user != self.bot_user_id:
            self.logger.info('Detected non-bot message in topic channel')
            delete_command = DeleteTopicChannelMessageCommand(
                slack_client_wrapper=self.slack_client_wrapper,
                slack_team_id=self.event_request.team_id,
                slack_channel_id=self.event_request.event.channel,
                message_ts=self.event_request.event.ts,
            )
            Thread(target=delete_command.execute, daemon=True).start()
            if not self.event_request.event.is_system_message:
                self.logger.info('Detected that this message was not sent by the system')
                inform_command = InformTopicChannelMessageDeletedCommand(
                    slack_client_wrapper=self.slack_client_wrapper,
                    slack_team_id=self.event_request.team_id,
                    slack_user_id=self.event_request.event.user,
                    attempted_text=self.event_request.event.text
                )
                Thread(target=inform_command.execute, daemon=True).start()
