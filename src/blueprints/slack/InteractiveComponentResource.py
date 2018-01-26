import json

from flask import current_app, request
from flask_restful import Resource

from src.command.messages.onboarding_dm import ONBOARDING_DM
from src.domain.repositories.SlackAgentRepository import slack_agent_repository
from src.command.OnboardTeam import OnboardTeam
from src.domain.models.portal.SlackAgent import SlackAgentSchema


# TODO model & validate Slack's message payload

class InteractiveComponentResource(Resource):
    def post(self):
        """Receiving an interactive menu payload"""
        payload = json.loads(request.form['payload'])
        if payload['type'] == 'interactive_message' and payload['callback_id'] == ONBOARDING_DM.callback_id:
            slack_team_id = payload['team']['id']
            channel_id = payload['channel']['id']
            response_url = payload['response_url']
            filter(lambda x: x['name'] == 'help_channel_list', payload['actions'])
            help_channel_selections = payload['actions'][0]['selected_options']
            selected_channel_id = help_channel_selections[0]['value'] if len(help_channel_selections) > 0 else None
            pass
            # TODO register errors (slack exceptions, wrapper exceptions, repository exceptions)
            # Do command (forward the slackagent.slackapplicationinstallation change to portal & DM user)
        args = request.get_json()
        slack_agent = SlackAgentSchema().load(args).data
        slack_agent_repository.add_slack_agent(slack_agent)

        OnboardTeam(slack_client_wrapper=current_app.slack_client_wrapper,
                    team_id=slack_agent.slack_team.id,
                    installer_id=slack_agent.slack_application_installation.installer.id).execute()

        return {'ok': True}
