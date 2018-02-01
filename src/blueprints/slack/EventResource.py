from http import HTTPStatus

from flask import request

from src.blueprints.slack.SlackResource import SlackResource
from src.domain.models.slack.requests.EventRequest import EventRequestSchema


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
            #  determine if it's relevant
            pass
        return {}, HTTPStatus.OK
