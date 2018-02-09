from flask import Blueprint
from flask_restful import Api

from src.blueprints.portal.DiscussionStatusResource import ClosedDiscussionStatusResource, StaleDiscussionStatusResource
from src.blueprints.portal.SlackAgentResource import SlackAgentResource

blueprint = Blueprint('portal', __name__)
api = Api(blueprint)

api.add_resource(SlackAgentResource, '/slackagents')
api.add_resource(StaleDiscussionStatusResource, '/discussions/stale')
api.add_resource(ClosedDiscussionStatusResource, '/discussions/closed')
