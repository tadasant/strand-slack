import requests
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
            retry=(retry_if_exception_type(ConnectionError) | retry_if_result(self._is_response_negative))
        )

    def _get_slack_client(self, slack_team_id, is_bot=False):
        repo = slack_agent_repository
        token = repo.get_slack_bot_access_token(slack_team_id=slack_team_id) if is_bot else repo.get_slack_access_token(
            slack_team_id=slack_team_id)
        return self.SlackClientClass(token=token)

    def _is_response_negative(self, response):
        is_negative = not response['ok'] if 'ok' in response else response.status_code != 200
        if is_negative:
            self.logger.error(f'Negative response from slack: {response}')
        return is_negative

    def send_dm_to_user(self, slack_team_id, slack_user_id, text, attachments=None):
        if not attachments:
            attachments = []

        slack_client = self._get_slack_client(slack_team_id=slack_team_id, is_bot=True)
        response = self.standard_retrier.call(slack_client.api_call, method='im.open', user=slack_user_id)
        slack_channel_id = response['channel']['id']
        self.standard_retrier.call(slack_client.api_call, method='chat.postMessage', channel=slack_channel_id,
                                   text=text, attachments=attachments)

    def post_to_response_url(self, response_url, payload):
        response_retrier = self.standard_retrier.copy(wait=wait_fixed(0.5), stop=stop_after_attempt(4))
        response_retrier.call(fn=requests.post, url=response_url, headers={'Content-Type': 'application/json'},
                              json=payload)

    def send_dialog(self, trigger_id, slack_team_id, dialog):
        slack_client = self._get_slack_client(slack_team_id=slack_team_id)
        self.standard_retrier.call(slack_client.api_call, method='dialog.open', trigger_id=trigger_id, dialog=dialog)
