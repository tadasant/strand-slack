from flask import current_app, request
from flask_restful import Resource

from src.domain.repositories.SlackAgentRepository import slack_agent_repository
from src.command.OnboardTeam import OnboardTeam
from src.domain.models.SlackAgent import SlackAgentSchema


class SlackAgentResource(Resource):
    def put(self):
        args = request.get_json()
        slack_agent = SlackAgentSchema().load(args).data
        slack_agent_repository.set_slack_agent(slack_agent)

    def post(self):
        args = request.get_json()
        slack_agent = SlackAgentSchema().load(args).data
        slack_agent_repository.add_slack_agent(slack_agent)

        # POST means append, so assuming we need to onboard
        OnboardTeam(slack_client_wrapper=current_app.slack_client_wrapper,
                    team_id=slack_agent.slack_team.id,
                    installer_id=slack_agent.slack_application_installation.installer.id).execute()

        return SlackAgentSchema().dump(slack_agent)
