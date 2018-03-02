from random import choice

import factory

from src.domain.models.slack.Channel import Channel
from src.domain.models.slack.Team import Team
from src.domain.models.slack.User import User
from src.domain.models.slack.requests.EventRequest import EventRequest
from src.domain.models.slack.requests.InteractiveComponentRequest import InteractiveComponentRequest
from src.domain.models.slack.requests.SlashCommandRequest import SlashCommandRequest
from src.domain.models.slack.requests.elements.Action import Action
from src.domain.models.slack.requests.elements.Event import Event
from src.domain.models.slack.requests.elements.File import File
from src.domain.models.slack.requests.elements.Message import Message
from src.domain.models.slack.requests.elements.Option import Option
from src.domain.models.slack.requests.elements.Submission import Submission


class MessageFactory(factory.Factory):
    class Meta:
        model = Message

    text = factory.Faker('paragraph')
    ts = factory.Faker('msisdn')


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

    id = factory.Faker('bban')


class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Faker('bban')


class ChannelFactory(factory.Factory):
    class Meta:
        model = Channel

    id = factory.LazyFunction(lambda: choice(['C', 'D', 'G']) + '0G9QF9GW')
    name = factory.Faker('word')


class SubmissionFactory(factory.Factory):
    class Meta:
        model = Submission

    title = factory.Faker('paragraph')
    description = factory.Faker('paragraph')
    tags = factory.Faker('paragraph')
    share_with_current_channel = False


class FileFactory(factory.Factory):
    class Meta:
        model = File

    id = factory.Faker('bban')
    public_url_shared = factory.Faker('url')
    permalink_public = False


class EventFactory(factory.Factory):
    class Meta:
        model = Event

    type = factory.Faker('word')
    user = factory.Faker('bban')
    channel = factory.Faker('bban')
    text = factory.Faker('paragraph')
    ts = factory.Faker('msisdn')
    subtype = factory.Faker('word')
    file = factory.SubFactory(FileFactory)


#  TOP LEVEL

class InteractiveComponentRequestFactory(factory.Factory):
    class Meta:
        model = InteractiveComponentRequest

    type = factory.Faker('word')
    callback_id = factory.Faker('word')
    team = factory.SubFactory(TeamFactory)
    user = factory.SubFactory(UserFactory)
    channel = factory.SubFactory(ChannelFactory)
    response_url = factory.Faker('url')
    trigger_id = factory.Faker('md5')


class SlashCommandRequestFactory(factory.Factory):
    class Meta:
        model = SlashCommandRequest

    team_id = factory.Faker('bban')
    user_id = factory.Faker('bban')
    command = factory.Faker('word')
    response_url = factory.Faker('url')
    trigger_id = factory.Faker('md5')
    channel_id = factory.Faker('bban')


class EventRequestFactory(factory.Factory):
    class Meta:
        model = EventRequest

    type = factory.Faker('word')
    challenge = factory.Faker('md5')
    team_id = factory.Faker('bban')
    event = factory.SubFactory(EventFactory)
