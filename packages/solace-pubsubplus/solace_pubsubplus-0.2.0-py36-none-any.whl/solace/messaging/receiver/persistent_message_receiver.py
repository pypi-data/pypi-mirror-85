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
Module contains the abstract base class for a Persistent Message Receiver

A PersistentMessageReceiver can be instantiated to receive Persistent Messages from a PubSub+ broker.

"""
# pylint: disable=too-few-public-methods, too-many-ancestors
import logging

from solace.messaging.receiver.acknowledgement_support import AcknowledgementSupport
from solace.messaging.receiver.message_receiver import MessageReceiver
from solace.messaging.receiver.receiver_flow_control import ReceiverFlowControl

logger = logging.getLogger('solace.messaging.receiver')


class PersistentMessageReceiver(MessageReceiver, ReceiverFlowControl,
                                AcknowledgementSupport):
    """
    An abstract class that defines the interface to a persistent message receiver.

    Note:
        A caller of any of blocking message receiving methods , those without the *async* suffix such as the
        :py:meth:`solace.messaging.receiver.message_receiver.MessageReceiver.receive_message()` method.
        will receive a new message for each call.

    WARNING:
        When you use this class, these are some considerations to aware of:
            - Concurrent use of asynchronous and synchronous message receiving methods on a single instance of
              receiver can have some unintended side effects and should be avoided.
            - Asynchronous methods should NOT be called multiple times or in combination with blocking message
              receiving function on the same :py:class:`solace.messaging.receiver.message_receiver.MessageReceiver` instance
              to avoid any unintended side effects.

    """
