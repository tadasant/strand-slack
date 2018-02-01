from http import HTTPStatus

from flask import request

from src.blueprints.slack.SlackResource import SlackResource
from src.domain.models.slack.requests.EventRequest import EventRequestSchema
from src.domain.repositories.SlackAgentRepository import slack_agent_repository


class EventResource(SlackResource):
    def post(self):
        """Receiving an event from Slack"""
        self.logger.info(f'Processing Event request: {request}')
        payload = request.json
        self._authenticate(payload)
        event_request = EventRequestSchema().load(payload).data
        if event_request.is_verification_request:
            return event_request.challenge, HTTPStatus.OK
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
                # TODO [CCS-71] Command to forward messages to portal
                # command = None
                # Thread(target=command.execute, daemon=True).start()
        return {}, HTTPStatus.OK
