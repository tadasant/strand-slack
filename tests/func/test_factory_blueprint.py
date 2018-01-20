class TestFactoryBlueprint:
    def test_get_bots(self, client):
        res = client.get('/factory/bots')
        assert res.json == []

    def test_create_bot(self, client):
        res = client.post('/factory/bots')
        assert res.json == {}
