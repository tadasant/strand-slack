from src import slack_agent_repository
from src.common.logging import get_logger
from src.domain.models.exceptions.WrapperException import WrapperException


class SlackClientWrapper:
    """Manages all outgoing interaction with Slack APIs"""

    def __init__(self, SlackClientClass):
        self.SlackClientClass = SlackClientClass
        self.logger = get_logger('SlackClientWrapper')

    def _get_slack_client(self, slack_team_id, is_bot=False):
        repo = slack_agent_repository
        token = repo.get_slack_bot_access_token(slack_team_id=slack_team_id) if is_bot else repo.get_slack_access_token(
            slack_team_id=slack_team_id)
        # TODO retry logic
        return self.SlackClientClass(token=token)

    def send_dm_to_user(self, slack_team_id, slack_user_id, text, attachments=[]):
        slack_client = self._get_slack_client(slack_team_id=slack_team_id, is_bot=True)
        # TODO retry logic
        slack_channel_id = slack_client.api_call('im.open', user=slack_user_id)['channel']['id']
        slack_client.api_call('chat.postMessage', channel=slack_channel_id, text=text, attachments=attachments)
