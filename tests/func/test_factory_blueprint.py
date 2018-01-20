import threading

import factory


class TestFactoryBlueprint:
    def test_get_bots(self, client):
        res = client.get('/factory/bots')
        assert res.json == []

    def test_create_bot_missing_params(self, client):
        thread_count = threading.active_count()

        res = client.post('/factory/bots')

        assert res.json == dict(message=dict(slack_team_id='Missing required parameter in the JSON body or the post '
                                                           'body or the query string'))
        assert res.status_code == 400
        assert threading.active_count() == thread_count

    def test_create_bot(self, client, bot_factory):
        thread_count = threading.active_count()

        data = factory.build(dict, FACTORY_CLASS=bot_factory)
        res = client.post('/factory/bots', data=data)

        assert res.json == dict(created=True)
        assert res.status_code == 201
        assert threading.active_count() == thread_count + 1
