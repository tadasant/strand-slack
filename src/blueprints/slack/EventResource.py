from http import HTTPStatus
from threading import Thread

from flask import request, current_app

from src.blueprints.slack.SlackResource import SlackResource
from src.models.slack.requests.SlackEventRequest import EventRequestSchema
from src.services.parent.ProvideHelpService import ProvideHelpService


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
            elif event_request.event and event_request.event.is_message_dm_event:
                self.logger.info('Processing help message in DM')
                service = ProvideHelpService(slack_client_wrapper=current_app.slack_client_wrapper,
                                             slack_team_id=event_request.team_id,
                                             slack_user_id=event_request.event.user,
                                             slack_channel_id=event_request.event.channel)
                Thread(target=service.execute, daemon=True).start()
        finally:
            # Slack will keep re-sending if we don't respond 200 OK, even in exception case on our end
            return result
