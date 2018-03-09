from flask import Blueprint
from flask_restful import Api

from src.blueprints.coreapi.SlackAgentResource import SlackAgentResource

blueprint = Blueprint('coreapi', __name__)
api = Api(blueprint)

api.add_resource(SlackAgentResource, '/slackagents')
