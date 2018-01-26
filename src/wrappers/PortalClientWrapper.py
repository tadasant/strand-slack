from tenacity import Retrying, wait_fixed, stop_after_attempt, retry_if_exception_type, after_log

from src.clients.PortalClient import PortalClientException
from src.common.logging import get_logger
from src.domain.models.portal.SlackAgent import SlackAgentSchema

# TODO [CCS-26] Add authentication
from src.domain.models.exceptions.WrapperException import WrapperException
from src.domain.models.portal.SlackAgentStatus import SlackAgentStatus
from src.domain.models.utils import dict_keys_camel_case_to_underscores


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

    def get_slack_agents(self):
        operation_definition = '''
            {
                slackAgents {
                    status
                    helpChannelId
                    slackTeam {
                        id
                    }
                    slackApplicationInstallation {
                        accessToken
                        installer {
                            id
                        }
                        botAccessToken
                    }
                }
            }
        '''
        response_body = self.standard_retrier.call(self.portal_client.query, operation_definition=operation_definition)
        if 'errors' in response_body:
            raise WrapperException(wrapper_name='PortalClient',
                                   message=f'Errors when calling PortalClient. Body: {response_body}')
        slack_agent_dicts = response_body['data']['slackAgents']
        return [SlackAgentSchema().load(dict_keys_camel_case_to_underscores(x)).data for x in slack_agent_dicts]

    def update_help_channel_and_activate_agent(self, slack_team_id, help_channel_id):
        operation_definition = f'''
            {{
                updateSlackAgentHelpChannelAndActivate(input: {{slackTeamId: "{slack_team_id}",
                                                                helpChannelId: "{help_channel_id}"}}) {{
                slackAgent {{
                    helpChannelId
                    status
                }}
            }}
        '''
        response_body = self.standard_retrier.call(self.portal_client.mutate, operation_definition=operation_definition)
        if 'errors' in response_body:
            raise WrapperException(wrapper_name='PortalClient',
                                   message=f'Errors when calling PortalClient. Body: {response_body}')
        slack_agent = response_body['data']['updateSlackAgentHelpChannelAndActivate']['slackAgent']
        result = SlackAgentSchema().load(slack_agent)
        assert result.status == SlackAgentStatus.ACTIVE.name, 'Call to activate Slack Agent oddly did not transition'
        return result
