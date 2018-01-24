from flask import Blueprint
from flask_restful import Api

blueprint = Blueprint('hooks', __name__)
api = Api(blueprint)
