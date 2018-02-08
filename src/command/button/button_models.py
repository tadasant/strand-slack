from src.command.button.Action import Action
from src.command.button.Button import Button


class PostNewTopicButton(Button):
    def __init__(self):
        super().__init__(
            fallback=f'Can\'t display the button, please use `/codeclippy post`',
            callback_id='post_new_topic',
            color='#3AA3E3',
            attachment_type='default',
            actions=[Action(
                name='post',
                text='Post new topic',
                style='primary',
                type='button',
                value='post'
            )]
        )
