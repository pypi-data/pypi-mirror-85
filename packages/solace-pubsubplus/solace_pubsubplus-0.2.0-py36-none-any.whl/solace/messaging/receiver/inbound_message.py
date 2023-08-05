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
This module defines the interface to an inbound message used to receive data from the PubSub+ broker.
"""
# pylint: disable=too-few-public-methods

from abc import ABC, abstractmethod
from typing import Union, TypeVar

from solace.messaging.core._message import Message
from solace.messaging.interoperability_support import InteroperabilitySupport
from solace.messaging.utils.converter import BytesToObject

T = TypeVar('T')  # pylint: disable=invalid-name


class InboundMessage(Message, InteroperabilitySupport):
    """
    Abstract class to define the interfaces to an inbound message.
    """

    @abstractmethod
    def get_and_convert_payload(self, converter: BytesToObject[T], output_type: type) -> type:
        """
        Retrieve the payload and converts it to the target object using given ``converter``.

        Args:
            converter(BytesToObject): An application provided converter to deserialize the payload to a Python object.
            output_type (type):  The Python Class returned by the BytesToObject type.

        Returns:
            type: An instance of the defined output_type.

        Raises:
            PubSubPlusClientError:  When the converter returns a non-matching object type.
        """

    @abstractmethod
    def get_application_message_type(self) -> Union[str, None]:
        """
        Retrieve the application message type.

        The application message type is carried in the message metadata. It is used for application to
        application signaling.  This value is used by applications only, and is received exactly as set by
        a publishing application.

        Returns:
            str: The application message type or None if not set.
        """

    @abstractmethod
    def get_destination_name(self) -> str:
        """
        Retrieve the destination which the message was received, which can be a topic or a queue.

        Returns:
            str: The destination name.

        """

    @abstractmethod
    def get_time_stamp(self) -> [int, None]:
        """
        Retrieve the timestamp (Unix epoch time) of the message when it arrived at the Client API.
        The time is in milliseconds.

        Returns:
            int: The timestamp (Unix Epoch time) or None if not set. The time is in milliseconds.
        """

    @abstractmethod
    def get_sender_timestamp(self) -> [int, None]:
        """
        Retrieve the sender's timestamp (Unix epoch time). This field can be set during message publishing.
        The time is in milliseconds.

        Returns:
            int: The timestamp (Unix Epoch time) or None if not set. The time is in milliseconds.
        """

    @abstractmethod
    def get_message_discard_notification(self) -> 'MessageDiscardNotification':
        """
        Retrieve the message discard notification about previously discarded messages.
        This is for non-durable consumers that use Direct Transport.

        Returns:
            MessageDiscardNotification: A value not expected to be None.
        """

    class MessageDiscardNotification(ABC):
        """
         An interface to Discard Notification Information.
        """

        @abstractmethod
        def has_broker_discard_indication(self) -> bool:
            """
            Retrieve the broker discard indication. A receiving client can use a message discard indication method or
            function to query whether the event broker has for any reason discarded any Direct messages previous to the
            current received message.

            When the PubSub+ event broker discards messages before sending them, the next message successfully sent to
            the receiver will have discard indication set.

            Returns:
                bool: True if PubSub+ event broker has discarded one or more messages prior to the current message.
            """
