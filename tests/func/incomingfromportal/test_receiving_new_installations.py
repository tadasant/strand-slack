class TestReceivingNewInstallations:
    def test_receive_valid_installation(self, factory, bot_settings_factory):
        bot_one_settings = bot_settings_factory.build()
        factory.create_bot(bot_one_settings)

        assert threading.active_count() == 2

        bot_two_settings = bot_settings_factory.build()
        factory.create_bot(bot_two_settings)

        assert threading.active_count() == 3

    def test_receive_invalid_installation(self, factory, bot_settings_factory):
        bot_one_settings = bot_settings_factory.build()
        factory.create_bot(bot_one_settings)

        assert threading.active_count() == 2

        bot_two_settings = bot_settings_factory.build()
        factory.create_bot(bot_two_settings)

        assert threading.active_count() == 3
