from src.common.logging import get_logger
from tests.common.PrimitiveFaker import PrimitiveFaker

SlackRepository = {
    'created_channels_by_id': {}
}


def clear_slack_state():
    SlackRepository['created_channels_by_id'] = {}


class TestSlackClient:
    def __init__(self, token, *args, **kwargs):
        self.token = token
        self.logger = get_logger('TestSlackClient')

    def api_call(self, method, *args, **kwargs):
        if method == 'im.open':
            return {'ok': True, 'channel': {'id': 0}}
        elif method == 'chat.postMessage':
            return {'ok': True, 'ts': 0}
        elif method == 'users.info':
            return {'ok': True, 'user': {'id': 'someid', 'profile': {'image_72': 'url.com'}}}
        elif method == 'channels.create':
            channel_id = str(PrimitiveFaker('bban'))
            channel_name = kwargs.get('name')
            SlackRepository['created_channels_by_id'][channel_id] = {'id': channel_id, 'name': channel_name}
            return {'ok': True, 'channel': {'id': channel_id, 'name': channel_name}}
        elif method == 'channels.invite':
            return {'ok': True, 'channel': {'id': 'someid', 'name': 'somename'}}
        elif method == 'channels.history':
            return {'ok': True, 'messages': [{'text': 'some', 'ts': '4328.1292'}]}
        elif method == 'files.sharedPublicURL':
            return {'ok': True, 'file': {'permalink_public': 'someurl.com'}}
        elif method == 'channels.info':
            channel_id = kwargs.get('channel')
            if channel_id in SlackRepository['created_channels_by_id']:
                return {'ok': True, 'channel': SlackRepository['created_channels_by_id'][channel_id]}
            else:
                return {'ok': False}
        return {'ok': True}
