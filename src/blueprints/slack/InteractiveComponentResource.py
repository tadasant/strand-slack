import json

from flask import current_app, request
from flask_restful import Resource

from src.command.messages.initial_onboarding_dm import INITIAL_ONBOARDING_DM
from src.domain.repositories.SlackAgentRepository import slack_agent_repository
from src.command.InitiateAgentOnboarding import InitiateAgentOnboarding
from src.domain.models.portal.SlackAgent import SlackAgentSchema


# TODO model & validate Slack's message payload

class InteractiveComponentResource(Resource):
    def post(self):
        """Receiving an interactive menu payload"""
        payload = json.loads(request.form['payload'])
        if payload['type'] == 'interactive_message' and payload['callback_id'] == INITIAL_ONBOARDING_DM.callback_id:
            # TODO validate that this request is coming from Slack (payload['token'])
            slack_team_id = payload['team']['id']
            channel_id = payload['channel']['id']
            response_url = payload['response_url']
            filter(lambda x: x['name'] == 'help_channel_list', payload['actions'])
            help_channel_selections = payload['actions'][0]['selected_options']
            selected_channel_id = help_channel_selections[0]['value'] if len(help_channel_selections) > 0 else None
            pass
            # TODO register errors (slack exceptions, wrapper exceptions, repository exceptions)
            # Do command (forward the slackagent.slackapplicationinstallation change to portal & DM user)

        return None, 200
