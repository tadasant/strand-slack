class SlackAgentRepository:
    def __init__(self):
        self.slack_agents_by_team_id = {}

    def set_slack_agents(self, slack_agents):
        self.slack_agents_by_team_id = {x.slack_team.id: x for x in slack_agents}

    def set_slack_agent(self, slack_agent):
        self.slack_agents_by_team_id[slack_agent.slack_team.id] = slack_agent

    def add_slack_agent(self, slack_agent):
        self.set_slack_agent(slack_agent)


slack_agent_repository = SlackAgentRepository()
