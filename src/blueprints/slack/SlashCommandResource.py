from http import HTTPStatus
from threading import Thread

from flask import request, current_app

from src.blueprints.slack.SlackResource import SlackResource
from src.models.slack.requests.SlackSlashCommandRequest import SlashCommandRequestSchema, \
    SlackSlashCommandRequest
from src.translators.SlackSlashCommandTranslator import SlackSlashCommandTranslator


class SlashCommandResource(SlackResource):

    @SlackResource.authenticate
    def post(self):
        """Receive a slash command (e.g. /strand save 10:59 PM) payload"""
        self.logger.info(f'Processing slash command request: {request.get_json()}')
        payload = request.form
        slash_command_request: SlackSlashCommandRequest = SlashCommandRequestSchema().load(payload).data
        translator = SlackSlashCommandTranslator(
            slack_slash_command_request=slash_command_request,
            slack_client_wrapper=current_app.slack_client_wrapper,
            strand_api_client_wrapper=current_app.strand_api_client_wrapper
        )
        Thread(target=translator.translate, daemon=True).start()
        return None, HTTPStatus.NO_CONTENT
