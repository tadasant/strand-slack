import re

from flask import current_app, request
from flask_restful import Resource

from src.command.InitiateAgentOnboardingCommand import InitiateAgentOnboardingCommand
from src.domain.models.exceptions.UnauthorizedException import UnauthorizedException
from src.domain.models.portal.SlackAgent import SlackAgentSchema
from src.domain.repositories.SlackAgentRepository import slack_agent_repository


def authenticate_portal(func):
    token_regex = r'Token (.*)'

    def wrapper(*args, **kwargs):
        authorization_header = request.headers['Authorization']
        if authorization_header:
            matches = re.findall(token_regex, authorization_header)
            if len(matches) == 1:
                token = matches[0]
                if token == current_app.portal_verification_token:
                    return func(*args, **kwargs)
        raise UnauthorizedException(message='Portal authorization failed.')

    return wrapper


class SlackAgentResource(Resource):

    @authenticate_portal
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

    @authenticate_portal
    def post(self):
        """Used for CREATING a SlackAgent"""
        args = request.get_json()
        slack_agent = SlackAgentSchema().load(args).data
        slack_agent_repository.add_slack_agent(slack_agent)

        InitiateAgentOnboardingCommand(slack_client_wrapper=current_app.slack_client_wrapper,
                                       slack_team_id=slack_agent.slack_team.id,
                                       installer_id=slack_agent.slack_application_installation.installer.id).execute()

        return SlackAgentSchema().dump(slack_agent)
