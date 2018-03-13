from src.utilities.logging import get_logger


class TestStrandApiClient:
    def __init__(self, **kwargs):
        self.logger = get_logger('TestCoreApiClient')

    def query(self, operation_definition):
        self.logger.info(f'Query call: {operation_definition}')
        return {'data': {'slackAgents': []}}

    def mutate(self, operation_definition):
        self.logger.info(f'Mutate call: {operation_definition}')
        if 'createTeam' in operation_definition:
            return {'data': {'createTeam': {'team': {
                'id': '3249838',
            }}}}
        elif 'createUser' in operation_definition:
            return {'data': {'createUser': {'user': {
                'id': '84338',
            }}}}
        return {'errors': [{'message': 'Some other error'}]}
