from flask import Flask, jsonify
from app import factory, slack
from app.exceptions import BotAlreadyExists


def create_app():
    app = Flask(__name__)

    app.register_blueprint(factory.blueprint, url_prefix='/factory')
    app.register_blueprint(slack.blueprint, url_prefix='/slack')

    return app
