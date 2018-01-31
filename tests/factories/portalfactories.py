import factory

from src.domain.models.portal.SlackApplicationInstallation import SlackApplicationInstallation
from src.domain.models.portal.SlackTeam import SlackTeam
from src.domain.models.portal.SlackUser import SlackUser
from src.domain.models.portal.SlackAgent import SlackAgent
from src.domain.models.portal.SlackAgentStatus import SlackAgentStatus


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


class SlackAgentFactory(factory.Factory):
    class Meta:
        model = SlackAgent

    status = SlackAgentStatus.INITIATED.name
    discuss_channel_id = factory.Faker('bban')
    slack_team = factory.SubFactory(SlackTeamFactory)
    slack_application_installation = factory.SubFactory(SlackApplicationInstallationFactory)
