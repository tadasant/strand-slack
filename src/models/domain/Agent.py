from src.models.Model import Model


class Agent(Model):
    def __init__(self, status, slack_team_id, slack_application_installation=None):
        self.status = status
        self.slack_team_id = slack_team_id
        self.slack_application_installation = slack_application_installation
