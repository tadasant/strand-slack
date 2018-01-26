import json

from flask import current_app, request
from flask_restful import Resource

from src.command.UpdateHelpChannelCommand import UpdateHelpChannelCommand
from src.command.messages.initial_onboarding_dm import INITIAL_ONBOARDING_DM


# TODO model & validate Slack's message payload
# TODO validate that this request is coming from Slack (payload['token'])
# TODO register errors (slack exceptions, wrapper exceptions, repository exceptions)
# TODO write tests

class InteractiveComponentResource(Resource):
    def post(self):
        """Receiving an interactive menu payload"""
        payload = json.loads(request.form['payload'])
        if payload['type'] == 'interactive_message' and payload['callback_id'] == INITIAL_ONBOARDING_DM.callback_id:
            slack_team_id = payload['team']['id']
            response_url = payload['response_url']
            original_message_text = payload['original_message']['text']
            filter(lambda x: x['name'] == 'help_channel_list', payload['actions'])
            help_channel_selections = payload['actions'][0]['selected_options']
            selected_channel_id = help_channel_selections[0]['value'] if len(help_channel_selections) > 0 else None
            UpdateHelpChannelCommand(slack_client_wrapper=current_app.slack_client_wrapper,
                                     portal_client_wrapper=current_app.portal_client_wrapper,
                                     slack_team_id=slack_team_id,
                                     original_message_text=original_message_text,
                                     help_channel_id=selected_channel_id,
                                     response_url=response_url).execute()

        return None, 200
