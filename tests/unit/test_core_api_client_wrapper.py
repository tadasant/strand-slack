from textwrap import dedent

import pytest

from src import WrapperException
from src.domain.models.coreapi.SlackProfile import SlackProfile
from src.domain.models.coreapi.SlackUser import SlackUser
from src.wrappers.CoreApiClientWrapper import CoreApiClientWrapper
from tests.common.PrimitiveFaker import PrimitiveFaker


def test_handles_double_quotes_in_new_topic(core_api_client, mocker):
    mocker.spy(core_api_client, 'mutate')
    core_api_client_wrapper = CoreApiClientWrapper(core_api_client=core_api_client)
    with pytest.raises(WrapperException):  # TODO not ideal; won't need when core_api client queuing is removed
        core_api_client_wrapper.create_topic_from_slack(
            title='"abc"123',
            description='ab"c23"4',
            tag_names=['a"b"c', '1234'],
            original_poster_slack_user_id='someid',
        )
    assert dedent(core_api_client.mutate.call_args[1]['operation_definition']) == dedent(r'''
      {
        createTopicFromSlack(input: {title: "\"abc\"123",
                                      description: "ab\"c23\"4",
                                      originalPosterSlackUserId: "someid",
                                      tags: [{name: "a\"b\"c"},{name: "1234"}]
                                    })
        {
          topic {
            id
            title
            description
            tags {
              name
            }
            originalPoster {
              id
            }
          }
        }
      }
    ''')


def test_handles_newlines_in_new_topic(core_api_client, mocker):
    mocker.spy(core_api_client, 'mutate')
    core_api_client_wrapper = CoreApiClientWrapper(core_api_client=core_api_client)
    with pytest.raises(WrapperException):  # TODO not ideal; won't need when core_api client queuing is removed
        core_api_client_wrapper.create_topic_from_slack(
            title='abc123',
            description='abc234\nline2',
            tag_names=['abc', '1234'],
            original_poster_slack_user_id='someid',
        )
    assert dedent(core_api_client.mutate.call_args[1]['operation_definition']) == dedent(r'''
      {
        createTopicFromSlack(input: {title: "abc123",
                                      description: "abc234\nline2",
                                      originalPosterSlackUserId: "someid",
                                      tags: [{name: "abc"},{name: "1234"}]
                                    })
        {
          topic {
            id
            title
            description
            tags {
              name
            }
            originalPoster {
              id
            }
          }
        }
      }
    ''')


def test_handles_newlines_in_new_topic_with_user(core_api_client, mocker):
    mocker.spy(core_api_client, 'mutate')
    core_api_client_wrapper = CoreApiClientWrapper(core_api_client=core_api_client)
    with pytest.raises(WrapperException):  # TODO not ideal; won't need when core_api client queuing is removed
        core_api_client_wrapper.create_topic_and_user_as_original_poster_from_slack(
            title='abc"123"',
            description='abc234\nline2',
            tag_names=['abc', '1234'],
            slack_user=SlackUser(id=1, profile=SlackProfile(image_72='url')),
        )

    assert 'abc\\\"123\\\"' in core_api_client.mutate.call_args[1]['operation_definition']
    assert 'abc234\\nline2' in core_api_client.mutate.call_args[1]['operation_definition']


def test_handles_newlines_and_quotes_in_message(core_api_client, mocker):
    mocker.spy(core_api_client, 'mutate')
    core_api_client_wrapper = CoreApiClientWrapper(core_api_client=core_api_client)
    with pytest.raises(WrapperException):  # TODO not ideal; won't need when core_api client queuing is removed
        core_api_client_wrapper.create_message_from_slack(
            text='Once upon a "time"\nIn a "galaxy" *far*, _far_ "away"...',
            slack_channel_id=str(PrimitiveFaker('bban')),
            slack_event_ts="1520007783.127152",
            author_slack_user_id=1,
        )

    assert '"Once upon a \\"time\\"\\nIn a \\"galaxy\\" *far*, _far_ \\"away\\"..."' in \
           core_api_client.mutate.call_args[1]['operation_definition']


def test_handles_newlines_and_quotes_in_message_with_new_user(core_api_client, mocker):
    mocker.spy(core_api_client, 'mutate')
    core_api_client_wrapper = CoreApiClientWrapper(core_api_client=core_api_client)
    with pytest.raises(WrapperException):  # TODO not ideal; won't need when core_api client queuing is removed
        core_api_client_wrapper.create_message_and_user_as_author_from_slack(
            text='Once upon a "time"\nIn a "galaxy" *far*, _far_ "away"...',
            slack_channel_id=str(PrimitiveFaker('bban')),
            slack_event_ts="1520007783.127152",
            slack_user=SlackUser(id=1, profile=SlackProfile(image_72='url')),
        )

    assert '"Once upon a \\"time\\"\\nIn a \\"galaxy\\" *far*, _far_ \\"away\\"..."' in \
           core_api_client.mutate.call_args[1]['operation_definition']


def test_handles_newlines_and_quotes_in_reply(core_api_client, mocker):
    mocker.spy(core_api_client, 'mutate')
    core_api_client_wrapper = CoreApiClientWrapper(core_api_client=core_api_client)
    with pytest.raises(WrapperException):  # TODO not ideal; won't need when core_api client queuing is removed
        core_api_client_wrapper.create_reply_from_slack(
            text='Once upon a "time"\nIn a "galaxy" *far*, _far_ "away"...',
            slack_channel_id=str(PrimitiveFaker('bban')),
            slack_event_ts="1520007997.137676",
            slack_thread_ts="1520007783.127152",
            author_slack_user_id=1,
        )

    assert '"Once upon a \\"time\\"\\nIn a \\"galaxy\\" *far*, _far_ \\"away\\"..."' in \
           core_api_client.mutate.call_args[1]['operation_definition']


def test_handles_newlines_and_quotes_in_reply_with_new_user(core_api_client, mocker):
    mocker.spy(core_api_client, 'mutate')
    core_api_client_wrapper = CoreApiClientWrapper(core_api_client=core_api_client)
    with pytest.raises(WrapperException):  # TODO not ideal; won't need when core_api client queuing is removed
        core_api_client_wrapper.create_reply_and_user_as_author_from_slack(
            text='Once upon a "time"\nIn a "galaxy" *far*, _far_ "away"...',
            slack_channel_id=str(PrimitiveFaker('bban')),
            slack_event_ts="1520007997.137676",
            slack_thread_ts="1520007783.127152",
            slack_user=SlackUser(id=1, profile=SlackProfile(image_72='url')),
        )

    assert '"Once upon a \\"time\\"\\nIn a \\"galaxy\\" *far*, _far_ \\"away\\"..."' in \
           core_api_client.mutate.call_args[1]['operation_definition']
