from flask import Blueprint
from flask_restful import Api, Resource

blueprint = Blueprint('factory', __name__)
api = Api(blueprint)


class BotList(Resource):
    def get(self):
        return []

    def post(self):
        return {}


api.add_resource(BotList, '/bots')
