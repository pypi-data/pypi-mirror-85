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

"""Module contains the implementation class and methods for the MessagePublisherBuilder"""

import logging
import typing

from solace.messaging.builder.message_publisher_builder import MessagePublisherBuilder
from solace.messaging.config import sol_constants
from solace.messaging.config import solace_message_constants
from solace.messaging.config.publisher_back_pressure_configuration import PublisherBackPressure
from solace.messaging.config.solace_properties import publisher_properties
from solace.messaging.errors.pubsubplus_client_error import IllegalArgumentError

if typing.TYPE_CHECKING:
    from solace.messaging.messaging_service import MessagingService

logger = logging.getLogger('solace.messaging')


class _MessagePublisherBuilder(MessagePublisherBuilder)\
        :  # pylint: disable=missing-class-docstring, missing-module-docstring
    def __init__(self, messaging_service: 'MessagingService'):
        logger.debug('[%s] initialized', type(self).__name__)
        self._messaging_service: 'MessagingService' = messaging_service
        self._buffer_capacity: int = 0  # queue value either 0(infinite size) or +ve number
        self._publisher_back_pressure_type: PublisherBackPressure = PublisherBackPressure.No

    @property
    def messaging_service(self):
        """property to hold and return the messaging service instance"""
        return self._messaging_service

    @property
    def buffer_capacity(self):
        """property to hold and return the buffer capacity"""
        return self._buffer_capacity

    @property
    def publisher_back_pressure_type(self):
        """property to hold and return the publisher back pressure tye"""
        return self._publisher_back_pressure_type

    def from_properties(self, configuration: dict) -> 'MessagePublisherBuilder':
        """Enables dict  based configuration"""
        self.__build_back_pressure_from_props(configuration)
        return self

    def on_back_pressure_reject(self, buffer_capacity: int) -> 'MessagePublisherBuilder':
        """
        :py:class:`~solace.messaging.publisher.direct_message_publisher.DirectMessagePublisher` that are built will
        throw an :py:class:`~solace.messaging.errors.pubsubplus_client_exception.BackPressureError`
        when unable to publish message because the publisher buffer capacity is exceeded.  Messages are queued
        for transmit whenever the publisher exceeds the network transmit capacity, which is a function
        of network speed and network transit time.

        Args:
            buffer_capacity (int): an integer value which represents the maximum queue size in number of messages.

        Raises:
            IllegalArgumentError: if the provided buffer size is either zero or any negative number
        Returns:
            DirectMessagePublisherBuilder for method chaining.
        """
        if not isinstance(buffer_capacity, int):
            raise IllegalArgumentError(solace_message_constants.ILLEGAL_BUFFER_CAPACITY)
        if buffer_capacity <= 0:
            logger.warning("Buffer size::'%d' %s", buffer_capacity, solace_message_constants.VALUE_CANNOT_BE_NEGATIVE)
            raise IllegalArgumentError(
                f"Buffer size::'{buffer_capacity}' {solace_message_constants.VALUE_CANNOT_BE_NEGATIVE}")

        logger.debug('Enabled back pressure with reject mechanism, buffer/queue max capacity: %d', buffer_capacity)
        self._publisher_back_pressure_type = PublisherBackPressure.Reject
        self._buffer_capacity = buffer_capacity
        return self

    def on_back_pressure_elastic(self) -> 'MessagePublisherBuilder':
        """
        :py:class:`~solace.messaging.publisher.direct_message_publisher.DirectMessagePublisher` that are built will
        buffer all messages until memory is exhausted. Messages are queued for transmit whenever the publisher
        exceeds the network transmit capacity, which is a function of network speed and network transit time.

        Usage of this strategy can lead to out of memory situation and application could crash. This strategy
        may be useful for microservices which are running in a managed environment that can detect crashes and perform
        restarts of a microservices.
        Returns:
            DirectMessagePublisherBuilder for method chaining.
        """
        logger.debug('Enabled back pressure with elasticity mechanism, buffer/queue capacity: MAX')
        self._publisher_back_pressure_type = PublisherBackPressure.Elastic
        return self

    def on_back_pressure_wait(self, buffer_capacity: int) -> 'MessagePublisherBuilder':
        """
        :py:class:`~solace.messaging.publisher.direct_message_publisher.DirectMessagePublisher` that are built will
        wait when unable to publish message because the publisher buffer capacity is exceeded. Messages are queued
        for transmit whenever the publisher exceeds the network transmit capacity, which is a function of network
        speed and network transit time. Attempts to publish beyond specified bufferCapacity will pause a publisher
        thread

        Args:
            buffer_capacity (int):  max number of messages that can be buffered in between before publishing
            thread is put on hold
        Raises:
            IllegalArgumentError: if either the  provided buffer size
        Returns:
            DirectMessagePublisherBuilder for method chaining.
        """
        if not isinstance(buffer_capacity, int):
            raise IllegalArgumentError(solace_message_constants.ILLEGAL_BUFFER_CAPACITY)
        if buffer_capacity <= 0:
            logger.warning("Buffer size:'%d' %s", buffer_capacity, solace_message_constants.VALUE_CANNOT_BE_NEGATIVE)
            raise IllegalArgumentError(
                f"Buffer size:'{buffer_capacity}' {solace_message_constants.VALUE_CANNOT_BE_NEGATIVE}")
        self._publisher_back_pressure_type = PublisherBackPressure.Wait
        self._buffer_capacity = buffer_capacity
        return self

    def __build_back_pressure_from_props(self, configuration: dict):
        if publisher_properties.PUBLISHER_BACK_PRESSURE_STRATEGY in configuration.keys():
            if configuration[publisher_properties.PUBLISHER_BACK_PRESSURE_STRATEGY] \
                    == sol_constants.PUBLISHER_BACK_PRESSURE_STRATEGY_ELASTIC:
                self.on_back_pressure_elastic()
            elif configuration[publisher_properties.PUBLISHER_BACK_PRESSURE_STRATEGY] == \
                    sol_constants.PUBLISHER_BACK_PRESSURE_STRATEGY_BUFFER_REJECT_WHEN_FULL:
                self.__validate_buffer_capacity_key(configuration)
                self.on_back_pressure_reject(
                    buffer_capacity=configuration[publisher_properties.PUBLISHER_BACK_PRESSURE_BUFFER_CAPACITY])
            elif configuration[publisher_properties.PUBLISHER_BACK_PRESSURE_STRATEGY] == \
                    sol_constants.PUBLISHER_BACK_PRESSURE_STRATEGY_BUFFER_WAIT_WHEN_FULL:
                self.__validate_buffer_capacity_key(configuration)
                self.on_back_pressure_wait(
                    buffer_capacity=configuration[publisher_properties.PUBLISHER_BACK_PRESSURE_BUFFER_CAPACITY])

    @staticmethod
    def __validate_buffer_capacity_key(configuration: dict):
        if publisher_properties.PUBLISHER_BACK_PRESSURE_BUFFER_CAPACITY not in configuration.keys():
            raise IllegalArgumentError(solace_message_constants.MISSING_BUFFER_CAPACITY)
        if not isinstance(configuration[publisher_properties.PUBLISHER_BACK_PRESSURE_BUFFER_CAPACITY], int):
            raise IllegalArgumentError(solace_message_constants.ILLEGAL_BUFFER_CAPACITY)
