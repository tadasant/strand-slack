import threading

from src.domain.models.exceptions.WrapperException import WrapperException


class TestPortalClient:
    def __init__(self, **kwargs):
        self.next_responses = []
        self.lock = threading.Lock()

    # UTILITIES

    def set_next_response(self, response):
        # TODO [CCS-70] shouldn't use this feature
        with self.lock:
            self.next_responses.append(response)

    def clear_responses(self):
        with self.lock:
            self.next_responses = []

    # MOCKS

    def query(self, operation_definition):
        with self.lock:
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
            if self.next_responses:
                result = self.next_responses[0]
                self.next_responses = self.next_responses[1:]
                if result:
                    # Allow us to set_next_response as None to skip a call
                    return result
            if 'updateSlackAgentDiscussChannelAndActivate' in operation_definition:
                return {'data': {'updateSlackAgentDiscussChannelAndActivate': {
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
                            }
                        }
                    }
                }}}
            elif 'createTopicFromSlack' in operation_definition:
                # Assuming that portal does not have the user in the request
                raise WrapperException(wrapper_name='PortalClient', message='',
                                       errors=['SlackUser matching query does not exist.'])
            return {'errors': ['someerror']}
