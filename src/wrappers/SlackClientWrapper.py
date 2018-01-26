from tenacity import Retrying, wait_fixed, stop_after_attempt, after_log, retry_if_exception_type, retry_if_result

from src import slack_agent_repository
from src.common.logging import get_logger


class SlackClientWrapper:
    """Manages all outgoing interaction with Slack APIs"""

    def __init__(self, SlackClientClass):
        self.SlackClientClass = SlackClientClass
        self.logger = get_logger('SlackClientWrapper')
        self.standard_retrier = Retrying(
            reraise=True,
            wait=wait_fixed(2),
            stop=stop_after_attempt(5),
            after=after_log(logger=self.logger, log_level=self.logger.getEffectiveLevel()),
            retry=(retry_if_exception_type(ConnectionError) | retry_if_result(self._is_response_not_ok))
        )

    def _get_slack_client(self, slack_team_id, is_bot=False):
        repo = slack_agent_repository
        token = repo.get_slack_bot_access_token(slack_team_id=slack_team_id) if is_bot else repo.get_slack_access_token(
            slack_team_id=slack_team_id)
        return self.SlackClientClass(token=token)

    def _is_response_not_ok(self, response):
        return not response['ok']

    def send_dm_to_user(self, slack_team_id, slack_user_id, text, attachments=[]):
        slack_client = self._get_slack_client(slack_team_id=slack_team_id, is_bot=True)
        response = self.standard_retrier.call(slack_client.api_call, method='im.open', user=slack_user_id)
        slack_channel_id = response['channel']['id']
        self.standard_retrier.call(slack_client.api_call, method='chat.postMessage', channel=slack_channel_id,
                                   text=text, attachments=attachments)
