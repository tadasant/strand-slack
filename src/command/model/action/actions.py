from src.command.model.action.action_models import PostNewTopicButton, CloseDiscussionButton

POST_NEW_TOPIC_BUTTON = PostNewTopicButton()
POST_NEW_TOPIC_BUTTON_WITH_CONFIRM = PostNewTopicButton(require_confirmation=True)
CLOSE_DISCUSSION_BUTTON = CloseDiscussionButton()
