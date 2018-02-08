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


def topic_queue_message(discussion_channel_id, original_poster_slack_user_id, title, tags):
    return dedent(f'''
        *Channel*: <#{discussion_channel_id}>
        *OP*: <@{original_poster_slack_user_id}>
        *Title*: {title}
        *Tags*: {tags}
    ''')


def discussion_initiation_dm(slack_channel_id):
    return dedent(f'''
        Your discussion has been started at <#{slack_channel_id}>. Check it out!

        Please `/codeclippy close` it (invoke the command inside the channel) when the discussion is over.
    ''')


def topic_channel_introduction():
    return dedent(f'''
        This channel is a live view of the topics of all discussions going on right now.

        `/codeclippy post` to start another one!
    ''')


def topic_channel_introduction_repost():
    return dedent(f'''
        I updated my last message with a new topic for discussion, check it out! :fire:

        This channel is a live view of the topics of all discussions going on right now.

        `/codeclippy post` to start another one!
    ''')


def close_discussion(closer_slack_user_id):
    return dedent(f'''
        <@{closer_slack_user_id}> has marked this discussion as closed.

        At this time, no more messages will be allowed in this channel.

        This conversation will be archived and may be reviewed on www.codeclippy.com
    ''')
