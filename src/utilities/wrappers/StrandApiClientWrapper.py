import json

from tenacity import Retrying, wait_fixed, stop_after_attempt, retry_if_exception_type, after_log

from src.models.exceptions.exceptions import StrandTranslationException
from src.models.strand.StrandStrand import StrandStrandSchema, StrandStrand
from src.models.strand.StrandTeam import StrandTeamSchema
from src.models.strand.StrandUser import StrandUserSchema
from src.models.strand.utils import dict_keys_camel_case_to_underscores
from src.utilities.clients.StrandApiClient import StrandApiClientException
from src.utilities.logging import get_logger


class StrandApiClientWrapper:
    """Manage all outgoing interaction with the CoreApi"""

    def __init__(self, strand_api_client):
        self.strand_api_client = strand_api_client
        self.logger = get_logger('StrandApiClientWrapper')
        self.standard_retrier = Retrying(
            reraise=True,
            wait=wait_fixed(2),
            stop=stop_after_attempt(5),
            after=after_log(logger=self.logger, log_level=self.logger.getEffectiveLevel()),
            retry=retry_if_exception_type(StrandApiClientException)
        )

    def get_user_by_email(self, email):
        operation_definition = f'''
        {{
            user(email: "{email}") {{
              id
            }}
        }}
        '''
        response_body = self.standard_retrier.call(self.strand_api_client.query,
                                                   operation_definition=operation_definition)
        if self._did_return_not_exists(response_body=response_body):
            return None
        return self._deserialize_response_body(
            response_body=response_body, ObjectSchema=StrandUserSchema,
            path_to_object=['data', 'user']
        )

    def create_user_with_team(self, email, first_name, last_name, team_id):
        operation_definition = f'''
                {{
                    createUserWithTeams(input: {{email: "{email}",
                                        firstName: "{first_name}",
                                        lastName: "{last_name}",
                                        teamIds: [{team_id}]}}) {{
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
            path_to_object=['data', 'createUserWithTeams', 'user']
        )

    def add_user_to_team(self, user_id, team_id):
        operation_definition = f'''
                {{
                    addMembersToTeam(input: {{  id: {team_id},
                                              memberIds: [{user_id}]}}) {{
                      team {{
                        members {{
                          id
                        }}
                      }}
                    }}
                }}
                '''
        response_body = self.standard_retrier.call(self.strand_api_client.mutate,
                                                   operation_definition=operation_definition)
        self._validate_no_response_body_errors(response_body=response_body)

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

    def create_strand(self, team_id, saver_user_id, body):
        body = json.dumps(body)
        operation_definition = f'''
                {{
                    createStrand(input: {{ownerId: {team_id},
                                        saverId: {saver_user_id},
                                        body: {body}}}) {{
                      strand {{
                        id
                      }}
                    }}
                }}
        '''
        response_body = self.standard_retrier.call(self.strand_api_client.mutate,
                                                   operation_definition=operation_definition)
        return self._deserialize_response_body(
            response_body=response_body, ObjectSchema=StrandStrandSchema,
            path_to_object=['data', 'createStrand', 'strand']
        )

    def update_strand(self, strand: StrandStrand):
        title = json.dumps(strand.title)
        operation_definition = f'''
                {{
                    updateStrand(input: {{title: {title},
                                          id: {strand.id},
                                          tags: [{','.join([f'{{name: "{tag.name}"}}' for tag in strand.tags])}]
                                        }}){{
                      strand {{
                        id
                      }}
                    }}
                }}
        '''
        response_body = self.standard_retrier.call(self.strand_api_client.mutate,
                                                   operation_definition=operation_definition)
        self._validate_no_response_body_errors(response_body=response_body)

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
            message = f'Errors when calling StrandApiClient. Body: {response_body}'
            self.logger.error(message)
            raise StrandTranslationException(message)

    def _did_return_not_exists(self, response_body):
        """Returns true if the errors exists but it looks like it's only because there's no result"""
        if 'errors' in response_body and len(response_body['errors']) == 1:
            return 'matching query does not exist' in response_body['errors'][0]['message']
        return False
