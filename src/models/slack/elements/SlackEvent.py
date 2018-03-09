from marshmallow import Schema, fields, post_load

from src.models.Model import Model
from src.models.slack.elements.SlackFile import SlackFileSchema
from src.models.slack.elements.SlackItem import SlackItemSchema


class SlackEvent(Model):
    def __init__(self, type, user, hidden=False, channel=None, text=None, ts=None, thread_ts=None, file=None,
                 subtype=None, item=None, item_user=None, reaction=None):
        self.type = type
        self.user = user
        self.hidden = hidden
        self.channel = channel
        self.text = text
        self.ts = ts
        self.thread_ts = thread_ts
        self.file = file
        self.subtype = subtype
        self.item = item
        self.item_user = item_user
        self.reaction = reaction

    @property
    def is_message_channels_event(self):
        if self.type == 'message' and self.channel:
            return self.user and self.text and self.ts and self.channel.startswith('C')
        return False

    @property
    def is_message_dm_event(self):
        if self.type == 'message' and self.channel:
            return self.user and self.text and self.ts and self.channel.startswith('D')
        return False

    @property
    def is_message(self):
        return self.type == 'message'

    @property
    def is_floppy_disk_reaction_added_event(self):
        # TODO: Reactions to file are currently being ignored
        return self.type == 'reaction_added' and self.item.type == 'message' and self.reaction == 'floppy_disk'

    @property
    def is_system_message(self):
        """Message that wasn't actually sent by a user"""
        return self.is_message and self.subtype == 'channel_join'

    @property
    def is_reply(self):
        return self.is_message and self.thread_ts


class SlackEventSchema(Schema):
    type = fields.String(required=True)
    user = fields.String(required=True)
    hidden = fields.Boolean()
    channel = fields.String()
    text = fields.String()
    ts = fields.String()
    thread_ts = fields.String()
    file = fields.Nested(SlackFileSchema)
    subtype = fields.String()
    item = fields.Nested(SlackItemSchema)
    item_user = fields.String()
    reaction = fields.String()

    @post_load
    def make_event(self, data):
        return SlackEvent(**data)

    class Meta:
        strict = True
