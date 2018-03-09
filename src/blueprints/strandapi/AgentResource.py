from flask import request

from src.blueprints.strandapi.StrandApiResource import CoreApiResource
# from src.models.domain.Agent import AgentSchema


class AgentResource(CoreApiResource):

    @CoreApiResource.authenticate
    def put(self):
        """Used for UPDATING a Agent"""
        args = request.get_json()
        # slack_agent = AgentSchema().load(args).data
        # former_slack_agent = slack_agent_repository.get_slack_agent(slack_team_id=slack_agent.slack_team.id)
        # slack_agent_repository.set_slack_agent(slack_agent)

        # if former_slack_agent.slack_application_installation != slack_agent.slack_application_installation:
        # presumably, this was an oauth update, so we're re-sending the onboarding message
        # InitiateAgentOnboardingCommand(
        #     slack_client_wrapper=current_app.slack_client_wrapper,
        #     slack_team_id=slack_agent.slack_team.id,
        #     installer_id=slack_agent.slack_application_installation.installer.id
        # ).execute()

        # return AgentSchema().dump(slack_agent)

    @CoreApiResource.authenticate
    def post(self):
        """Used for CREATING a Agent"""
        args = request.get_json()
        # slack_agent = AgentSchema().load(args).data
        # slack_agent_repository.add_slack_agent(slack_agent)
        #
        # InitiateAgentOnboardingCommand(slack_client_wrapper=current_app.slack_client_wrapper,
        #                                slack_team_id=slack_agent.slack_team.id,
        #                                installer_id=slack_agent.slack_application_installation.installer.id).execute()

        # return AgentSchema().dump(slack_agent)
