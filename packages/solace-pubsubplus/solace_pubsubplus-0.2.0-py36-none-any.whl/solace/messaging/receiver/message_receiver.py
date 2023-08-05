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
Module that abstracts message receiving behavior; it is a base class for all receivers.
"""
from abc import ABC, abstractmethod
from enum import Enum

from solace.messaging.receiver.async_receiver_subscriptions import AsyncReceiverSubscriptions
from solace.messaging.receiver.inbound_message import InboundMessage
from solace.messaging.receiver.receiver_subscriptions import ReceiverSubscriptions
from solace.messaging.utils.life_cycle_control import LifecycleControl, AsyncLifecycleControl


class MessageReceiverState(Enum):  # pylint: disable=too-few-public-methods, missing-class-docstring
    # """enum class for holding the receiver state constants"""
    NOT_STARTED = 0
    STARTING = 1
    STARTED = 2
    TERMINATING = 3
    TERMINATED = 4


class MessageReceiver(LifecycleControl, AsyncLifecycleControl, ReceiverSubscriptions, AsyncReceiverSubscriptions, ABC):
    """An abstract class that provides the message receiver implementation. """

    @abstractmethod
    def receive_async(self, message_handler: 'MessageHandler'):
        """
        Register an asynchronous message receiver on the :py:class:`solace.messaging.receiver.persistent_message_receiver.PersistentMessageReceiver`
        instance.

        Args:
            message_handler(MessageHandler): The object that receives all inbound messages (InboundMessage) in its onMessage() callback.
                             If the provided value is None, then the asynchronous receiver is removed and
                             the receive_message() (solace.messaging.receiver.persistent_message_receiver.PersistentMessageReceiver).
                             can be used.
        """

    @abstractmethod
    def receive_message(self, timeout=None) -> InboundMessage:
        """
        Blocking request to receive the next message. You acknowledge the message using the
        :py:func:`solace.messaging.receiver.acknowledgement_support.AcknowledgementSupport.ack()` function.

        This method is usually used in loop an its use is mutually exclusive when
        used asynchronously.

        Args:
            timeout(int): The time, in milliseconds, to wait for a message to arrive.

        Returns:
            InboundMessage: An object that represents an inbound message.

        Raises:
            Queue:  An empty queue object if no messages arrive before timeout expires.
            PubSubPlusClientError: If error occurred while receiving or processing the message.
    """


class MessageHandler(ABC):  # pylint: disable=too-few-public-methods
    """
    An abstract base class that defines the interface for a  message handler for inbound messages.
    """

    @abstractmethod
    def on_message(self, message: InboundMessage):
        """
        Definition for a message processing function.

        Args:
            message(InboundMessage): The inbound message.
        """
