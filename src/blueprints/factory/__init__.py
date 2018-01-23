from flask import Blueprint
from flask_restful import Api, Resource, reqparse

from src.blueprints.factory.Factory import Factory
from src.blueprints.factory.bot.BotSettings import BotSettings

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
        return factory.get_bots(), 200

    def post(self):
        args = self.post_parser.parse_args()

        bot_settings = BotSettings(**args)
        bot = factory.create_bot(bot_settings)

        return bot.as_dict(), 201


api.add_resource(BotList, '/bots')