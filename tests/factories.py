import factory

from src.domain.models.SlackApplicationInstallation import SlackApplicationInstallation
from src.domain.models.SlackTeam import SlackTeam
from src.domain.models.SlackUser import SlackUser
from src.domain.models.SlackAgent import SlackAgent
from src.domain.models.SlackAgentStatus import SlackAgentStatus


class SlackTeamFactory(factory.Factory):
    class Meta:
        model = SlackTeam

    id = factory.Faker('ean8')


class SlackUserFactory(factory.Factory):
    class Meta:
        model = SlackUser

    id = factory.Faker('ean8')


class SlackApplicationInstallationFactory(factory.Factory):
    class Meta:
        model = SlackApplicationInstallation

    bot_access_token = factory.Faker('md5')
    access_token = factory.Faker('md5')
    installer = factory.SubFactory(SlackUserFactory)


class SlackAgentFactory(factory.Factory):
    class Meta:
        model = SlackAgent

    status = SlackAgentStatus.INITIATED.name
    help_channel_id = factory.Faker('ean8')
    slack_team = factory.SubFactory(SlackTeamFactory)
    slack_application_installation = factory.SubFactory(SlackApplicationInstallationFactory)
