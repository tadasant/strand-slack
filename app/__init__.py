from flask import Flask, jsonify
from app import factory, slack
from app.exceptions import BotAlreadyExists

app = Flask(__name__)

app.register_blueprint(factory.blueprint, url_prefix='/factory')
app.register_blueprint(slack.blueprint, url_prefix='/slack')


@app.errorhandler(BotAlreadyExists)
def handle_bot_already_exists_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
