import threading


class TestFactoryBlueprint:
    def test_get_bots(self, client):
        res = client.get('/factory/bots')
        assert res.json == []

    def test_create_bot(self, client):
        assert threading.active_count() == 1
        res = client.post('/factory/bots')
        assert res.json == {'created': True}
        assert threading.active_count() == 2
