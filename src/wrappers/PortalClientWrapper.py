from tenacity import Retrying, wait_fixed, stop_after_attempt

from src.clients.PortalClient import PortalClient, PortalClientException
from src.common.log_retry_failure import log_retry_failure
from src.common.logging import get_logger
from src.models.exceptions.WrapperException import WrapperException
from src.models.namedtuples import SlackTokens


class PortalClientWrapper:
    def __init__(self, log_file, host, endpoint):
        self.portal_client = PortalClient(host=host, endpoint=endpoint)
        self.logger = get_logger('PortalClientWrapper', log_file)

    def get_slack_tokens(self):
        operation_definition = '''
            {
                slackTeamInstallations {
                    botAccessToken
                    accessToken
                }
            }
        '''
        retrier = Retrying(
            reraise=True,
            wait=wait_fixed(2),
            stop=stop_after_attempt(5),
            after=log_retry_failure(logger=self.logger,
                                    level='ERROR',
                                    message=f'Failed to call PortalClientWrapper.get_slack_tokens.'
                                            f'{operation_definition}')
        )
        try:
            slack_installations = retrier.call(self.portal_client.query(operation_definition=operation_definition))
        except PortalClientException as e:
            self.logger.error(f'Failed when calling PortalClient. Error: {e}')
            raise WrapperException(wrapper_name='PortalClient', message='Failed when calling PortalClient')
        return [SlackTokens(bot_access_token=x['botAccessToken'],
                            access_token=x['accessToken'])
                for x in slack_installations]
