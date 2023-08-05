# pubsubplus-python-client
#
# Copyright 2020 Solace Corporation. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Module contains the implementation class and methods for the DirectMessageReceiverBuilder"""

from typing import List

from solace.messaging.builder.direct_message_receiver_builder import DirectMessageReceiverBuilder
from solace.messaging.receiver._impl._direct_message_receiver import _DirectMessageReceiver
from solace.messaging.receiver.direct_message_receiver import DirectMessageReceiver
from solace.messaging.resources.share_name import ShareName, _ShareName
from solace.messaging.resources.topic_subscription import TopicSubscription


class _DirectMessageReceiverBuilder(DirectMessageReceiverBuilder)\
        :  # pylint: disable=missing-class-docstring, missing-module-docstring

    def __init__(self, messaging_service: 'MessagingService'):
        self._messaging_service: 'MessagingService' = messaging_service
        self._topic_subscriptions = list()

    def with_subscriptions(self, subscriptions: List[TopicSubscription]) -> 'DirectMessageReceiverBuilder':
        # """
        # Add a list of subscriptions to be applied to all DirectMessageReceiver subsequently created with
        # this builder.
        # Args:
        #     subscriptions (List[TopicSubscription]): subscriptions list of topic subscriptions to be added
        # Returns:
        #     DirectMessageReceiverBuilder instance for method chaining
        # """
        self._topic_subscriptions = list()
        for topic in subscriptions:
            self._topic_subscriptions.append(topic.get_name())
        return self

    # TODO missing implementation no suitable prop available for direct receiver
    def from_properties(self, configuration: dict) -> 'DirectMessageReceiverBuilder':
        # """
        # Set DirectMessageReceiver properties from the dictionary of (property,value) tuples.
        # Args:
        #     configuration (dict): configuration properties
        # Returns:
        #     DirectMessageReceiverBuilder instance for method chaining
        # """
        return self

    def build(self, shared_subscription_group: ShareName = None) -> DirectMessageReceiver:

        topic_dict = dict()
        topic_dict['subscriptions'] = self._topic_subscriptions
        if shared_subscription_group:
            name = shared_subscription_group.get_name()
            share_name = _ShareName(name)
            share_name.validate()
            topic_dict['group_name'] = name
        return _DirectMessageReceiver(self._messaging_service, topic_dict)
