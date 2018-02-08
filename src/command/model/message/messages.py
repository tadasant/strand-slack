from src.command.model.message.message_models import TopicChannelIntroMessage, DiscussionInitiationMessage

TOPIC_CHANNEL_INTRO_MESSAGE = TopicChannelIntroMessage()
INITIAL_TOPIC_CHANNEL_INTRO_MESSAGE = TopicChannelIntroMessage(is_update=False)

# these need runtime args
DISCUSSION_INITIATION_MESSAGE_FACTORY = DiscussionInitiationMessage
