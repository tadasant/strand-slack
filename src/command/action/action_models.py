from src.command.action.Action import Action


class PostNewTopicButton(Action):
    def __init__(self):
        super().__init__(
            name='post',
            text='Post new topic',
            style='primary',
            type='button',
            value='post'
        )
