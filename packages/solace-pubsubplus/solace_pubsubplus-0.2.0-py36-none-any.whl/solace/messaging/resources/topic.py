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


"""Module contains the Abstract, API representation of a PubSub+ Broker Message Topic"""
import logging
from abc import ABC

from solace.messaging.config.solace_message_constants import TOPIC_NAME_CANNOT_BE_EMPTY
from solace.messaging.errors.pubsubplus_client_error import IllegalArgumentError
from solace.messaging.resources.named_resources import NamedResource

logger = logging.getLogger('solace.messaging.core')


class Topic(NamedResource, ABC):
    """
    An interface that abstracts a PubSub+ event broker resource that's used primarily for publishing messages.
    A topic acts as a destination that a MessagePublisher  can publish messages to.
    ``MessageReceivers`` add subscriptions that can be exactly a topic, or expressions that may match one
    or more topics.
    """

    @staticmethod
    def of(topic_string: str) -> 'Topic':  # pylint: disable=invalid-name
        """
        This is a factory method to take the topic in the form of a string
        and return the topic.

        Args:
            topic_string: The topic.
        Returns:
            Topic: An object representing the topic subscription.
        """
        if topic_string is None or len(topic_string) == 0:
            logger.warning(TOPIC_NAME_CANNOT_BE_EMPTY)
            raise IllegalArgumentError(TOPIC_NAME_CANNOT_BE_EMPTY)
        return _Topic(topic_string)


class _Topic(Topic):  # pylint: disable=missing-class-docstring
    # """class to implement Topic"""

    def __init__(self, expression):
        self._expression = expression

    def get_name(self) -> str:
        # """ returns the name """
        return self._expression

    def __str__(self):
        return f"topic : {self._expression} "
