from src.command.model.message.message_models import TopicChannelIntroMessage, DiscussionInitiationMessage, \
    StaleDiscussionMessage

# TODO ideally (if # of messages, etc, start to blow up) there should be a Factory level to this creation
# This would mean no inconsistency between invoking some formatting directly versus having to provide runtime args

TOPIC_CHANNEL_INTRO_MESSAGE = TopicChannelIntroMessage()
INITIAL_TOPIC_CHANNEL_INTRO_MESSAGE = TopicChannelIntroMessage(is_update=False)
STALE_DISCUSSION_MESSAGE = StaleDiscussionMessage()

# These need runtime args
DiscussionInitiationMessage = DiscussionInitiationMessage
