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
    Module to handle back pressure configuration in
    py:class:`solace.messaging.builder.message_publisher_builder.MessagePublisherBuilder`.
"""
from abc import ABC, abstractmethod
from enum import Enum

__all__ = ["PublisherBackPressureConfiguration"]


class PublisherBackPressure(Enum):  # pydoc: no  # pylint: disable=missing-class-docstring
    # """class which extends Enum to hold the publisher back pressure"""
    No = -1
    Reject = 0
    Elastic = 1
    Wait = 2


class PublisherBackPressureConfiguration(ABC):
    """
    A class that abstracts configuration of back-pressure features
    All methods in this class are mutually exclusive and therefore should be called only once.
    """

    @abstractmethod
    def on_back_pressure_reject(self, buffer_capacity: int):
        """
        Abstract method to be implemented in superclass.
        Configures the  publisher with capacity-bounded, buffered back-pressure; when the application keeps publishing,
        the publish method raises a :py:class:`solace.messaging.errors.pubsubplus_client_error.PublisherOverflowError`
        if the specified ``buffer_capacity`` is exceeded.
        Args:
            buffer_capacity int): The maximum number of messages to buffer before raising an exception.
        Raises:
            PubSubPlusClientError: When the maximum number of messages have been exceeded.
        """

    @abstractmethod
    def on_back_pressure_elastic(self):
        """
        Configures the publisher to buffer indefinitely, consuming as much memory as required for buffered messages.
        This abstract method is to be implemented in the superclass.

        Raises:
            PubSubPlusClientError: When unable to configure the publisher.
        """

    @abstractmethod
    def on_back_pressure_wait(self, buffer_capacity: int):
        """
        Configures the  publisher with capacity bounded buffered back-pressure. If the application application keeps publishing
        using the ``publish()`` method, it blocks and waits for room if the specified ``buffer_capacity`` has been exceeded.
        This abstract method is to be implemented in the superclass.

        Args:
            buffer_capacity (int): The maximum number of messages to buffer before raising an error.

        Raises:
            PubSubPlusClientError: When the specified buffer capacity has been exceeded.
        """
