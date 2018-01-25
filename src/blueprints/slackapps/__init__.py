from flask import Blueprint
from flask_restful import Api

from src.blueprints.slackapps.agents.SlackAgentResource import SlackAgentResource

blueprint = Blueprint('portal', __name__)
api = Api(blueprint)

api.add_resource(SlackAgentResource, '/agents')
