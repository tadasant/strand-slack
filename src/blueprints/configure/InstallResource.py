from http import HTTPStatus
from threading import Thread

from flask import request, current_app
from flask_restful import Resource

from src.translators.InstallTranslator import InstallTranslator


class InstallResource(Resource):
    def post(self):
        """Receive installation requests from the Strand UI"""
        args = request.get_json()
        # Intentional: Omitting schema validation due to simplicity
        if 'code' in args:
            translator = InstallTranslator(code=args['code'],
                                           slack_client_wrapper=current_app.slack_client_wrapper,
                                           strand_api_client_wrapper=current_app.strand_api_client_wrapper)
            Thread(target=translator.translate, daemon=True).start()
            # TODO Wait until DB has new entry or timeout. Future optimization: replace with socket.
            return {}, HTTPStatus.OK
        return {'error': 'No code in request body'}, HTTPStatus.BAD_REQUEST
