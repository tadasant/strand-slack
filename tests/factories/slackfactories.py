import factory

from src.domain.models.slack.Action import Action
from src.domain.models.slack.InteractiveComponentRequest import InteractiveComponentRequest
from src.domain.models.slack.Message import Message
from src.domain.models.slack.Option import Option
from src.domain.models.slack.SlashCommandRequest import SlashCommandRequest
from src.domain.models.slack.Team import Team


class MessageFactory(factory.Factory):
    class Meta:
        model = Message

    text = factory.Faker('paragraph')


class OptionFactory(factory.Factory):
    class Meta:
        model = Option

    value = factory.Faker('word')


class ActionFactory(factory.Factory):
    class Meta:
        model = Action

    name = factory.Faker('word')
    selected_options = factory.List([OptionFactory.build()])


class TeamFactory(factory.Factory):
    class Meta:
        model = Team

    id = factory.Faker('ean8')


class InteractiveComponentRequestFactory(factory.Factory):
    class Meta:
        model = InteractiveComponentRequest

    type = factory.Faker('word')
    callback_id = factory.Faker('word')
    team = factory.SubFactory(TeamFactory)
    original_message = factory.SubFactory(MessageFactory)
    response_url = factory.Faker('url')
    actions = factory.List([ActionFactory.build()])


class SlashCommandRequestFactory(factory.Factory):
    class Meta:
        model = SlashCommandRequest

    team_id = factory.Faker('ean8')
    user_id = factory.Faker('ean8')
    command = factory.Faker('word')
    response_url = factory.Faker('url')
    trigger_id = factory.Faker('md5')
