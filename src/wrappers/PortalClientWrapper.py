from tenacity import Retrying, wait_fixed, stop_after_attempt, retry_if_exception_type, after_log

from src.clients.PortalClient import PortalClientException
from src.common.logging import get_logger
from src.models.SlackApplicationInstallation import SlackApplicationInstallationSchema
from src.models.exceptions.WrapperException import WrapperException

# TODO [CCS-26] Add authentication
from src.models.utils import dict_keys_camel_case_to_underscores


class PortalClientWrapper:
    def __init__(self, portal_client):
        self.portal_client = portal_client
        self.logger = get_logger('PortalClientWrapper')
        self.standard_retrier = Retrying(
            reraise=True,
            wait=wait_fixed(2),
            stop=stop_after_attempt(5),
            after=after_log(logger=self.logger, log_level=self.logger.getEffectiveLevel()),
            retry=retry_if_exception_type(PortalClientException)
        )

    def get_installations_by_slack_team_id(self):
        operation_definition = '''
            {
                slackApplicationInstallations {
                    botAccessToken
                    accessToken
                    isActive
                    slackTeam {
                        id
                    }
                    installer {
                        id
                    }
                }
            }
        '''
        response_body = self.standard_retrier.call(self.portal_client.query, operation_definition=operation_definition)
        if 'errors' in response_body:
            raise WrapperException(wrapper_name='PortalClient',
                                   message=f'Errors when calling PortalClient. Body: {response_body}')
        installations_dicts = response_body['data']['slackApplicationInstallations']
        installations = [SlackApplicationInstallationSchema().load(dict_keys_camel_case_to_underscores(x)).data for x in
                         installations_dicts]
        return {x.slack_team.id: x for x in installations}
