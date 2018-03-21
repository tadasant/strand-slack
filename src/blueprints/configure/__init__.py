from flask import Blueprint
from flask_restful import Api

from src.blueprints.configure.InstallResource import InstallResource

blueprint = Blueprint('configure', __name__)
api = Api(blueprint)

api.add_resource(InstallResource, '/install')
