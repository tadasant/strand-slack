from flask import url_for


class TestBotList:
    def test_get_bots(self, client):
        res = client.get(url_for('factory.botlist', _external=True))
        assert res.json == []

    def test_create_bot(self, client):
        res = client.post(url_for('factory.botlist', _external=True))
        assert res.json == {}
