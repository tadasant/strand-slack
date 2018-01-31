from textwrap import dedent


def discussion_initiation_message(original_post_slack_user_id, title, description, tags):
    return dedent(f'''
        *OP*: <@{original_post_slack_user_id}>
        *Title*: {title}
        *Description*: {description}
        *Tags*: {tags}

        <@{original_post_slack_user_id}>: please `/codeclippy close` this discussion when you are done

        Do not post sensitive information! A transcript of this discussion will be available on www.codeclippy.com.
    ''')


def discussion_initiation_dm(slack_channel_id):
    return dedent(f'''
        Your discussion has been started at <#{slack_channel_id}>. Check it out!

        Please `/codeclippy close` it (invoke the command inside the channel) when the discussion is over.
    ''')
