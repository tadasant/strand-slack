from src.command.Command import Command
from src.command.model.message.messages import STALE_DISCUSSION_MESSAGE


class MarkDiscussionPendingClosed(Command):
    """Send a message to the channel and then (if no exceptions) inform the Portal that it is done"""

    def __init__(self, slack_client_wrapper, portal_client_wrapper, slack_team_id, slack_channel_id):
        super().__init__(slack_client_wrapper=slack_client_wrapper, portal_client_wrapper=portal_client_wrapper,
                         slack_team_id=slack_team_id)
        self.slack_channel_id = slack_channel_id

    def execute(self):
        log_msg = f'Executing MarkDiscussionPendingClosed for {self.slack_team_id} with channel ' \
                  f'{self.slack_channel_id}'
        self.logger.info(log_msg)
        self.slack_client_wrapper.send_message(slack_team_id=self.slack_team_id, slack_channel_id=self.slack_channel_id,
                                               text=STALE_DISCUSSION_MESSAGE.text)
        self.portal_client_wrapper.mark_discussion_as_pending_closed(slack_channel_id=self.slack_channel_id)