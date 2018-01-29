import json
from http import HTTPStatus
from threading import Thread

from flask import current_app, request

from src.blueprints.slack.SlackResource import SlackResource
from src.command.SendUserQuestionDialogCommand import SendUserQuestionDialogCommand
from src.domain.models.exceptions.UnexpectedSlackException import UnexpectedSlackException
from src.domain.models.slack.SlashCommandRequest import SlashCommandRequestSchema


class SlashCommandResource(SlackResource):
    def post(self):
        self.logger.info(f'Processing SlashCommand request: {request}')
        payload = json.loads(request.form['payload'])
        self._authenticate(payload)
        slash_command_request = SlashCommandRequestSchema().load(payload).data
        r = slash_command_request
        if r.is_question_initiation:
            command = SendUserQuestionDialogCommand(slack_client_wrapper=current_app.slack_client_wrapper,
                                                    trigger_id=r.trigger_id,
                                                    slack_team_id=r.team_id,
                                                    slack_user_id=r.user_id)
            Thread(target=command.execute).start()
        else:
            message = f'Could not interpret slack request: {r}'
            self.logger.error(message)
            raise UnexpectedSlackException(message=message)

        return '', HTTPStatus.NO_CONTENT
