from datetime import datetime

from marshmallow import Schema, fields, post_load

from src.domain.models.Model import Model


class SlackMessage(Model):
    """Subset of Event from requests"""

    def __init__(self, file_url=None, **kwargs):
        """Construct kwargs by unpacking an Event dict"""
        expected_args = ['ts', 'text']
        assert all(x in kwargs for x in expected_args), f'Expected {expected_args} in SlackMessage constructor'

        self.thread_ts = kwargs.get('thread_ts')
        self.channel_id = kwargs.get('channel')
        self.user_id = kwargs.get('user')
        self.ts = kwargs.get('ts')
        self.subtype = kwargs.get('subtype')
        self.text = kwargs.get('text')
        self.file_url = file_url

    @property
    def is_join_message(self):
        return self.subtype == 'channel_join'

    @property
    def time(self):
        return datetime.fromtimestamp(int(self.ts.split('.')[0]))


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
