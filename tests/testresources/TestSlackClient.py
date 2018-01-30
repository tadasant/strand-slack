class TestSlackClient:
    def __init__(self, token, *args, **kwargs):
        self.token = token

    def api_call(self, method, *args, **kwargs):
        if method == 'im.open':
            return {'ok': True, 'channel': {'id': 0}}
        elif method == 'chat.postMessage':
            return {'ok': True, 'ts': 0}
        elif method == 'users.info':
            return {'ok': True, 'user': {'id': 'someid', 'profile': {'image_72': 'url.com'}}}
        elif method == 'channels.create':
            return {'ok': True, 'channel': {'id': 'someid', 'name': 'somename'}}
        elif method == 'channels.invite':
            return {'ok': True, 'channel': {'id': 'someid', 'name': 'somename'}}
        return {'ok': True}
