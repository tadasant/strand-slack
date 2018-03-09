from tenacity import Retrying, wait_fixed, stop_after_attempt, retry_if_exception_type, after_log

from src.utilities.clients.StrandApiClient import StrandApiClientException
from src.utilities.logging import get_logger
from src.models.exceptions.WrapperException import WrapperException
from src.models.strand.utils import dict_keys_camel_case_to_underscores


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

    def create_discussion(self, topic_id):
        # TODO convert to create strand
        operation_definition = f'''
        {{
            createDiscussion(input: {{topicId: {topic_id}}}) {{
              discussion {{
                id
              }}
            }}
        }}
        '''
        response_body = self.standard_retrier.call(self.strand_api_client.mutate,
                                                   operation_definition=operation_definition)
        return self._deserialize_response_body(
            response_body=response_body, ObjectSchema=None,
            path_to_object=['data', 'createDiscussion', 'discussion']
        )

    def _deserialize_response_body(self, response_body, ObjectSchema, path_to_object, many=False):
        """Deserializes response_body[**path_to_object] using ObjectSchema"""
        self._validate_no_response_body_errors(response_body=response_body)
        result_json = response_body
        for key in path_to_object:
            result_json = result_json[key]
        if many:
            return [ObjectSchema().load(dict_keys_camel_case_to_underscores(x)).data for x in result_json]
        return ObjectSchema().load(dict_keys_camel_case_to_underscores(result_json)).data

    def _validate_no_response_body_errors(self, response_body):
        """Raises an exception if there are any errors in response_body"""
        if 'errors' in response_body:
            message = f'Errors when calling CoreApiClient. Body: {response_body}'
            raise WrapperException(wrapper_name='CoreApiClient', message=message, errors=response_body['errors'])
