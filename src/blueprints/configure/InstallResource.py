from http import HTTPStatus
from threading import Thread

from flask import request
from flask_restful import Resource

from src.translators.InstallTranslator import InstallTranslator


class InstallResource(Resource):
    def post(self):
        """Receive installation requests from the Strand UI"""
        args = request.get_json()
        # Intentional: Omitting schema validation due to simplicity
        if 'code' in args:
            install_translator = InstallTranslator(code=args['code'])
            Thread(target=install_translator.translate, daemon=True).start()
            # TODO Wait until DB has new entry or timeout. Future optimization: replace with socket.
            return {}, HTTPStatus.OK
        return {'error': 'No code in request body'}, HTTPStatus.BAD_REQUEST
