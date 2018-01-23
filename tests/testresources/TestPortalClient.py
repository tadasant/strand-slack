class TestPortalClient:
    def __init__(self, host, endpoint):
        self.url = f'{host}{endpoint}'

    def query(self, operation_definition):
        full_definition = f'query {operation_definition}'
        response = requests.post(url=self.url, data={'query': full_definition})
        if response.status_code != 200:
            raise TestPortalClientException('Query failed.', response)
        return response.json()['data']