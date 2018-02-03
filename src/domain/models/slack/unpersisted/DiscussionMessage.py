from src.domain.models.Model import Model


class DiscussionMessage(Model):
    """Subset of Event from requests"""

    def __init__(self, file_url=None, **kwargs):
        """Construct kwargs by unpacking an Event dict"""
        expected_args = ['channel', 'user', 'ts', 'text']
        assert all(x in kwargs for x in expected_args), f'Expected {expected_args} in DiscussionMessage constructor'

        self.thread_ts = kwargs.get('thread_ts')
        self.channel_id = kwargs.get('channel')
        self.user_id = kwargs.get('user')
        self.ts = kwargs.get('ts')
        self.subtype = kwargs.get('subtype')
        self.text = kwargs.get('text')
        self.file_url = file_url
