from flask import Flask
from app import factory, slack
from app.exceptions import BotAlreadyExists, handle_bot_already_exists_usage


def create_app():
    app = Flask(__name__)

    app.register_blueprint(factory.blueprint, url_prefix='/factory')
    app.register_blueprint(slack.blueprint, url_prefix='/slack')

    app.register_error_handler(BotAlreadyExists, handle_bot_already_exists_usage)

    return app
