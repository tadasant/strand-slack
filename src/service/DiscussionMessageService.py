from threading import Thread

from src.command.ForwardMessageCommand import ForwardMessageCommand
from src.service.Service import Service


class DiscussionMessageService(Service):
    """
        event_request in constructor must represent a discussion message

        Actions:
        * Convert Slack markup to readable markup
        * Convert Slack attachments (files) to text w/ public file URLS

        Outputs:
        * Request to Portal (Message/Reply, User)

        Normalize Message's text & attachments, create
    """

    def __init__(self, slack_client_wrapper, portal_client_wrapper, event_request):
        # TODO [CCS-81] assert event_request.is_discussion_message
        super().__init__(slack_client_wrapper=slack_client_wrapper, portal_client_wrapper=portal_client_wrapper)
        self.event_request = event_request

    def execute(self):
        # Parse the message text
        # Handle files
        command = ForwardMessageCommand(slack_client_wrapper=self.slack_client_wrapper,
                                        portal_client_wrapper=self.portal_client_wrapper,
                                        team_id=self.event_request.team_id,
                                        event=self.event_request.event)
        Thread(target=command.execute, daemon=True).start()
