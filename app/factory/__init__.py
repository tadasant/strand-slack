from flask import Blueprint
from flask_restful import Api, Resource, reqparse

from app.factory.Factory import Factory

blueprint = Blueprint('factory', __name__)
api = Api(blueprint)
factory = Factory()


class BotList(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('slack_team_id', type=str, required=True)
        self.post_parser.add_argument('slack_team_name', type=str, required=True)
        self.post_parser.add_argument('access_token', type=str, required=True)
        self.post_parser.add_argument('installer_id', type=str, required=True)
        self.post_parser.add_argument('bot_user_id', type=str, required=True)
        self.post_parser.add_argument('bot_access_token', type=str, required=True)

    def get(self):
        return []

    def post(self):
        args = self.post_parser.parse_args()
        factory.create_bot(**args)
        return {'created': True}, 201


api.add_resource(BotList, '/bots')
