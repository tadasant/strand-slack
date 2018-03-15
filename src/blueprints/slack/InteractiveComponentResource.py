import json
from http import HTTPStatus
from threading import Thread

from flask import request, current_app

from src.blueprints.slack.SlackResource import SlackResource
from src.models.slack.requests.SlackInteractiveComponentRequest import InteractiveComponentRequestSchema
from src.translators.SlackInteractiveComponentTranslator import SlackInteractiveComponentTranslator


class InteractiveComponentResource(SlackResource):

    @SlackResource.authenticate
    def post(self):
        """Receive an interactive component (e.g. menu, dialog box) payload"""
        self.logger.info(f'Processing InteractiveComponent request: {request.__dict__}')
        payload = json.loads(request.form['payload'])
        interactive_component_request = InteractiveComponentRequestSchema().load(payload).data
        translator = SlackInteractiveComponentTranslator(
            slack_interactive_component_request=interactive_component_request,
            slack_client_wrapper=current_app.slack_client_wrapper,
            strand_api_client_wrapper=current_app.strand_api_client_wrapper
        )
        Thread(target=translator.translate, daemon=True).start()
        return {}, HTTPStatus.OK
