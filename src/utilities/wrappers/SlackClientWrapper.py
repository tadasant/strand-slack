import requests
from tenacity import Retrying, wait_fixed, stop_after_attempt, after_log, retry_if_exception_type

from src.config import config
from src.models.exceptions.WrapperException import WrapperException
from src.models.slack.elements.SlackUser import SlackUserSchema
from src.models.slack.responses import SlackOauthAccessResponse
from src.models.slack.responses.SlackOauthAccessResponse import SlackOauthAccessResponseSchema
from src.utilities.logging import get_logger


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

    def send_ephemeral_message(self, slack_team_id, slack_channel_id, slack_user_id, text, attachments=None):
        if not attachments:
            attachments = []

        slack_client = self._get_slack_client(slack_team_id=slack_team_id)
        self.standard_retrier.call(slack_client.api_call, method='chat.postEphemeral', channel=slack_channel_id,
                                   user=slack_user_id, text=text, attachments=attachments)

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
        return self._deserialize_response_body(response_body=response, ObjectSchema=SlackUserSchema,
                                               path_to_object=['user'])

    def send_message(self, slack_team_id, slack_channel_id, text, attachments=None):
        slack_client = self._get_slack_client(slack_team_id=slack_team_id)
        response = self.standard_retrier.call(slack_client.api_call, method='chat.postMessage',
                                              channel=slack_channel_id, text=text, attachments=attachments)
        self._validate_response_ok(response, 'send_message', slack_team_id, slack_channel_id, text)

    def submit_oauth_code(self, code) -> SlackOauthAccessResponse:
        slack_client = self.SlackClientClass(token=None)
        # Intentional: pulling from config directly to avoid long pass-through
        response = self.standard_retrier.call(slack_client.api_call, method='oauth.access', code=code,
                                              client_id=config['CLIENT_ID'], client_secret=config['CLIENT_SECRET'])
        self._validate_response_ok(response, 'submit_oauth_code', code)
        return self._deserialize_response_body(response_body=response, ObjectSchema=SlackOauthAccessResponseSchema)

    def _deserialize_response_body(self, response_body, ObjectSchema, path_to_object=None, many=False, **kwargs):
        """Deserializes response_body[**path_to_object] merged with **kwargs using ObjectSchema"""
        if path_to_object is None:
            path_to_object = []
        result_json = response_body
        for key in path_to_object:
            result_json = result_json[key]
        if many:
            return [ObjectSchema().load(dict(**x, **kwargs)).data for x in result_json]
        return ObjectSchema().load(dict(**result_json, **kwargs)).data

    def _get_slack_client(self, slack_team_id, is_bot=True):
        """Using slack_team_id's tokens from the in-memory repo, wires up a slack_client"""
        # TODO [SLA-36] pull the token from DB
        token = None if is_bot else None  # get tokens from repo
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
