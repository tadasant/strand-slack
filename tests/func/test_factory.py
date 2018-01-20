import threading


class TestFactory:
    def test_create_bot(self, factory, bot_settings_factory):
        bot_one_settings = bot_settings_factory.build()
        factory.create_bot(bot_one_settings)

        assert threading.active_count() == 2

        bot_two_settings = bot_settings_factory.build()
        factory.create_bot(bot_two_settings)

        assert threading.active_count() == 3

    def test_get_bots(self, factory, bot_settings_factory):
        bot_one_settings = bot_settings_factory.build()
        factory.create_bot(bot_one_settings)
        bot_two_settings = bot_settings_factory.build()
        factory.create_bot(bot_two_settings)

        assert factory.get_bots() == [{'slack_team_id': bot_one_settings.slack_team_id,
                                       'slack_team_name': bot_one_settings.slack_team_name,
                                       'is_alive': True},
                                      {'slack_team_id': bot_two_settings.slack_team_id,
                                       'slack_team_name': bot_two_settings.slack_team_name,
                                       'is_alive': True}]
