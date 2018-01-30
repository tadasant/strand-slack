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
        return {'ok': True}
