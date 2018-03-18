# TODO [SLA-61] test this / effectively treat it as an independent package (or use an existing graphql client?)
import requests


class StrandApiClient:
    """
    This client library returns the results of a GraphQL query on {host}{endpoint}.

    If the GraphQL operation fails due to an HTTP error, will throw a CoreApiClientException.

    If there are GraphQL errors for the operation, will return the standard {'errors': [...]} GraphQL response format.
    """

    def __init__(self, host, endpoint, email, password):
        self.host = host
        self.graphql_url = f'{host}{endpoint}'

        token = self._get_token(email=email, password=password)
        self.headers = {'Authorization': f'Token {token}'}

    def query(self, operation_definition):
        print("a change here")
        full_definition = f'query {operation_definition}'
        response = requests.post(url=self.graphql_url, data={'query': full_definition}, headers=self.headers)
        if response.status_code != 200:
            raise StrandApiClientException('Query failed.', response)
        return response.json()

    def mutate(self, operation_definition):
        full_definition = f'mutation {operation_definition}'
        response = requests.post(url=self.graphql_url, data={'query': full_definition}, headers=self.headers)
        if response.status_code != 200:
            raise StrandApiClientException('Mutation failed.', response)
        return response.json()

    def _get_token(self, email, password):
        response = requests.post(url=f'{self.host}auth-token', data={'email': email, 'password': password})
        if response.status_code != 200:
            raise StrandApiClientException('Authentication failed.', response)
        return response.json()['token']


class StrandApiClientException(Exception):
    def __init__(self, message, response):
        super().__init__()
        self.message = message
        self.response = response

    def __str__(self):
        return f'{self.message}\n\tStatus: {self.response.status_code}\n\t' \
               f'Reason: {self.response.reason}\n\tText: {self.response.text}'
