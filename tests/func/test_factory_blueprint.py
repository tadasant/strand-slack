import threading

import factory


class TestFactoryBlueprint:
    def test_get_bots(self, client, bot_settings_factory):
        bot_one_data = factory.build(dict, FACTORY_CLASS=bot_settings_factory)

        res = client.get('/factory/bots')
        assert res.json == []

        client.post('/factory/bots', data=bot_one_data)

        res = client.get('/factory/bots')
        assert res.json == [{'slack_team_id': bot_one_data['slack_team_id'],
                             'slack_team_name': bot_one_data['slack_team_name'],
                             'is_alive': True}]

    def test_create_bot_missing_params(self, client):
        thread_count = threading.active_count()

        res = client.post('/factory/bots')

        assert res.json == dict(message=dict(slack_team_id='Missing required parameter in the JSON body or the post '
                                                           'body or the query string'))
        assert res.status_code == 400
        assert threading.active_count() == thread_count

    def test_create_bot_duplicate(self, client, bot_settings_factory):
        bot_one_data = factory.build(dict, FACTORY_CLASS=bot_settings_factory)
        bot_two_data = factory.build(dict, FACTORY_CLASS=bot_settings_factory)
        bot_two_data['slack_team_id'] = bot_one_data['slack_team_id']

        client.post('/factory/bots', data=bot_one_data)
        res = client.post('/factory/bots', data=bot_two_data)

        assert res.status_code == 400
        assert res.json == dict(message=dict(slack_team_id='Bot already exists for this id'))

    def test_create_bot(self, client, bot_settings_factory):
        thread_count = threading.active_count()

        data = factory.build(dict, FACTORY_CLASS=bot_settings_factory)
        res = client.post('/factory/bots', data=data)

        assert res.json == {'is_alive': True,
                            'slack_team_id': data['slack_team_id'],
                            'slack_team_name': data['slack_team_name']}
        assert res.status_code == 201
        assert threading.active_count() == thread_count + 1
