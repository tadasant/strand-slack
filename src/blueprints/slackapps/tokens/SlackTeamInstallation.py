import json

from flask import current_app
from flask_restful import Resource, reqparse, abort

# TODO consider formally modelling SlackTeamInstallation with e.g. SQLAlchemy (use in-memory DB) -- scrap SlackTokens
from src.command.OnboardTeam import OnboardTeam
from src.models.namedtuples import SlackTokens


class SlackTeamInstallation(Resource):
    def get(self):
        return 'Hello world!'

    # TODO we'll want a put() for updating -- then post() should raise error if exists
    def post(self):
        # TODO flask restful's request parsing is deprecated. Migrate to marshmallow.
        parser = reqparse.RequestParser()
        parser.add_argument('bot_access_token', required=True, help='Need bot_access_token')
        parser.add_argument('access_token', required=True, help='Need access_token')
        parser.add_argument('slack_team_id', required=True, help='Need slack_team_id')
        parser.add_argument('is_active', type=bool, help='is_active is optional, defaults to false')
        parser.add_argument('installer_id', help='If is_active is true, not needed')
        args = parser.parse_args()
        if not args['is_active'] and not args['installer_id']:
            abort(400, message=['Installation is not active: we need installer_id'])
        tokens = SlackTokens(bot_access_token=args['bot_access_token'], access_token=args['access_token'])
        current_app.slack_client_wrapper.set_tokens(tokens=tokens, team_id=args['slack_team_id'])
        if not args['is_active']:
            OnboardTeam(slack_client_wrapper=current_app.slack_client_wrapper,
                        team_id=args['slack_team_id'],
                        installer_id=args['installer_id']).execute()
        return tokens._asdict()
