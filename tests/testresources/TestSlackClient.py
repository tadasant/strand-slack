import json

from src.utilities.logging import get_logger

SlackRepository = {
    'oauth_access_responses_by_code': {},
}


# TODO Optimization: use factories instead of hardcoded shapes in responses


def clear_slack_state(keys):
    for key in keys:
        SlackRepository[key] = {}


class TestSlackClient:
    def __init__(self, token, *args, **kwargs):
        self.token = token
        self.logger = get_logger('TestSlackClient')

    def api_call(self, method, *args, **kwargs):
        if method == 'oauth.access':
            return {
                'ok': True,
                **json.loads(SlackRepository['oauth_access_responses_by_code'][kwargs.get('code')].to_json())
            }
        elif method == 'im.open':
            return {
                'ok': True,
                'channel': {
                    'id': 'SOMEID'
                }
            }
        elif method == 'users.info':
            return {
                'ok': True,
                'user': {
                    'id': 'SOMEID',
                    'profile': {
                        'real_name': 'Jimmy Immortalized',
                        'display_name': 'jimbo',
                        'email': 'jimbo@trystrand.com',
                    }
                }
            }
        return {'ok': True}
