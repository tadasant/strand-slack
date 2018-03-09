from flask import Blueprint
from flask_restful import Api

from src.blueprints.strandapi.AgentResource import AgentResource

blueprint = Blueprint('strandapi', __name__)
api = Api(blueprint)

api.add_resource(AgentResource, '/strandapi')
