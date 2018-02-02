from http import HTTPStatus
from threading import Thread

from flask import request, current_app

from src.blueprints.slack.SlackResource import SlackResource
from src.command.ForwardMessageCommand import ForwardMessageCommand
from src.domain.models.slack.requests.EventRequest import EventRequestSchema
from src.domain.repositories.SlackAgentRepository import slack_agent_repository


class EventResource(SlackResource):
    def post(self):
        """Receive events for which we are registered from Slack (Events API)"""
        result = ({}, HTTPStatus.OK)
        try:
            self.logger.info(f'Processing Event request: {request.get_json()}')
            payload = request.get_json()
            self._authenticate(payload)
            event_request = EventRequestSchema().load(payload).data
            if event_request.is_verification_request:
                result = ({'challenge': event_request.challenge}, HTTPStatus.OK)
            elif event_request.event and event_request.event.is_message_channels_event:
                discuss_channel_id = slack_agent_repository.get_discuss_channel_id(slack_team_id=event_request.team_id)
                if event_request.event.item.channel == discuss_channel_id:
                    self.logger.info('Detected message in #discuss channel')
                    # TODO [CCS-75] Command to delete non-clippy #discuss channel messages
                    # command = None
                    # Thread(target=command.execute, daemon=True).start()
                else:
                    # TODO [CCS-81] Check whether or not this is #discussions-X vs. other should happen here via db
                    self.logger.info('Message in non-discuss channel')
                    command = ForwardMessageCommand(slack_client_wrapper=current_app.slack_client_wrapper,
                                                    portal_client_wrapper=current_app.portal_client_wrapper,
                                                    slack_team_id=event_request.team_id,
                                                    message_item=event_request.event.item)
                    Thread(target=command.execute, daemon=True).start()
        finally:
            # Slack will keep re-sending if we don't respond 200 OK, even in exception case on our end
            return result
