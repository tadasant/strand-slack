import requests
from tenacity import Retrying, wait_fixed, stop_after_attempt, after_log, retry_if_exception_type

from src.common.logging import get_logger
from src.domain.models.exceptions.WrapperException import WrapperException
from src.domain.repositories.SlackAgentRepository import slack_agent_repository


# TODO move deserialization to this class instead of in Commands

class SlackClientWrapper:
    """Manage all outgoing interaction with Slack APIs"""

    def __init__(self, SlackClientClass):
        self.SlackClientClass = SlackClientClass
        self.logger = get_logger('SlackClientWrapper')
        self.standard_retrier = Retrying(
            reraise=True,
            wait=wait_fixed(2),
            stop=stop_after_attempt(5),
            after=after_log(logger=self.logger, log_level=self.logger.getEffectiveLevel()),
            retry=(retry_if_exception_type(ConnectionError))
        )

    def send_dm_to_user(self, slack_team_id, slack_user_id, text, attachments=None):
        if not attachments:
            attachments = []

        slack_client = self._get_slack_client(slack_team_id=slack_team_id)
        response = self.standard_retrier.call(slack_client.api_call, method='im.open', user=slack_user_id)
        self._validate_response_ok(response, 'send_dm_to_user', slack_team_id, slack_user_id, text)
        slack_channel_id = response['channel']['id']
        self.standard_retrier.call(slack_client.api_call, method='chat.postMessage', channel=slack_channel_id,
                                   text=text, attachments=attachments)

    def post_to_response_url(self, response_url, payload):
        response_retrier = self.standard_retrier.copy(wait=wait_fixed(0.5), stop=stop_after_attempt(4))
        response = response_retrier.call(fn=requests.post, url=response_url,
                                         headers={'Content-Type': 'application/json'},
                                         json=payload)
        self._validate_response_ok(response, 'post_to_response_url', response_url, payload)

    def send_dialog(self, trigger_id, slack_team_id, dialog):
        slack_client = self._get_slack_client(slack_team_id=slack_team_id)
        response = self.standard_retrier.call(slack_client.api_call, method='dialog.open', trigger_id=trigger_id,
                                              dialog=dialog)
        self._validate_response_ok(response, 'send_dialog', trigger_id, slack_team_id, dialog)

    def get_user_info(self, slack_team_id, slack_user_id):
        slack_client = self._get_slack_client(slack_team_id=slack_team_id)
        response = self.standard_retrier.call(slack_client.api_call, method='users.info', user=slack_user_id)
        self._validate_response_ok(response, 'get_user_info', slack_team_id, slack_user_id)
        return response['user']

    def create_channel(self, slack_team_id, channel_name):
        slack_client = self._get_slack_client(slack_team_id=slack_team_id, is_bot=False)
        response = self.standard_retrier.call(slack_client.api_call, method='channels.create', name=channel_name)
        self._validate_response_ok(response, 'create_channel', slack_team_id, channel_name)
        return response['channel']

    def invite_user_to_channel(self, slack_team_id, slack_channel_id, slack_user_id):
        slack_client = self._get_slack_client(slack_team_id=slack_team_id, is_bot=False)
        response = self.standard_retrier.call(slack_client.api_call, method='channels.invite', channel=slack_channel_id,
                                              user=slack_user_id)
        self._validate_response_ok(response, 'invite_user_to_channel', slack_team_id, slack_channel_id, slack_user_id)

    def send_message(self, slack_team_id, slack_channel_id, text):
        slack_client = self._get_slack_client(slack_team_id=slack_team_id)
        response = self.standard_retrier.call(slack_client.api_call, method='chat.postMessage',
                                              channel=slack_channel_id, text=text)
        self._validate_response_ok(response, 'send_message', slack_team_id, slack_channel_id, text)

    def get_last_channel_message(self, slack_team_id, slack_channel_id):
        slack_client = self._get_slack_client(slack_team_id=slack_team_id, is_bot=False)
        response = self.standard_retrier.call(slack_client.api_call, method='channels.history',
                                              channel=slack_channel_id, count=1)
        self._validate_response_ok(response, 'get_last_channel_message', slack_team_id, slack_channel_id)
        messages = response['messages']
        if len(messages) != 1:
            self._raise_wrapper_exception(response, 'no messages in discuss', slack_team_id, slack_channel_id)
        return messages[0]

    def get_first_channel_message(self, slack_team_id, slack_channel_id):
        slack_client = self._get_slack_client(slack_team_id=slack_team_id, is_bot=False)
        response = self.standard_retrier.call(slack_client.api_call, method='channels.history',
                                              channel=slack_channel_id, count=1000)
        self._validate_response_ok(response, 'get_last_channel_message', slack_team_id, slack_channel_id)
        messages = response['messages']
        if len(messages) == 0:
            self._raise_wrapper_exception(response, 'no messages in discuss', slack_team_id, slack_channel_id)
        return messages[-1]

    def update_message(self, slack_team_id, slack_channel_id, new_text, message_ts):
        slack_client = self._get_slack_client(slack_team_id=slack_team_id)
        response = self.standard_retrier.call(slack_client.api_call, method='chat.update', channel=slack_channel_id,
                                              text=new_text, ts=message_ts, as_user=True)  # bot is user in this case
        self._validate_response_ok(response, 'update_message', slack_team_id, slack_channel_id)

    def get_channel_info(self, slack_team_id, slack_channel_id):
        slack_client = self._get_slack_client(slack_team_id=slack_team_id)
        response = self.standard_retrier.call(slack_client.api_call, method='channels.info', channel=slack_channel_id)
        self._validate_response_ok(response, 'get_channel_info', slack_team_id, slack_channel_id)
        return response['channel']

    def publicize_file(self, slack_team_id, file_id):
        slack_client = self._get_slack_client(slack_team_id=slack_team_id)
        response = self.standard_retrier.call(slack_client.api_call, method='files.sharedPublicURL', file=file_id)
        self._validate_response_ok(response, 'publicize_file', slack_team_id, file_id)
        return response['file']

    def archive_channel(self, slack_team_id, slack_channel_id):
        slack_client = self._get_slack_client(slack_team_id=slack_team_id, is_bot=False)
        response = self.standard_retrier.call(slack_client.api_call, method='channels.archive',
                                              channel=slack_channel_id)
        self._validate_response_ok(response, 'archive_channel', slack_team_id, slack_channel_id)

    def _get_slack_client(self, slack_team_id, is_bot=True):
        """Using slack_team_id's tokens from the in-memory repo, wires up a slack_client"""
        repo = slack_agent_repository
        token = repo.get_slack_bot_access_token(slack_team_id=slack_team_id) if is_bot else repo.get_slack_access_token(
            slack_team_id=slack_team_id)
        return self.SlackClientClass(token=token)

    def _validate_response_ok(self, response, *args):
        """All variables in *args are dumped to logger output"""
        is_negative = not response['ok'] if 'ok' in response else response.status_code != 200
        if is_negative:
            self._raise_wrapper_exception(response, *args)

    def _raise_wrapper_exception(self, response, *args):
        message = f'Errors when calling SlackClient. \n\t{response}\n\t{args}'
        self.logger.error(message)
        raise WrapperException(wrapper_name='SlackClient', message=message)
