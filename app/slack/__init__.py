from flask import Blueprint
from flask_restful import Api

blueprint = Blueprint('slack', __name__)
api = Api(blueprint)
