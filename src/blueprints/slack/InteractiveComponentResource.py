from flask import current_app, request
from flask_restful import Resource

from src.command.messages.onboarding_dm import ONBOARDING_DM
from src.domain.repositories.SlackAgentRepository import slack_agent_repository
from src.command.OnboardTeam import OnboardTeam
from src.domain.models.portal.SlackAgent import SlackAgentSchema


class InteractiveComponentResource(Resource):
    def post(self):
        """Used for receiving an interactive menu payload"""
        payload = request.form['payload']
        if payload['type'] == 'interactive_message' and payload['callback_id'] == ONBOARDING_DM.callback_id:

            #Do command
            pass
        args = request.get_json()
        slack_agent = SlackAgentSchema().load(args).data
        slack_agent_repository.add_slack_agent(slack_agent)

        OnboardTeam(slack_client_wrapper=current_app.slack_client_wrapper,
                    team_id=slack_agent.slack_team.id,
                    installer_id=slack_agent.slack_application_installation.installer.id).execute()

        return SlackAgentSchema().dump(slack_agent)
