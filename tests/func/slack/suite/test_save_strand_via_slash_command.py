from tests.func.slack.TestSlackFixtures import TestSlackFixtures


class TestSaveStrandViaSlashCommand(TestSlackFixtures):
    """Test the flow for a user saving a strand via Slash Command"""

    target_endpoint = 'slack.slashcommandresource'
    default_headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def test_save_installed_user_no_start_phrase(self):
        """Extract channel history, forward to Strand API, send user ephemeral message"""
        pass

    def test_save_installed_user_start_phrase(self):
        """Extract channel history, splice by start phrase, forward to Strand API, send user ephemeral message"""
        pass

    def test_save_installed_user_invalid_start_phrase(self):
        """Extract channel history, splice by start phrase, raise exception, send user ephemeral message"""
        pass

    def test_save_installed_user_group(self):
        """Extract group history, splice by start phrase, forward to Strand API, send user ephemeral message"""
        pass

    def test_save_installed_user_mpim(self):
        """Extract mpim history, splice by start phrase, forward to Strand API, send user ephemeral message"""
        pass

    def test_save_installed_user_im(self):
        """Extract im history, splice by start phrase, forward to Strand API, send user ephemeral message"""
        pass

    def test_save_uninstalled_user(self):
        """Fail quietly"""
        pass
