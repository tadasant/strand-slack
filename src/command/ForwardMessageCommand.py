import re

from src.command.Command import Command
from src.domain.models.exceptions.WrapperException import WrapperException


class ForwardMessageCommand(Command):
    def __init__(self, slack_client_wrapper, portal_client_wrapper, slack_team_id, message, event_item):
        super().__init__(slack_client_wrapper=slack_client_wrapper, portal_client_wrapper=portal_client_wrapper,
                         slack_team_id=slack_team_id)
        self.message = message
        # TODO [CCS-81] won't need event_item in this command after refactoring
        self.event_item = event_item

    def execute(self):
        """Forward message onward to the portal for storage"""
        log_message = f'Executing ForwardMessageCommand for {self.slack_team_id} with message {self.message}'
        self.logger.info(log_message)
        if self._is_discussion_message():
            try:
                pass
                # forward message
            except WrapperException as e:
                self.logger.error(f'Failed to store message. {self.event_item} {self.message}')
                raise e

        self.slack_client_wrapper.post_to_response_url(response_url=self.response_url, payload=response_payload)

    def _is_discussion_message(self):
        # TODO [CCS-81] This check should happen via db prior to this command's execution
        calling_channel_id = self.event_item.channel
        calling_channel_info = self.slack_client_wrapper.get_channel_info(slack_team_id=self.slack_team_id,
                                                                          slack_channel_id=calling_channel_id)
        calling_channel_name = calling_channel_info['name']
        return re.fullmatch(pattern=r'discussions-(\d+)', string=calling_channel_name) is not None
