from marshmallow import Schema, fields, post_load

from src.models.slack.outgoing.SlackMessageModel import SlackMessageModel


class SlackMessage(SlackMessageModel):
    """Subset of Event from requests"""

    def __init__(self, file_url=None, attachments=None, **kwargs):
        """Can construct kwargs by unpacking an Event dict"""
        non_nullables = ['text']
        assert all(x in kwargs for x in non_nullables), f'Expected {non_nullables} in SlackMessage constructor'

        self.attachments = [] if attachments is None else attachments
        self.thread_ts = kwargs.get('thread_ts')
        self.channel = kwargs.get('channel')
        self.user = kwargs.get('user')
        self.ts = kwargs.get('ts')
        self.subtype = kwargs.get('subtype')
        self.text = kwargs.get('text')
        self.file_url = file_url

    @property
    def is_join_message(self):
        return self.subtype == 'channel_join'

    def as_dict(self):
        result = super().as_dict()
        result['attachments'] = [attachment.as_dict() for attachment in self.attachments]
        return result


class SlackMessageSchema(Schema):
    thread_ts = fields.String(allow_none=True)
    channel = fields.String(allow_none=True)
    user = fields.String(allow_none=True)
    ts = fields.String()
    subtype = fields.String(allow_none=True)
    text = fields.String()
    file_url = fields.String(allow_none=True)

    @post_load
    def make_slack_message(self, data):
        return SlackMessage(**data)

    class Meta:
        strict = True
