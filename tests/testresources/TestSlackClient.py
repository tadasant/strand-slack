class TestSlackClient:
    def __init__(self, *args, **kwargs):
        pass

    def api_call(self, method, *args, **kwargs):
        if method == 'im.open':
            return {'ok': True, 'channel': {'id': 0}}
        elif method == 'chat.postMessage':
            return {'ok': True, 'ts': 0}
        return {'ok': True}
