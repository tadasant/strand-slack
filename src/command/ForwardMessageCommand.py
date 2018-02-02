import re

from src.command.Command import Command
from src.domain.models.exceptions.WrapperException import WrapperException


class ForwardMessageCommand(Command):
    def __init__(self, slack_client_wrapper, portal_client_wrapper, slack_team_id, slack_event):
        super().__init__(slack_client_wrapper=slack_client_wrapper, portal_client_wrapper=portal_client_wrapper,
                         slack_team_id=slack_team_id)
        self.slack_event = slack_event

    def execute(self):
        """Forward message onward to the portal for storage"""
        log_message = f'Executing ForwardMessageCommand for {self.slack_team_id} with message {self.slack_event}'
        self.logger.info(log_message)
        if self._is_discussion_message():
            try:
                if self.slack_event.is_reply:
                    self.portal_client_wrapper.create_reply(text=self.slack_event.text,
                                                            slack_channel_id=self.slack_event.channel,
                                                            slack_event_ts=self.slack_event.ts,
                                                            slack_thread_ts=self.slack_event.thread_ts,
                                                            author_slack_user_id=self.slack_event.user)
                else:
                    # regular message
                    self.portal_client_wrapper.create_message(text=self.slack_event.text,
                                                              slack_channel_id=self.slack_event.channel,
                                                              slack_event_ts=self.slack_event.ts,
                                                              author_slack_user_id=self.slack_event.user)
            except WrapperException as e:
                self.logger.error(f'Failed to store message: {self.slack_event}')
                raise e

    def _is_discussion_message(self):
        # TODO [CCS-81] This check should happen via db prior to this command's execution
        calling_channel_id = self.slack_event.channel
        calling_channel_info = self.slack_client_wrapper.get_channel_info(slack_team_id=self.slack_team_id,
                                                                          slack_channel_id=calling_channel_id)
        calling_channel_name = calling_channel_info['name']
        return re.fullmatch(pattern=r'discussion-(\d+)', string=calling_channel_name) is not None
