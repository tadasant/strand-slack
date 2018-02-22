from textwrap import dedent

import pytest

from src import WrapperException
from src.wrappers.PortalClientWrapper import PortalClientWrapper


def test_handles_double_quotes_in_new_topic(portal_client, mocker):
    mocker.spy(portal_client, 'mutate')
    portal_client_wrapper = PortalClientWrapper(portal_client=portal_client)
    with pytest.raises(WrapperException):  # TODO not ideal; won't need when portal client queuing is removed
        portal_client_wrapper.create_topic(
            title='"abc"123',
            description='ab"c23"4',
            tag_names=['a"b"c', '1234'],
            original_poster_slack_user_id='someid',
        )
    assert dedent(portal_client.mutate.call_args[1]['operation_definition']) == dedent(r'''
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
          }
        }
      }
    ''')


def test_handles_newlines_in_new_topic(portal_client, mocker):
    mocker.spy(portal_client, 'mutate')
    portal_client_wrapper = PortalClientWrapper(portal_client=portal_client)
    with pytest.raises(WrapperException):  # TODO not ideal; won't need when portal client queuing is removed
        portal_client_wrapper.create_topic(
            title='abc123',
            description='abc234\nline2',
            tag_names=['abc', '1234'],
            original_poster_slack_user_id='someid',
        )
    assert dedent(portal_client.mutate.call_args[1]['operation_definition']) == dedent(r'''
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
          }
        }
      }
    ''')
