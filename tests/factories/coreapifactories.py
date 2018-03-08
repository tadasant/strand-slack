import factory

from src.models.coreapi.SlackApplicationInstallation import SlackApplicationInstallation
from src.models.coreapi.SlackTeam import SlackTeam
from src.models.coreapi.SlackUser import SlackUser
from src.models.coreapi.SlackAgent import SlackAgent
from src.models.coreapi.SlackAgentStatus import SlackAgentStatus


class SlackTeamFactory(factory.Factory):
    class Meta:
        model = SlackTeam

    id = factory.Faker('bban')


class SlackUserFactory(factory.Factory):
    class Meta:
        model = SlackUser

    id = factory.Faker('bban')


class SlackApplicationInstallationFactory(factory.Factory):
    class Meta:
        model = SlackApplicationInstallation

    bot_access_token = factory.Faker('md5')
    access_token = factory.Faker('md5')
    installer = factory.SubFactory(SlackUserFactory)
    bot_user_id = factory.Faker('bban')


class SlackAgentFactory(factory.Factory):
    class Meta:
        model = SlackAgent

    status = SlackAgentStatus.INITIATED.name
    topic_channel_id = factory.Faker('bban')
    slack_team = factory.SubFactory(SlackTeamFactory)
    slack_application_installation = factory.SubFactory(SlackApplicationInstallationFactory)
