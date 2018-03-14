from http import HTTPStatus
from threading import Thread

from flask import request, current_app

from src.blueprints.slack.SlackResource import SlackResource
from src.models.slack.requests.SlackEventRequest import SlackEventRequestSchema
from src.translators.SlackEventTranslator import SlackEventTranslator


class EventResource(SlackResource):

    @SlackResource.authenticate
    def post(self):
        """Receive events for which we are registered from Slack (Events API)"""
        result = ({}, HTTPStatus.OK)
        try:
            self.logger.info(f'Processing Event request: {request.get_json()}')
            payload = request.get_json()
            slack_event_request = SlackEventRequestSchema().load(payload).data
            if slack_event_request.is_verification_request:
                result = ({'challenge': slack_event_request.challenge}, HTTPStatus.OK)
            elif slack_event_request.event and slack_event_request.event.is_message_dm_event:
                self.logger.info('Processing DM')
                translator = SlackEventTranslator(slack_event_request=slack_event_request,
                                                  slack_client_wrapper=current_app.slack_client_wrapper,
                                                  strand_api_client_wrapper=current_app.strand_api_client_wrapper)
                Thread(target=translator.translate, daemon=True).start()
        finally:
            # Slack will keep re-sending if we don't respond 200 OK, even in exception case on our end
            return result
