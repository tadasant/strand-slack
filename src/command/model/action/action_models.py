from src.command.model.action.Action import Action


class PostNewTopicButton(Action):
    def __init__(self, require_confirmation=False):
        # confirm = Confirm() if require_confirmation else None
        super().__init__(
            name='post',
            text='Post new topic',
            style='primary',
            type='button',
            value='post'
        )


class CloseDiscussionButton(Action):
    def __init__(self):
        super().__init__(
            name='close',
            text='Close discussion',
            type='button',
            value='close'
        )
