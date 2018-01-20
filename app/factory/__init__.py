from flask import Blueprint
from flask_restful import Api, Resource, reqparse

from app.factory.Factory import Factory
from app.factory.bot.BotSettings import BotSettings

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
        bot_settings = BotSettings(SLACK_TEAM_NAME=args.get('SLACK_TEAM_NAME'),
                                   SLACK_TEAM_ID=args.get('SLACK_TEAM_ID'),
                                   ACCESS_TOKEN=args.get('ACCESS_TOKEN'),
                                   INSTALLER_ID=args.get('INSTALLER_ID'),
                                   BOT_USER_ID=args.get('BOT_USER_ID'),
                                   BOT_ACCESS_TOKEN=args.get('BOT_ACCESS_TOKEN'))
        bot = factory.create_bot(bot_settings)
        return bot.as_dict(), 201


api.add_resource(BotList, '/bots')
