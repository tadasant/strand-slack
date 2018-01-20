from collections import namedtuple

BotSettings = namedtuple(
    'BotSettings',
    'SLACK_TEAM_NAME, SLACK_TEAM_ID, ACCESS_TOKEN, INSTALLER_ID, BOT_USER_ID, BOT_ACCESS_TOKEN'
)
