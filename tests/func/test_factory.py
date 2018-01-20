import threading


class TestFactory:
    def test_create_bot(self, factory, bot_factory):
        bot_one = bot_factory.build()
        factory.create_bot(bot_one.slack_team_name, bot_one.slack_team_id,
                           bot_one.access_token, bot_one.installer_id,
                           bot_one.bot_user_id, bot_one.bot_access_token)
        assert threading.active_count() == 2

        bot_two = bot_factory.build()
        factory.create_bot(bot_two.slack_team_name, bot_two.slack_team_id,
                           bot_two.access_token, bot_two.installer_id,
                           bot_two.bot_user_id, bot_two.bot_access_token)
        assert threading.active_count() == 3

    def test_get_bots(self, factory, bot_factory):
        bot_one = bot_factory.build()
        factory.create_bot(bot_one.slack_team_name, bot_one.slack_team_id,
                           bot_one.access_token, bot_one.installer_id,
                           bot_one.bot_user_id, bot_one.bot_access_token)
        bot_two = bot_factory.build()
        factory.create_bot(bot_two.slack_team_name, bot_two.slack_team_id,
                           bot_two.access_token, bot_two.installer_id,
                           bot_two.bot_user_id, bot_two.bot_access_token)

        assert factory.get_bots() == [{'bot': bot_one.slack_team_name,
                                       'is_alive': True},
                                      {'bot': bot_two.slack_team_name,
                                       'is_alive': True}]
