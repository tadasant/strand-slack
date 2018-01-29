import factory

from src.domain.models.slack.Action import Action
from src.domain.models.slack.InteractiveMenuRequest import InteractiveMenuRequest
from src.domain.models.slack.Message import Message
from src.domain.models.slack.Option import Option
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


class InteractiveMenuRequestFactory(factory.Factory):
    class Meta:
        model = InteractiveMenuRequest

    type = factory.Faker('word')
    callback_id = factory.Faker('word')
    team = factory.SubFactory(TeamFactory)
    original_message = factory.SubFactory(MessageFactory)
    response_url = factory.Faker('url')
    actions = factory.List([ActionFactory.build()])
