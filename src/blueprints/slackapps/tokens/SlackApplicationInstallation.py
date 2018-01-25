from flask import current_app
from flask_restful import Resource, reqparse, abort

from src.command.OnboardTeam import OnboardTeam


class SlackApplicationInstallation(Resource):
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('bot_access_token', required=True, help='Need bot_access_token')
        self.post_parser.add_argument('access_token', required=True, help='Need access_token')
        self.post_parser.add_argument('slack_team_id', required=True, help='Need slack_team_id')
        self.post_parser.add_argument('is_active', type=bool, help='is_active is optional, defaults to false')
        self.post_parser.add_argument('installer_id', help='If is_active is true, not needed')

    # TODO we'll want a put() for updating -- then post() should raise error if exists
    def post(self):
        # TODO flask restful's request parsing is deprecated. Migrate to marshmallow.
        args = self._parse_post_args()
        tokens = SlackTokens(bot_access_token=args['bot_access_token'], access_token=args['access_token'])
        current_app.slack_client_wrapper.set_tokens(tokens=tokens, team_id=args['slack_team_id'])
        if not args['is_active']:
            OnboardTeam(slack_client_wrapper=current_app.slack_client_wrapper,
                        team_id=args['slack_team_id'],
                        installer_id=args['installer_id']).execute()
        return tokens._asdict()

    def _parse_post_args(self):
        args = self.post_parser.parse_args()
        if not args['is_active'] and not args['installer_id']:
            abort(400, message=['Installation is not active: we need installer_id'])
        return args
