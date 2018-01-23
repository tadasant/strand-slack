from tenacity import Retrying, wait_fixed, stop_after_attempt, retry_if_exception_type, after_log

from src.clients.PortalClient import PortalClient, PortalClientException
from src.common.logging import get_logger
from src.models.exceptions.WrapperException import WrapperException
from src.models.namedtuples import SlackTokens


class PortalClientWrapper:
    def __init__(self, log_file, host, endpoint):
        self.portal_client = PortalClient(host=host, endpoint=endpoint)
        self.logger = get_logger('PortalClientWrapper', log_file)

    def get_slack_tokens_by_slack_team_id(self):
        operation_definition = '''
            {
                slackTeamInstallations {
                    botAccessToken
                    accessToken
                    slackTeam
                }
            }
        '''
        retrier = Retrying(
            reraise=True,
            wait=wait_fixed(2),
            stop=stop_after_attempt(5),
            after=after_log(logger=self.logger, log_level=self.logger.getEffectiveLevel()),
            retry=retry_if_exception_type(PortalClientException)
        )
        retrier.call(lambda: self.portal_client.query(operation_definition=operation_definition))
        try:
            slack_installations = retrier.call(self.portal_client.query(operation_definition=operation_definition))
        except PortalClientException as e:
            self.logger.error(f'Failed when calling PortalClient. Error: {str(e)}')
            raise WrapperException(wrapper_name='PortalClient',
                                   message=f'Failed when calling PortalClient Error: {str(e)}')
        return {
            x['slackTeam']: SlackTokens(bot_access_token=x['botAccessToken'], access_token=x['accessToken'])
            for x in slack_installations
        }
