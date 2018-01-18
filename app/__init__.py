from flask import Flask
from app.factory import blueprint as factory_blueprint
from app.slack import blueprint as slack_blueprint

app = Flask(__name__)

app.register_blueprint(factory_blueprint, url_prefix='/factory')
app.register_blueprint(slack_blueprint, url_prefix='/slack')
