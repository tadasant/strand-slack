from flask import current_app, request

from src.blueprints.portal.PortalResource import PortalResource
from src.command.InitiateAgentOnboardingCommand import InitiateAgentOnboardingCommand
from src.domain.models.portal.SlackAgent import SlackAgentSchema
from src.domain.repositories.SlackAgentRepository import slack_agent_repository


class SlackAgentResource(PortalResource):

    @PortalResource.authenticate
    def put(self):
        """Used for UPDATING a SlackAgent"""
        args = request.get_json()
        slack_agent = SlackAgentSchema().load(args).data
        slack_agent_repository.set_slack_agent(slack_agent)

        # TODO [CCS-28] probably want a different message the second time around
        InitiateAgentOnboardingCommand(slack_client_wrapper=current_app.slack_client_wrapper,
                                       slack_team_id=slack_agent.slack_team.id,
                                       installer_id=slack_agent.slack_application_installation.installer.id).execute()

        return SlackAgentSchema().dump(slack_agent)

    @PortalResource.authenticate
    def post(self):
        """Used for CREATING a SlackAgent"""
        args = request.get_json()
        slack_agent = SlackAgentSchema().load(args).data
        slack_agent_repository.add_slack_agent(slack_agent)

        InitiateAgentOnboardingCommand(slack_client_wrapper=current_app.slack_client_wrapper,
                                       slack_team_id=slack_agent.slack_team.id,
                                       installer_id=slack_agent.slack_application_installation.installer.id).execute()

        return SlackAgentSchema().dump(slack_agent)
