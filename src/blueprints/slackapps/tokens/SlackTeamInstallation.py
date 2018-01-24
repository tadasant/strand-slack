import json

from flask import current_app
from flask_restful import Resource, reqparse, abort

from src.blueprints.slackapps import api

# TODO consider formally modelling SlackTeamInstallation with e.g. SQLAlchemy (use in-memory DB) -- scrap SlackTokens
from src.command.OnboardTeam import OnboardTeam
from src.models.namedtuples import SlackTokens


class SlackTeamInstallation(Resource):
    # TODO we'll want a put() for updating -- then post() should throw if exists
    def post(self):
        # TODO flask restful's request parsing is deprecated. Migrate to marshmallow.
        parser = reqparse.RequestParser()
        parser.add_argument('bot_access_token', required=True, location='form', help='Need bot_access_token')
        parser.add_argument('access_token', required=True, location='form', help='Need access_token')
        parser.add_argument('slack_team', required=True, location='form', help='Need slack_team with id')
        parser.add_argument('is_active', location='form', help='is_active is optional, defaults to false')
        parser.add_argument('installer_id', location='form', help='If is_active is true, not needed')
        args = parser.parse_args()
        if not args['is_active'] and not args['installer_id']:
            abort(400, message=['Installation is not active: we need installer_id'])
        if 'id' not in args['slack_team']:
            abort(400, message=['slack_team must contain id'])
        tokens = SlackTokens(bot_access_token=args['bot_access_token'], access_token=['access_token'])
        current_app.slack_client_wrapper.set_tokens(tokens=tokens, team_id=args['slack_team']['id'])
        if not args['is_active']:
            OnboardTeam(slack_client_wrapper=current_app.slack_client_wrapper,
                        team_id=args['slack_team']['id'],
                        installer_id=args['installer_id']).execute()
        return json.dumps(tokens._asdict())


api.add_resource(SlackTeamInstallation, '/slackteaminstallation')
