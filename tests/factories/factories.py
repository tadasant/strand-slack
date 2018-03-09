import factory

from src.models.domain.Installation import Installation
from src.models.domain.Agent import Agent
from src.models.domain.AgentStatus import AgentStatus


class InstallationFactory(factory.Factory):
    class Meta:
        model = Installation

    # TODO missing installer
    bot_access_token = factory.Faker('md5')
    access_token = factory.Faker('md5')
    bot_user_id = factory.Faker('bban')


class AgentFactory(factory.Factory):
    class Meta:
        model = Agent

    status = AgentStatus.INITIATED.name
    topic_channel_id = factory.Faker('bban')
    slack_team_id = factory.Faker('bban')
    slack_application_installation = factory.SubFactory(InstallationFactory)
