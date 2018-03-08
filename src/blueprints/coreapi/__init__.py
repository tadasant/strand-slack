from flask import Blueprint
from flask_restful import Api

from src.blueprints.coreapi.DiscussionStatusResource import ClosedDiscussionStatusResource, \
    StaleDiscussionStatusResource
from src.blueprints.coreapi.SlackAgentResource import SlackAgentResource

blueprint = Blueprint('coreapi', __name__)
api = Api(blueprint)

api.add_resource(SlackAgentResource, '/slackagents')
api.add_resource(StaleDiscussionStatusResource, '/discussions/stale')
api.add_resource(ClosedDiscussionStatusResource, '/discussions/closed')
