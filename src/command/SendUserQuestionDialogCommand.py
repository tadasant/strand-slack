from src.command.Command import Command
from src.command.messages.question_dialog import QUESTION_DIALOG


class SendUserQuestionDialogCommand(Command):
    def __init__(self, slack_client_wrapper, trigger_id, slack_team_id, slack_user_id):
        super().__init__(slack_client_wrapper=slack_client_wrapper)
        self.slack_team_id = slack_team_id
        self.slack_user_id = slack_user_id
        self.trigger_id = trigger_id

    def execute(self):
        self.logger.info(f'Executing SendUserQuestionDialog for {self.slack_team_id} with user {self.slack_user_id}')
        self.slack_client_wrapper.send_dialog(trigger_id=self.trigger_id, slack_team_id=self.slack_team_id,
                                              dialog=QUESTION_DIALOG.value)
