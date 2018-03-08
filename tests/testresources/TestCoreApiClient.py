import threading

from src.utilities.logging import get_logger
from src.models.exceptions.WrapperException import WrapperException


class TestCoreApiClient:
    def __init__(self, **kwargs):
        self.next_responses = []
        self.lock = threading.RLock()
        self.logger = get_logger('TestCoreApiClient')

    # UTILITIES

    def set_next_response(self, response):
        # TODO [SLA-70] shouldn't use this feature. Will become mostly obsolete with SLA-81.
        with self.lock:
            self.logger.info(f'Queueing {response}')
            self.next_responses.append(response)

    def clear_responses(self):
        with self.lock:
            self.logger.info(f'Clearing all responses')
            self.next_responses = []

    # MOCKS

    def query(self, operation_definition):
        with self.lock:
            self.logger.info(f'Query call: {operation_definition}')
            if self.next_responses:
                result = self.next_responses[0]
                self.next_responses = self.next_responses[1:]
                if result:
                    # Allow us to set_next_response as None to skip a call
                    return result
            elif 'slackAgents' in operation_definition:
                return {'data': {'slackAgents': []}}
            return None

    def mutate(self, operation_definition):
        with self.lock:
            self.logger.info(f'Mutate call: {operation_definition}')
            if self.next_responses:
                result = self.next_responses[0]
                self.next_responses = self.next_responses[1:]
                if result:
                    # Allow us to set_next_response as None to skip a call
                    return result
            if 'updateSlackAgentTopicChannelAndActivate' in operation_definition:
                return {'data': {'updateSlackAgentTopicChannelAndActivate': {
                    'slackAgent': {
                        'status': 'ACTIVE',
                        'slackTeam': {
                            'id': 'unimportant'
                        },
                        'slackApplicationInstallation': {
                            'accessToken': 'unimportant',
                            'botAccessToken': 'unimportant',
                            'installer': {
                                'id': 'unimportant'
                            },
                            'botUserId': 'unimportant',
                        }
                    }
                }}}
            elif 'createTopicFromSlack'in operation_definition:
                # Assuming that core_api does not have the user in the request
                raise WrapperException(wrapper_name='CoreApiClient', message='',
                                       errors=[{'message': 'SlackUser matching query does not exist.'}])
            elif 'createMessageFromSlack' in operation_definition or 'createReplyFromSlack' in operation_definition:
                # Assuming that core_api does not have the user in the request
                raise WrapperException(wrapper_name='CoreApiClient', message='',
                                       errors=[{'message': 'User matching query does not exist.'}])
            return {'errors': [{'message': 'Some other error'}]}
