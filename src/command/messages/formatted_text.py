from textwrap import dedent


def discussion_initiation_message(original_poster_slack_user_id, title, description, tags):
    return dedent(f'''
        *OP*: <@{original_poster_slack_user_id}>
        *Title*: {title}
        *Description*: {description}
        *Tags*: {tags}

        <@{original_poster_slack_user_id}>: please `/codeclippy close` this discussion when you are done

        Do not post sensitive information! A transcript of this discussion will be available on www.codeclippy.com.
    ''')


def discussion_initiation_dm(slack_channel_id):
    return dedent(f'''
        Your discussion has been started at <#{slack_channel_id}>. Check it out!

        Please write `/codeclippy close` when the discussion is over.
    ''')


def close_discussion(closer_slack_user_id):
    return dedent(f'''
        <@{closer_slack_user_id}> has marked this discussion as closed.

        At this time, no more messages will be allowed in this channel.

        This conversation will be archived and may be reviewed on www.codeclippy.com
    ''')


def block_topic_channel_message(attempted_message):
    return dedent(f'''
        I\'m sorry but users may not post in this channel. Here's the message you tried to send:\n\n{attempted_message}
    ''')
