from flask import Blueprint
from flask_restful import Api

from src.blueprints.slack.InteractiveComponentResource import InteractiveComponentResource

blueprint = Blueprint('slack', __name__)
api = Api(blueprint)

api.add_resource(InteractiveComponentResource, '/interactivecomponents')
