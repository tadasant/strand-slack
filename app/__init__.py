from flask import Flask
from app import factory, slack

app = Flask(__name__)

app.register_blueprint(factory.blueprint, url_prefix='/factory')
app.register_blueprint(slack.blueprint, url_prefix='/slack')
