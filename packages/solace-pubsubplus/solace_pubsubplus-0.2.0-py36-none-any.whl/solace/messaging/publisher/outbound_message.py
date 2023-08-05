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
Module for outbound messages.

This module includes classes for an outbound message and the
interface definition for a builder for an outbound message.

 """

from abc import ABC, abstractmethod
from typing import TypeVar
from solace.messaging.config.property_based_configuration import PropertyBasedConfiguration
from solace.messaging.core._message import Message

T = TypeVar('T')  # pylint: disable=invalid-name


class OutboundMessageBuilder(PropertyBasedConfiguration):
    """
    .. _OutboundMessageBuilder:

    This builder is used for building outbound messages which are published as
    :py:class:`solace.messaging.publisher.message_publisher.MessagePublisher` objects.

    """

    T = TypeVar('T', bytearray, str, 'OutboundMessage')

    @abstractmethod
    def from_properties(self, configuration: dict) -> 'OutboundMessageBuilder':  # pragma: no cover
        """
        This method adds user properties to the message. User properties are carried in the message metadata as
         (``key``, ``value``) pairs.

        Args:
            configuration (dict): The configuration.

        Returns:
            OutboundMessageBuilder: A builder object representing an outbound message object for method chaining.

        """

    @abstractmethod
    def with_property(self, property_key: str, property_value: str) -> 'OutboundMessageBuilder':
        """
        Add user property with the given ``key`` and ``value``.

        Args:
            property_key (str): The key for the configuration.
            property_value (str): The value for the key.

        Returns:
            OutboundMessageBuilder: A builder object representing an outbound message object for method chaining.

        """

    @abstractmethod
    def with_expiration(self, timestamp: int) -> 'OutboundMessageBuilder':
        """
        Set message expiration time.

        Args:
            timestamp(int): The timestamp in milliseconds (Unix Epoch time), or None (to delete).


        Returns:
            OutboundMessageBuilder: A builder object representing an outbound message object for method chaining..
        """

    @abstractmethod
    def with_priority(self, priority: int) -> 'OutboundMessageBuilder':
        """
        Set the priority (0 to 9), where zero is the lowest priority.  If the priority is
        set to a value larger than 9, it's treated as a 9 (the highest priority possible).

        Args:
            priority(OutboundMessageBuilder.Priority): The priority of the outbound message.

        Returns:
            OutboundMessageBuilder: A builder object representing an outbound message object for method chaining.
        """

    @abstractmethod
    def with_application_message_type(self, application_message_type: str) -> 'OutboundMessageBuilder':
        """
        Set the application message type for a message using a string or None (to delete).

        The Application Message type is carried in the message meta data. It is used for application to
        application signaling.

        Args:
            application_message_type (str): The application message type.

        Returns:
            OutboundMessageBuilder: A builder object representing an outbound message object for method chaining.
        """

    @abstractmethod
    def with_sequence_number(self, sequence_number: int) -> 'OutboundMessageBuilder':
        """
        Set the sequence number for the message.

        The sequence number is carried in the message meta data.  It is used for application to
        application signaling.

        Args:
            sequence_number (int):  The expected integer value.

        Returns:
            OutboundMessageBuilder: A builder object representing an outbound message object for method chaining.
        """

    @abstractmethod
    def with_application_message_id(self, application_message_id: str) -> 'OutboundMessageBuilder':
        """
        Set the application message identifier for a message from a string or None (to delete it).

        The application message identifer is carried in the message metadata. It is used for application to
        application signaling.

        Args:
            application_message_id (str):  The application identifier.

        Returns:
            OutboundMessageBuilder: A builder object representing an outbound message object for method chaining.
        """

    @abstractmethod
    def with_http_content_header(self, content_type, content_encoding) -> 'OutboundMessageBuilder':
        """
        Set the HTTP content-type and HTTP content-encoding for a message.

        For interoperability with REST clients, it may be necessary to set the HTTP content-type
        and HTTP content-encoding parameters.

        Args:
            content_type (str):  The expected and valid HTTP content-type.
            content_encoding (str):  The expected and valid HTTP content-encoding

        Returns:
            OutboundMessageBuilder: A builder object representing an outbound message object for method chaining.
        """

    @abstractmethod
    def build(self, payload: T, additional_message_properties=None, converter=None) -> '_OutboundMessage':
        """
        Build a :py:class:`solace.messaging.publisher.outbound_message.OutboundMessage` instnace with the
        specified payload. The payload must be a ``bytearray`` or ``string``; if it is not, you must specify
        a``convertor`` that converts the object to a ``bytearray``.

        Args:
            payload (T): The payload to add to the message.
            additional_message_properties (dict): The additional message properties to add to the message metadata.
            converter(Any): The converter to convert the ``payload`` object to a ``bytearray``.

        Returns:
            OutboundMessage: A builder object representing an outbound message object.
        """


class OutboundMessage(Message, ABC):
    """
        Abstract class that defines the interface for Outbound message.

        An instance OutboundMessage can be created using a
        :py:class:`solace.messaging.publisher.outbound_message.OutboundMessageBuilder` instannce.
    """
