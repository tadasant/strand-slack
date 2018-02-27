from src.common.logging import get_logger
from tests.common.PrimitiveFaker import PrimitiveFaker

SlackRepository = {
    'created_channels_by_id': {},
    'messages_posted_by_channel_id': {}
}


def clear_slack_state():
    SlackRepository['created_channels_by_id'] = {}
    SlackRepository['messages_posted_by_channel_id'] = {}


class TestSlackClient:
    """TODO should be able to deprecate most of this after SLA-81 refactoring"""
    def __init__(self, token, *args, **kwargs):
        self.token = token
        self.logger = get_logger('TestSlackClient')

    def api_call(self, method, *args, **kwargs):
        if method == 'im.open':
            return {'ok': True, 'channel': {'id': 0}}
        elif method == 'chat.postMessage':
            """Stores the message in the channel it was posted"""
            channel_id = kwargs.get('channel')
            new_message = {'text': kwargs.get('text'), 'ts': str(PrimitiveFaker('random_int'))}
            if channel_id not in SlackRepository['messages_posted_by_channel_id']:
                SlackRepository['messages_posted_by_channel_id'][channel_id] = []
            SlackRepository['messages_posted_by_channel_id'][channel_id].append(new_message)
            return {'ok': True, **new_message}
        elif method == 'users.info':
            return {'ok': True, 'user': {'id': 'someid', 'profile': {'image_72': 'url.com'}, 'is_admin': True}}
        elif method == 'channels.create':
            channel_id = str(PrimitiveFaker('bban'))
            channel_name = kwargs.get('name')
            SlackRepository['created_channels_by_id'][channel_id] = {'id': channel_id, 'name': channel_name}
            return {'ok': True, 'channel': {'id': channel_id, 'name': channel_name}}
        elif method == 'channels.invite':
            return {'ok': True, 'channel': {'id': 'someid', 'name': 'somename'}}
        elif method == 'channels.history':
            """Returns all the messages posted to the channel in reverse order, abbreviated to kwargs['count']"""
            channel_id = kwargs.get('channel')
            messages = SlackRepository['messages_posted_by_channel_id'][channel_id] if channel_id in SlackRepository[
                'messages_posted_by_channel_id'] else []
            count = kwargs.get('count', 1000)
            messages.reverse()
            return {'ok': True, 'messages': messages[:count]}
        elif method == 'files.sharedPublicURL':
            return {'ok': True, 'file': {'permalink_public': 'someurl.com'}}
        elif method == 'channels.info':
            channel_id = kwargs.get('channel')
            if channel_id in SlackRepository['created_channels_by_id']:
                return {'ok': True, 'channel': SlackRepository['created_channels_by_id'][channel_id]}
            else:
                return {'ok': False}
        elif method == 'chat.update':
            messages = SlackRepository['messages_posted_by_channel_id'][kwargs.get('channel')]
            index = next(i for i, v in enumerate(messages) if v['ts'] == kwargs.get('ts'))
            messages[index]['text'] = kwargs.get('text')
            return {'ok': True}
        return {'ok': True}
