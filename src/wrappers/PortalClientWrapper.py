from tenacity import Retrying, wait_fixed, stop_after_attempt, retry_if_exception_type, after_log

from src.clients.PortalClient import PortalClientException
from src.common.logging import get_logger
from src.models.exceptions.WrapperException import WrapperException
from src.models.namedtuples import SlackTokens


# TODO [CCS-26] Add authentication

class PortalClientWrapper:
    def __init__(self, log_file, portal_client):
        self.portal_client = portal_client
        self.logger = get_logger('PortalClientWrapper', log_file)
        self.standard_retrier = Retrying(
            reraise=True,
            wait=wait_fixed(2),
            stop=stop_after_attempt(5),
            after=after_log(logger=self.logger, log_level=self.logger.getEffectiveLevel()),
            retry=retry_if_exception_type(PortalClientException)
        )

    def get_slack_tokens_by_slack_team_id(self):
        operation_definition = '''
            {
                slackTeamInstallations {
                    botAccessToken
                    accessToken
                    slackTeam {
                        id
                    }
                }
            }
        '''
        try:
            data = self.standard_retrier.call(self.portal_client.query, operation_definition=operation_definition)
        except PortalClientException as e:
            self.logger.error(f'Failed when calling PortalClient. Error: {str(e)}')
            raise WrapperException(wrapper_name='PortalClient',
                                   message=f'Failed when calling PortalClient Error: {str(e)}')
        return {
            x['slackTeam']['id']: SlackTokens(bot_access_token=x['botAccessToken'], access_token=x['accessToken'])
            for x in data['slackTeamInstallations']
        }
