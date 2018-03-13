from tenacity import Retrying, wait_fixed, stop_after_attempt, retry_if_exception_type, after_log

from src.models.exceptions.WrapperException import WrapperException
from src.models.strand.StrandTeam import StrandTeamSchema
from src.models.strand.StrandUser import StrandUserSchema
from src.models.strand.utils import dict_keys_camel_case_to_underscores
from src.utilities.clients.StrandApiClient import StrandApiClientException
from src.utilities.logging import get_logger


class StrandApiClientWrapper:
    """Manage all outgoing interaction with the CoreApi"""

    def __init__(self, strand_api_client):
        self.strand_api_client = strand_api_client
        self.logger = get_logger('CoreApiClientWrapper')
        self.standard_retrier = Retrying(
            reraise=True,
            wait=wait_fixed(2),
            stop=stop_after_attempt(5),
            after=after_log(logger=self.logger, log_level=self.logger.getEffectiveLevel()),
            retry=retry_if_exception_type(StrandApiClientException)
        )

    def get_user_by_email(self, email):
        # TODO convert to create strand
        operation_definition = f'''
        {{
            getUserByEmail(email: "{email}") {{
              user {{
                id
              }}
            }}
        }}
        '''
        response_body = self.standard_retrier.call(self.strand_api_client.query,
                                                   operation_definition=operation_definition)
        return self._deserialize_response_body(
            response_body=response_body, ObjectSchema=StrandUserSchema,
            path_to_object=['data', 'user']
        )

    def create_user(self, email, username, first_name, last_name):
        operation_definition = f'''
                {{
                    createUser(input: {{email: "{email}",
                                        username: "{username}",
                                        first_name: "{first_name}",
                                        last_name: "{last_name}"}}) {{
                      user {{
                        id
                      }}
                    }}
                }}
                '''
        response_body = self.standard_retrier.call(self.strand_api_client.mutate,
                                                   operation_definition=operation_definition)
        return self._deserialize_response_body(
            response_body=response_body, ObjectSchema=StrandUserSchema,
            path_to_object=['data', 'createUser', 'user']
        )

    def create_team(self, name):
        operation_definition = f'''
                {{
                    createTeam(input: {{name: "{name}"}}) {{
                      team {{
                        id
                      }}
                    }}
                }}
                '''
        response_body = self.standard_retrier.call(self.strand_api_client.mutate,
                                                   operation_definition=operation_definition)
        return self._deserialize_response_body(
            response_body=response_body, ObjectSchema=StrandTeamSchema,
            path_to_object=['data', 'createTeam', 'team']
        )

    def _deserialize_response_body(self, response_body, ObjectSchema, path_to_object, many=False):
        """Deserializes response_body[**path_to_object] using ObjectSchema"""
        self._validate_no_response_body_errors(response_body=response_body)
        result_json = response_body
        for key in path_to_object:
            result_json = result_json[key]
        if result_json is None:
            return None
        if many:
            return [ObjectSchema().load(dict_keys_camel_case_to_underscores(x)).data for x in result_json]
        return ObjectSchema().load(dict_keys_camel_case_to_underscores(result_json)).data

    def _validate_no_response_body_errors(self, response_body):
        """Raises an exception if there are any errors in response_body"""
        if 'errors' in response_body:
            message = f'Errors when calling CoreApiClient. Body: {response_body}'
            raise WrapperException(wrapper_name='CoreApiClient', message=message, errors=response_body['errors'])
