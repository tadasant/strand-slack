from threading import Thread

from src.command.ForwardMessageCommand import ForwardMessageCommand
from src.domain.models.slack.unpersisted.DiscussionMessage import DiscussionMessage
from src.service.Service import Service
from src.service.discussionmessage.DiscussionMessageTextFormatter import DiscussionMessageTextFormatter


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
        # def _get_file_public_permalink(self, file_id):
        #     if self._message.get('file').get('public_url_shared'):
        #         public_permalink = self._message.get('file').get('permalink_public')
        #     else:
        #         shared_file = self._slack_client.api_call('files.sharedPublicURL', file=file_id).get('file')
        #         public_permalink = shared_file.get('permalink_public')
        #     return public_permalink
        #
        # Handle file uploads
        # if self._sub_type == 'file_share':
        #     file_id = self._message.get('file').get('id')
        #     public_permalink = self._get_file_public_permalink(file_id)
        #     text = re.sub('(https):(.*?)\|', public_permalink + '|', text)
        # TODO make files public (if any) & pass them to the parser (via DiscussionMessage object)
        # TODO include subtype on Event
        # TODO Parse the message text
        discussion_message = DiscussionMessage(**self.event_request.event.__dict__)
        text_formatter = DiscussionMessageTextFormatter(discussion_message=discussion_message)
        discussion_message.text = text_formatter.format_text()
        command = ForwardMessageCommand(slack_client_wrapper=self.slack_client_wrapper,
                                        portal_client_wrapper=self.portal_client_wrapper,
                                        team_id=self.event_request.team_id,
                                        event=self.event_request.event)
        Thread(target=command.execute, daemon=True).start()
