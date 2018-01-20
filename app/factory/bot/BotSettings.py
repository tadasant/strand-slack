from collections import namedtuple

BotSettings = namedtuple(
    'BotSettings',
    ['slack_team_name', 'slack_team_id', 'access_token', 'installer_id', 'bot_user_id', 'bot_access_token']
)
