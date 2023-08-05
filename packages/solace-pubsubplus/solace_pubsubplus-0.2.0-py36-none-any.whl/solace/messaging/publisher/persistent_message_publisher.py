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

# pylint: disable=trailing-whitespace

"""
Module that contains Persistent Message Publisher.

A Persistent Message Publisher must be created by
:py:class:`solace.messaging.builder.persistent_message_publisher_builder.PersistentMessagePublisherBuilder`. The
``PersistentMessagePublisher`` instance is used to publish Guaranteed Messages created by a
:py:class:`solace.messaging.publisher.outbound_message.OutboundMessageBuilder`. The
Topic (or destination) can be added once the message is a published.

The persistent message publisher can also be used to publish simple messages containing only a bytearray or
string payload.
"""
from abc import ABC, abstractmethod
from typing import Union, Any

from solace.messaging.publisher.message_publisher import MessagePublisher
from solace.messaging.publisher.outbound_message import OutboundMessage
from solace.messaging.resources.topic import Topic


class PersistentMessagePublisher(MessagePublisher, ABC):  # pylint: disable=too-many-ancestors
    """
    A class that defines the interface to a publisher for persistent messages.

    NOTE:
        The ``DeliveryReceipt`` is available asynchronously via :py:class:`solace.messaging.publisher.persistent_message_publisher.MessageDeliverListener`.
        Message correlation tokens are used to DeliveryReceipt.

    Alternatively, applications can get delivery confirmation by publishing with the synchronous method
    :py:meth:`PersistentMessagePublisherpublish_await_acknowledgement()` which does
    not return until the published message has been acknowledged by the PubSub+ event broker.
    """

    @abstractmethod
    def set_message_delivery_listener(self, listener: 'MessageDeliveryListener'):
        """
        Set the MessageDeliveryListener for the given instance of the publisher. It is used to
        handle broker message acknowledgement or broker message reject for all the messages published.

        Args:
            listener(MessageDeliveryListener): A listener that handles message delivery confirmations or message delivery failures.
        """

    @abstractmethod
    def publish(self, message: Union[bytearray, str, OutboundMessage], destination: Topic, user_context: Any = None,
                additional_message_properties: dict = None):
        """
        Send and outbound message to the given destination.

        The :py:class:`solace.messaging.builder.outbound_message.OutboundMessageBuilder` can be used
        to create the ``OutboundMessage`` instance.  Alternatively, a bytearray or string payload can be passed
        to this function and the API will create a py:class:`solace.messaging.core.message.Message` to send.

        Args:
            message (bytearray, str, OutboundMessage): The message or the or payload to publish.
            destination ()Topic: The destination to add to the message.
            user_context (Any): The context of the message.
            additional_message_properties(dict) : Additional properties, to customize a particular message. Each key can be customer provided, or it can be a key from a solace.messaging.config.solace_properties.message_properties object.

        Raises:
            PubSubPlusClientError: When message can't be send and retry attempts would not help
            PublisherOverflowError: Thrown when publisher publishes messages faster then IO capabilities allow to send and/or internal message buffering capabilities are exceeded
        """

    @abstractmethod
    def publish_await_acknowledgement(self, message: Union[bytearray, str, OutboundMessage], destination: Topic,
                                      time_out: int = None, additional_message_properties: dict = None):
        """
        Send a persistent message, blocking until delivery acknowledgement is received or timeout
        occurs

        Args:
            message (bytearray, str, OutboundMessage): The message to send.
            destination (Topic): The message topic to send to, which is the message destination.
            time_out (int): The maximum time (in milliseconds) to wait for a message acknowledgement.
            additional_message_properties (dict):Additional properties, to customize a particular message. Each key can be customer provided, or it can be a key from a solace.messaging.config.solace_properties.message_properties object.

        Raises:
            PubSubTimeoutError: After specified timeout when no-response received.
            MessageRejectedByBrokerError: When a message was rejected from a broker for some reason.
            PublisherOverflowError: When publisher publishes too fast, message can be republished immediately or after some time
            MessageDestinationDoesNotExistError: When a given message destination does not exist.
            MessageNotAcknowledgedByBrokerError: When a message broker could not acknowledge message persistence on an event broker.
            PubSubPlusClientError: When some internal error occurs.
            IllegalArgumentError:  When the value of timeout is negative.

        """


class MessageDeliveryListener(ABC):  # pylint: disable=too-few-public-methods
    """Message delivery listener interface to process broker message delivery notifications (success/failure).
    """

    @abstractmethod
    def on_delivery_receipt(self, delivery_receipt: 'DeliveryReceipt'):
        """
        On delivery, send the delivery receipt.
        Args:
            Delivery_receipt (DeliveryReceipt): The object to indicate that delivery was done.

        """
