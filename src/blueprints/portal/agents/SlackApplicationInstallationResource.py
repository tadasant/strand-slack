from flask import current_app, request
from flask_restful import Resource

from src.command.OnboardTeam import OnboardTeam
from src.domain.models import SlackApplicationInstallationSchema


class SlackApplicationInstallationResource(Resource):
    # TODO we'll want a patch/put for updating (w/ no onboard) -- and post() should raise error if already exists
    def post(self):
        args = request.get_json()
        installation = SlackApplicationInstallationSchema().load(args).data
        current_app.slack_client_wrapper.set_installation(installation=installation, team_id=installation.slack_team.id)
        if not installation.is_active:
            OnboardTeam(slack_client_wrapper=current_app.slack_client_wrapper,
                        team_id=installation.slack_team.id,
                        installer_id=installation.installer.id).execute()
        return SlackApplicationInstallationSchema().dump(installation)
