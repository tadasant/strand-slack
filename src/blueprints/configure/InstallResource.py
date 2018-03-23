from http import HTTPStatus
from threading import Thread

from flask import request, current_app, redirect
from flask_restful import Resource

from src.config import config
from src.translators.InstallTranslator import InstallTranslator
from src.utilities.logging import get_logger


class InstallResource(Resource):
    def __init__(self):
        self.logger = get_logger(self.__class__.__name__)

    def get(self):
        """Redirect the user to the Slack OAuth flow"""
        return redirect(f'https://slack.com/oauth/authorize?client_id={config["CLIENT_ID"]}&scope={config["SCOPES"]}')

    def post(self):
        """Receive installation requests from the Strand UI"""
        args = request.get_json()
        self.logger.debug(f'Received Install request: {args}')
        # Intentional: Omitting schema validation due to simplicity
        if 'code' in args:
            translator = InstallTranslator(code=args['code'],
                                           slack_client_wrapper=current_app.slack_client_wrapper,
                                           strand_api_client_wrapper=current_app.strand_api_client_wrapper)
            Thread(target=translator.translate, daemon=True).start()
            # TODO Wait until DB has new entry or timeout. Future optimization: replace with socket.
            return {}, HTTPStatus.OK
        return {'error': 'No code in request body'}, HTTPStatus.BAD_REQUEST
