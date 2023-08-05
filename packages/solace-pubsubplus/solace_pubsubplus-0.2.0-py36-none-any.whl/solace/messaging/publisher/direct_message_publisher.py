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


"""
Module contains Direct Message Publisher.

A Direct Message Publisher must be created by
:py:class:`~solace.messaging.builder.direct_message_publisher_builder.DirectMessagePublisherBuilder`.The
DirectMessagePublisher instance is used to publish Direct Messages created by a
:py:class:`~solace.messaging.publisher.outbound_message.OutboundMessageBuilder`. Topic (destination)
may be added when the message is a published.

The direct message publisher may also be use to publish simple messages containing only a bytearray or string payload.
"""

from abc import abstractmethod, ABC
from typing import Union

from solace.messaging.publisher.message_publisher import MessagePublisher
from solace.messaging.publisher.outbound_message import OutboundMessage
from solace.messaging.resources.topic import Topic


class DirectMessagePublisher(MessagePublisher, ABC):
    """ A class that defines the interface to a publisher for direct (non-persisted) messages."""

    @abstractmethod
    def set_publish_failure_listener(self, listener: 'PublishFailureListener'):
        """
        Set the specified ``PublishFailureListener`` to listen for a provided instance of the publisher.

        A :py:class:`solace.messaging.publisher.direct_message_publisher.PublishFailureListener` is notified
        through it's defined callback whenever a publish message attempt fails asynchronously.

        Published messages can be queued for later transmission when the transport is flow-controlled.  If queued
        messages cannot be published, the ``PublishFailureListener`` - if one is registered - is notified. The PubSub+ event broker
        can also reject messages which appear as rejection notices on the  specified``PublishFailureListener``.

        Args:
            listener(PublishFailureListener): The specified listener for publisher failures.
        """

    @abstractmethod
    def publish(self, message: Union[bytearray, str, OutboundMessage], destination: Topic,
                additional_message_properties=None):
        """
        Send outbound messages to the specified ``destination`` using a provided
        :py:class:`solace.messaging.builder.outbound_message.OutboundMessageBuilder` instance.
        Alternatively, a ``bytearray`` or ``str`` payload can be passed
        to this method this API will creates a py:class:`solace.messaging.core.message.Message` instance to send.

        Args:
            message(bytearray, str, OutboundMessage): The outbound message that can be an Outbound object, bytearray, or str.
            destination(Topic): The destination to add to the message.
            additional_message_properties(dict) : The additional properties to customize a particular message. Each key can be customer provided,
                                                  or it can be a key from of type solace.messaging.config.solace_properties.message_properties.
        Raises:
            PubSubPlusClientError: When the message cannot be send and retry attempts did not help to resolve the problem.
            PublisherOverflowError: Raised when the publisher sends messages faster than what the current I/O capabilities
                                    allow for or when internal buffering capabilities have been exceeded.
        """


class PublishFailureListener(ABC):  # pylint: disable=too-few-public-methods
    """Interface definition for a listener for publish failures.
    """

    @abstractmethod
    def on_failed_publish(self, failed_publish_event: 'FailedPublishEvent'):
        """
        Callback method executed when publish errors occur asynchronously.

        Args:
            failed_publish_event(FailedPublishEvent): The publish event indicating a failure.
        """
