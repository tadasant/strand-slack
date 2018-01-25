from src.domain.models.exceptions.RepositoryException import RepositoryException


class SlackAgentRepository:
    def __init__(self):
        self._slack_agents_by_team_id = {}

    def get_slack_access_token(self, slack_team_id):
        if slack_team_id not in self._slack_agents_by_team_id:
            raise RepositoryException(object_name='SlackAgent', message=f'No slack agent for team {slack_team_id}')
        return self._slack_agents_by_team_id[slack_team_id].slack_application_installation.access_token

    def get_slack_bot_access_token(self, slack_team_id):
        if slack_team_id not in self._slack_agents_by_team_id:
            raise RepositoryException(object_name='SlackAgent', message=f'No slack agent for team {slack_team_id}')
        return self._slack_agents_by_team_id[slack_team_id].slack_application_installation.bot_access_token

    def set_slack_agents(self, slack_agents):
        self._slack_agents_by_team_id = {x.slack_team.id: x for x in slack_agents}

    def set_slack_agent(self, slack_agent):
        self._slack_agents_by_team_id[slack_agent.slack_team.id] = slack_agent

    def add_slack_agent(self, slack_agent):
        self.set_slack_agent(slack_agent)

    def clear(self):
        self._slack_agents_by_team_id = {}


slack_agent_repository = SlackAgentRepository()
