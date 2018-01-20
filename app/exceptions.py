from flask import jsonify


class BotAlreadyExists(Exception):
    status_code = 400

    def __init__(self, message='Bot already exists for this slack team', status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


def handle_bot_already_exists_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
