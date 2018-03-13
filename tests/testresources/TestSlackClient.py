import json

from src.utilities.logging import get_logger
from tests.factories.slackfactories import SlackUserFactory

SlackRepository = {
    # OAuthAcessResponse objects as values
    'oauth_access_responses_by_code': {},
    # SlackUser objects as values
    'users_by_slack_user_id': {},
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
            user_id = kwargs.get('user')
            if user_id in SlackRepository['users_by_slack_user_id']:
                return {
                    'ok': True,
                    'user': json.loads(SlackRepository['users_by_slack_user_id'][user_id].to_json())
                }
            return {
                'ok': True,
                'user': json.loads(SlackUserFactory.create().to_json())
            }
        return {'ok': True}
