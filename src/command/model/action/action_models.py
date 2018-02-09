from src.command.model.action.Action import Action
from src.command.model.action.Confirm import Confirm


class PostNewTopicButton(Action):
    def __init__(self, require_confirmation=False):
        confirm = Confirm(
            title='Are you sure?',
            text='This will start a new discussion',
            ok_text='Yes',
            dismiss_text='No'
        ) if require_confirmation else None
        super().__init__(
            name='post',
            text='Post new topic',
            style='primary',
            type='button',
            value='post',
            confirm=confirm
        )


class CloseDiscussionButton(Action):
    def __init__(self):
        super().__init__(
            name='close',
            text='Close discussion',
            type='button',
            value='close'
        )
