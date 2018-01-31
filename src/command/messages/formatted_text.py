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
