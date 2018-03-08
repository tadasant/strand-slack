import json

from tenacity import Retrying, wait_fixed, stop_after_attempt, retry_if_exception_type, after_log

from src.clients.CoreApiClient import CoreApiClientException
from src.common.logging import get_logger
from src.domain.models.coreapi.Discussion import DiscussionSchema
from src.domain.models.coreapi.SlackAgent import SlackAgentSchema
from src.domain.models.coreapi.SlackAgentStatus import SlackAgentStatus
from src.domain.models.coreapi.Topic import TopicSchema
# TODO [SLA-26] Add authentication
from src.domain.models.exceptions.WrapperException import WrapperException
from src.domain.models.utils import dict_keys_camel_case_to_underscores


class CoreApiClientWrapper:
    """Manage all outgoing interaction with the CoreApi"""

    def __init__(self, core_api_client):
        self.core_api_client = core_api_client
        self.logger = get_logger('CoreApiClientWrapper')
        self.standard_retrier = Retrying(
            reraise=True,
            wait=wait_fixed(2),
            stop=stop_after_attempt(5),
            after=after_log(logger=self.logger, log_level=self.logger.getEffectiveLevel()),
            retry=retry_if_exception_type(CoreApiClientException)
        )

    def get_slack_agents(self):
        operation_definition = '''
            {
                slackAgents {
                    status
                    topicChannelId
                    slackTeam {
                        id
                    }
                    slackApplicationInstallation {
                        accessToken
                        installer {
                            id
                        }
                        botAccessToken
                        botUserId
                    }
                }
            }
        '''
        response_body = self.standard_retrier.call(self.core_api_client.query,
                                                   operation_definition=operation_definition)
        return self._deserialize_response_body(response_body=response_body, ObjectSchema=SlackAgentSchema,
                                               path_to_object=['data', 'slackAgents'], many=True)

    def update_topic_channel_and_activate_agent(self, slack_team_id, topic_channel_id):
        operation_definition = f'''
            {{
                updateSlackAgentTopicChannelAndActivate(input: {{slackTeamId: "{slack_team_id}",
                                                                topicChannelId: "{topic_channel_id}"}}) {{
                    slackAgent {{
                        topicChannelId
                        status
                    }}
                }}
            }}
        '''
        response_body = self.standard_retrier.call(self.core_api_client.mutate,
                                                   operation_definition=operation_definition)
        result = self._deserialize_response_body(
            response_body=response_body, ObjectSchema=SlackAgentSchema,
            path_to_object=['data', 'updateSlackAgentTopicChannelAndActivate', 'slackAgent']
        )
        assert result.status == SlackAgentStatus.ACTIVE, 'Call to activate Slack Agent oddly did not transition'
        return result

    def create_topic_from_slack(self, title, description, original_poster_slack_user_id, tag_names):
        # TODO: [CCP-89] add composite PK on slack_team bc slack_user_id should not be unique
        # TODO: Drop description field
        title = json.dumps(title)
        description = json.dumps(description)
        tag_names = [json.dumps(name) for name in tag_names]
        operation_definition = f'''
          {{
            createTopicFromSlack(input: {{title: {title},
                                          description: {description},
                                          originalPosterSlackUserId: "{original_poster_slack_user_id}",
                                          tags: [{','.join([f'{{name: {name}}}' for name in tag_names])}]
                                        }})
            {{
              topic {{
                id
                title
                description
                tags {{
                  name
                }}
                originalPoster {{
                  id
                }}
              }}
            }}
          }}
        '''
        response_body = self.standard_retrier.call(self.core_api_client.mutate,
                                                   operation_definition=operation_definition)
        return self._deserialize_response_body(
            response_body=response_body, ObjectSchema=TopicSchema,
            path_to_object=['data', 'createTopicFromSlack', 'topic']
        )

    def create_topic_and_user_as_original_poster_from_slack(self, title, description, slack_user, tag_names):
        title = json.dumps(title)
        description = json.dumps(description)
        tag_names = [json.dumps(name) for name in tag_names]

        operation_definition = f'''
            {{
              createUserAndTopicFromSlack(input: {{title: {title},
                                                   description: {description},
                                                   originalPosterSlackUser: {{
                                                     id: "{slack_user.id}",
                                                     name: "{slack_user.name}",
                                                     firstName: "{slack_user.profile.first_name}",
                                                     lastName: "{slack_user.profile.last_name}",
                                                     realName: "{slack_user.real_name}",
                                                     displayName: "{slack_user.profile.display_name}",
                                                     email: "{slack_user.profile.email}",
                                                     image72: "{slack_user.profile.image_72}",
                                                     isBot: {str(slack_user.is_bot).lower()},
                                                     isAdmin: {str(slack_user.is_admin).lower()},
                                                     slackTeamId: "{slack_user.team_id}"
                                                   }},
                                                   tags: [
                                                       {','.join([f'{{name: {name}}}' for name in tag_names])}
                                                   ]}}) {{
                topic {{
                  id
                  title
                  description
                  tags {{
                    name
                  }}
                  originalPoster {{
                    id
                  }}
                }}
              }}
            }}
        '''
        response_body = self.standard_retrier.call(self.core_api_client.mutate,
                                                   operation_definition=operation_definition)
        return self._deserialize_response_body(
            response_body=response_body, ObjectSchema=TopicSchema,
            path_to_object=['data', 'createUserAndTopicFromSlack', 'topic']
        )

    def create_discussion(self, topic_id):
        operation_definition = f'''
        {{
            createDiscussion(input: {{topicId: {topic_id}}}) {{
              discussion {{
                id
              }}
            }}
        }}
        '''
        response_body = self.standard_retrier.call(self.core_api_client.mutate,
                                                   operation_definition=operation_definition)
        return self._deserialize_response_body(
            response_body=response_body, ObjectSchema=DiscussionSchema,
            path_to_object=['data', 'createDiscussion', 'discussion']
        )

    def create_discussion_from_slack(self, topic_id, slack_channel, slack_team_id):
        operation_definition = f'''
        {{
            createDiscussionFromSlack(input: {{discussion: {{topicId: {topic_id}}},
                                               id: "{slack_channel.id}",
                                               name: "{slack_channel.name}",
                                               slackTeamId: "{slack_team_id}"}}) {{
              discussion {{
                id
              }}
            }}
          }}
        '''
        response_body = self.standard_retrier.call(self.core_api_client.mutate,
                                                   operation_definition=operation_definition)
        self._validate_no_response_body_errors(response_body=response_body)

    def create_message(self, text, discussion_id, author_id, time):
        text = json.dumps(text)

        operation_definition = f'''
          {{
            createMessage(input: {{text: {text},
                                   discussionId: {discussion_id},
                                   authorId: {author_id},
                                   time: "{time}"}}) {{
              message {{
                id
              }}
            }}
          }}
        '''
        response_body = self.standard_retrier.call(self.core_api_client.mutate,
                                                   operation_definition=operation_definition)
        self._validate_no_response_body_errors(response_body=response_body)

    def create_message_from_slack(self, text, slack_channel_id, slack_event_ts, author_slack_user_id):
        text = json.dumps(text)

        operation_definition = f'''
          {{
            createMessageFromSlack(input: {{text: {text},
                                            slackChannelId: "{slack_channel_id}",
                                            slackUserId: "{author_slack_user_id}",
                                            originSlackEventTs: "{slack_event_ts}"}}) {{
              message {{
                id
              }}
            }}
          }}
        '''
        response_body = self.standard_retrier.call(self.core_api_client.mutate,
                                                   operation_definition=operation_definition)
        self._validate_no_response_body_errors(response_body=response_body)

    def create_message_and_user_as_author_from_slack(self, text, slack_channel_id, slack_event_ts, slack_user):
        text = json.dumps(text)

        operation_definition = f'''
          {{
            createUserAndMessageFromSlack(input: {{text: {text},
                                            slackChannelId: "{slack_channel_id}",
                                            slackUser: {{
                                              id: "{slack_user.id}",
                                              name: "{slack_user.name}",
                                              firstName: "{slack_user.profile.first_name}",
                                              lastName: "{slack_user.profile.last_name}",
                                              realName: "{slack_user.real_name}",
                                              displayName: "{slack_user.profile.display_name}",
                                              email: "{slack_user.profile.email}",
                                              image72: "{slack_user.profile.image_72}",
                                              isBot: {str(slack_user.is_bot).lower()},
                                              isAdmin: {str(slack_user.is_admin).lower()},
                                              slackTeamId: "{slack_user.team_id}"
                                            }},
                                            originSlackEventTs: "{slack_event_ts}"}}) {{
              message {{
                id
              }}
            }}
          }}
        '''
        response_body = self.standard_retrier.call(self.core_api_client.mutate,
                                                   operation_definition=operation_definition)
        self._validate_no_response_body_errors(response_body=response_body)

    def create_reply_from_slack(self, text, slack_channel_id, slack_event_ts, slack_thread_ts, author_slack_user_id):
        # TODO: Drop originSlackEventTs
        text = json.dumps(text)

        operation_definition = f'''
          {{
            createReplyFromSlack(input: {{text: {text},
                                          messageOriginSlackEventTs: "{slack_thread_ts}",
                                          slackChannelId: "{slack_channel_id}",
                                          slackUserId: "{author_slack_user_id}",
                                          originSlackEventTs: "{slack_event_ts}"}}) {{
              reply {{
                id
              }}
            }}
          }}
        '''
        response_body = self.standard_retrier.call(self.core_api_client.mutate,
                                                   operation_definition=operation_definition)
        self._validate_no_response_body_errors(response_body=response_body)

    def create_reply_and_user_as_author_from_slack(self, text, slack_channel_id, slack_event_ts, slack_thread_ts,
                                                   slack_user):
        # TODO: Drop originSlackEventTs
        text = json.dumps(text)

        operation_definition = f'''
          {{
            createUserAndReplyFromSlack(input: {{text: {text},
                                                 originSlackEventTs: "{slack_thread_ts}",
                                                 slackChannelId: "{slack_channel_id}",
                                                 slackUser: {{
                                                   id: "{slack_user.id}",
                                                   name: "{slack_user.name}",
                                                   firstName: "{slack_user.profile.first_name}",
                                                   lastName: "{slack_user.profile.last_name}",
                                                   realName: "{slack_user.real_name}",
                                                   displayName: "{slack_user.profile.display_name}",
                                                   email: "{slack_user.profile.email}",
                                                   image72: "{slack_user.profile.image_72}",
                                                   isBot: {str(slack_user.is_bot).lower()},
                                                   isAdmin: {str(slack_user.is_admin).lower()},
                                                   slackTeamId: "{slack_user.team_id}"
                                                 }},
                                                 messageOriginSlackEventTs: "{slack_event_ts}"}}) {{
              reply {{
                id
              }}
            }}
          }}
        '''
        response_body = self.standard_retrier.call(self.core_api_client.mutate,
                                                   operation_definition=operation_definition)
        self._validate_no_response_body_errors(response_body=response_body)

    def close_discussion(self, discussion_id):
        # TODO: During shift to 0.2, API needs to be updated to validate discussion closer
        operation_definition = f'''
        {{
            closeDiscussion(input: {{id: {discussion_id}}}) {{
              discussion {{
                id
              }}
            }}
        }}
        '''
        response_body = self.standard_retrier.call(self.core_api_client.mutate,
                                                   operation_definition=operation_definition)
        return self._deserialize_response_body(
            response_body=response_body, ObjectSchema=DiscussionSchema,
            path_to_object=['data', 'closeDiscussion', 'discussion']
        )

    def close_discussion_from_slack(self, slack_channel_id, slack_user_id):
        # TODO shouldn't rely on slackChannelId being unique (need slack_team_id as well)
        operation_definition = f'''
          {{
            closeDiscussionFromSlack(input: {{slackChannelId: "{slack_channel_id}",
                                              slackUserId: "{slack_user_id}"}}) {{
              discussion {{
                id
              }}
            }}
          }}
        '''
        response_body = self.standard_retrier.call(self.core_api_client.mutate,
                                                   operation_definition=operation_definition)
        self._validate_no_response_body_errors(response_body=response_body)

    def mark_discussion_as_pending_closed_from_slack(self, slack_channel_id):
        # TODO shouldn't rely on slackChannelId being unique (need slack_team_id as well)
        operation_definition = f'''
          {{
            markDiscussionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel_id}"}}) {{
              discussion {{
                status
              }}
            }}
          }}
        '''
        response_body = self.standard_retrier.call(self.core_api_client.mutate,
                                                   operation_definition=operation_definition)
        self._validate_no_response_body_errors(response_body=response_body)

    def _deserialize_response_body(self, response_body, ObjectSchema, path_to_object, many=False):
        """Deserializes response_body[**path_to_object] using ObjectSchema"""
        self._validate_no_response_body_errors(response_body=response_body)
        result_json = response_body
        for key in path_to_object:
            result_json = result_json[key]
        if many:
            return [ObjectSchema().load(dict_keys_camel_case_to_underscores(x)).data for x in result_json]
        return ObjectSchema().load(dict_keys_camel_case_to_underscores(result_json)).data

    def _validate_no_response_body_errors(self, response_body):
        """Raises an exception if there are any errors in response_body"""
        if 'errors' in response_body:
            message = f'Errors when calling CoreApiClient. Body: {response_body}'
            raise WrapperException(wrapper_name='CoreApiClient', message=message, errors=response_body['errors'])
