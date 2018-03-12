from src.utilities.logging import get_logger

SlackRepository = {
    'oauth_access_responses_by_code': {},
}


def clear_slack_state(keys):
    for key in keys:
        SlackRepository[key] = {}


class TestSlackClient:
    def __init__(self, token, *args, **kwargs):
        self.token = token
        self.logger = get_logger('TestSlackClient')

    def api_call(self, method, *args, **kwargs):
        if method == 'oauth.access':
            return {'ok': True, **SlackRepository['oauth_access_responses_by_code'][kwargs.get('code')]}
        return {'ok': False}
