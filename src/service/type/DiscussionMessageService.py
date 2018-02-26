from threading import Thread

from src.command.ForwardMessageCommand import ForwardMessageCommand
from src.domain.models.slack.unpersisted.DiscussionMessage import DiscussionMessage
from src.service.Service import Service
from src.service.subservice.MessageFilePublicizer import MessageFilePublicizer
from src.service.subservice.MessageTextFormatter import MessageTextFormatter


class DiscussionMessageService(Service):
    """
        event_request in constructor must represent a discussion message

        Actions:
        * Convert Slack attachments (files) to text w/ public file URLS
        * Normalize Slack markup to readable markup

        Outputs:
        * Request to Portal (Message/Reply, User)

        Normalize Message's text & attachments, forward them to the Portal
    """

    def __init__(self, slack_client_wrapper, portal_client_wrapper, event_request):
        # TODO [SLA-81] assert event_request.is_discussion_message
        super().__init__(slack_client_wrapper=slack_client_wrapper, portal_client_wrapper=portal_client_wrapper)
        self.event_request = event_request

    def execute(self):
        slack_team_id = self.event_request.team_id
        discussion_message = DiscussionMessage(**self.event_request.event.__dict__)
        if discussion_message.subtype == 'file_share':
            file_publicizer = MessageFilePublicizer(event=self.event_request.event,
                                                    slack_client_wrapper=self.slack_client_wrapper,
                                                    slack_team_id=slack_team_id)
            file_url = file_publicizer.publicize_file()
            discussion_message.file_url = file_url
        text_formatter = MessageTextFormatter(discussion_message=discussion_message)
        discussion_message.text = text_formatter.format_text()
        command = ForwardMessageCommand(slack_client_wrapper=self.slack_client_wrapper,
                                        portal_client_wrapper=self.portal_client_wrapper,
                                        team_id=self.event_request.team_id,
                                        event=self.event_request.event)
        Thread(target=command.execute, daemon=True).start()
