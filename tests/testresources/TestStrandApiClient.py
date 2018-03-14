from src.utilities.logging import get_logger

StrandRepository = {
    # Plain dictionaries as values
    'users_by_email': {},
}


def clear_strand_state(keys):
    for key in keys:
        StrandRepository[key] = {}


# TODO Optimization: use factories instead of hardcoded shapes in responses

class TestStrandApiClient:
    def __init__(self, **kwargs):
        self.logger = get_logger('TestCoreApiClient')

    def query(self, operation_definition):
        self.logger.info(f'Query call: {operation_definition}')
        if 'getUserByEmail' in operation_definition:
            email = get_email_value(operation_definition)
            if email in StrandRepository['users_by_email']:
                return {'data': {'user': StrandRepository['users_by_email'][email]}}
            return {'data': {'user': None}}
        return {}

    def mutate(self, operation_definition):
        self.logger.info(f'Mutate call: {operation_definition}')
        if 'createTeam' in operation_definition:
            return {'data': {'createTeam': {'team': {
                'id': '3249838',
            }}}}
        elif 'addUserToTeam' in operation_definition:
            return {'data': {'addUserToTeam': {'user': {
                'id': '482782',
            }}}}
        elif 'createUserWithTeam' in operation_definition:
            return {'data': {'createUserWithTeam': {'user': {
                'id': '84338',
            }}}}
        elif 'createStrand' in operation_definition:
            return {'data': {'createStrand': {'strand': {
                'id': '23589348',
            }}}}
        return {'errors': [{'message': 'Some other error'}]}


def get_email_value(operation_definition):
    """Assuming format like: { GetUserByEmail(email: "someemail") { ... } }"""
    text_after_email = operation_definition.split('email:')[1]
    unquoted_tokens = text_after_email.split('"')
    return unquoted_tokens[1]
