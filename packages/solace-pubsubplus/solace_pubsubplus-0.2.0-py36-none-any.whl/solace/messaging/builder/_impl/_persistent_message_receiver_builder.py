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

"""Module contains the implementation class and methods for the PersistentMessageReceiverBuilder"""
# pylint: disable=trailing-whitespace

import typing
from typing import List

from solace.messaging.builder.persistent_message_receiver_builder import PersistentMessageReceiverBuilder
from solace.messaging.config.missing_resources_creation_configuration import MissingResourcesCreationStrategy
from solace.messaging.config.receiver_activation_passivation_configuration import ReceiverStateChangeListener
from solace.messaging.receiver._impl._persistent_message_receiver import _PersistentMessageReceiver
from solace.messaging.receiver.persistent_message_receiver import PersistentMessageReceiver
from solace.messaging.resources.queue import Queue

if typing.TYPE_CHECKING:
    from solace.messaging.messaging_service import MessagingService


class _PersistentMessageReceiverBuilder(PersistentMessageReceiverBuilder) \
        :  # pylint: disable=too-many-ancestors,too-many-instance-attributes, missing-class-docstring, missing-module-docstring
    # """Builder class for persistent message receiver"""

    def __init__(self, messaging_service: 'MessagingService'):
        self._messaging_service: 'MessagingService' = messaging_service
        self._strategy: MissingResourcesCreationStrategy
        self._strategy = None
        self._receiver_state_change_listener: ReceiverStateChangeListener
        self._receiver_state_change_listener = None
        self._topics: List = list()
        self._config: dict = dict()
        self._message_selector: str
        self._message_selector = ''
        self._auto_ack: bool = False
        self._endpoint_to_consume_from: Queue
        self._endpoint_to_consume_from = None

    def with_activation_passivation_support(self, receiver_state_change_listener: ReceiverStateChangeListener) \
            -> 'PersistentMessageReceiverBuilder':
        """Enables receiver to receive broker notifications about state changes of the give receiver instance"""
        self._receiver_state_change_listener = receiver_state_change_listener
        return self

    def with_subscriptions(self, subscriptions: List['TopicSubscription']) -> 'PersistentMessageReceiverBuilder':
        """Adds a list of subscriptions to be applied to all MessageReceiver subsequently created with
        this builder."""
        self._topics.extend(subscriptions)
        return self

    def from_properties(self, configuration: dict) -> 'PersistentMessageReceiverBuilder':
        """Set PersistentMessageReceiver properties from the dictionary of (property,value) tuples."""
        self._config = configuration
        return self

    def with_missing_resources_creation_strategy(self, strategy: 'MissingResourcesCreationStrategy') \
            -> 'PersistentMessageReceiverBuilder':
        """Implementation method for creating a PersistentMessageReceiverBuilder
         using the MissingResourcesCreationStrategy"""
        self._strategy = strategy
        return self

    def with_message_auto_acknowledgement(self) -> 'PersistentMessageReceiverBuilder':
        """Implementation method for creating a PersistentMessageReceiverBuilder using the
        message auto acknowledgement
        """
        self._auto_ack = True
        return self

    def with_message_selector(self, selector_query_expression: str) -> 'PersistentMessageReceiverBuilder':
        """Implementation method for creating the PersistentMessageReceiverBuilder using the message
        selector expression for selecting the messages based on the expression
        """
        self._message_selector = selector_query_expression
        return self

    @property
    def messaging_service(self):
        """property to hold and return the messaging service"""
        return self._messaging_service

    @property
    def strategy(self):
        """property to hold and return the ReconnectionRetryStrategy"""
        return self._strategy

    @property
    def receiver_state_change_listener(self):
        """property to hold and return the receiver state change listener value"""
        return self._receiver_state_change_listener

    @property
    def topics(self):
        """property to hold and return the topics"""
        return self._topics

    @property
    def config(self):
        """property to hold and return the configuration dictionary"""
        return self._config

    @property
    def message_selector(self):
        """property to hold and return the message selector expression"""
        return self._message_selector

    @property
    def endpoint_to_consume_from(self):
        """property to hold and return the endpoint from which a message to be consumed"""
        return self._endpoint_to_consume_from

    @property
    def auto_ack(self):
        """property to hold and return the auto acknowledgement value"""
        return self._auto_ack

    def build(self, endpoint_to_consume_from: Queue) -> PersistentMessageReceiver:
        """Implementation method to build the PersistentMessageReceiver"""
        self._endpoint_to_consume_from = endpoint_to_consume_from
        return _PersistentMessageReceiver(self)
