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


""" This module that contains the interface definition for the retry strategy.

The :py:class:`RetryStrategy` instance is configured in the ``MessagingService`` with
the :py:meth:`MessagingServiceClientBuilder.with_connection_retry_strategy()` method.
"""
import logging
from abc import ABC, abstractmethod

from solace.messaging.config.sol_constants import MAX_RETRY_INTERVAL_MS, \
    DEFAULT_RECONNECT_RETRY_INTERVAL_TIMER_MS
from solace.messaging.config.solace_message_constants import VALUE_CANNOT_BE_NEGATIVE, \
    VALUE_OUT_OF_RANGE
from solace.messaging.config.solace_properties import transport_layer_properties
from solace.messaging.errors.pubsubplus_client_error import IllegalArgumentError
from solace.messaging.utils.solace_utilities import Util

logger = logging.getLogger('solace.messaging')

__all__ = ["RetryStrategy"]


class RetryConfigurationProvider:
    """ This class contains methods to create ``TypedConfiguration`` objects and is used when
        you create :py:class:`RetryStrategy` instances. This is an implementation class, not for public use.
    """

    @staticmethod
    def to_reconnection_configuration(strategy: 'RetryStrategy') -> dict:
        """
        Creates reconnection behaviour configuration object from a given RetryStrategy.

        Args: strategy (RetryStrategy) : The retry strategy to use.

       Returns:
           dict: A configuration dictionary object that can be used to configure reconnection behavior on a PubSub+ event broker.
        """
        retry_configuration = dict()
        retry_configuration[transport_layer_properties.RECONNECTION_ATTEMPTS] = strategy.get_retries()
        retry_configuration[transport_layer_properties.RECONNECTION_ATTEMPTS_WAIT_INTERVAL] = \
            strategy.get_retry_interval()
        logger.debug('Reconnection configuration with retry strategy')
        return retry_configuration

    @staticmethod
    def to_connection_configuration(strategy: 'RetryStrategy') -> dict:
        """
           Creates connection behavior configuration object from a given ``RetryStrategy``.
           Args:
               strategy (RetryStrategy): The specified retry strategy.

           Returns:
                dict: A configuration dictionary object that can be used to configure reconnection behavior on a PubSub+ event broker.
           """
        retry_configuration = dict()
        retry_configuration[transport_layer_properties.CONNECTION_RETRIES] = strategy.get_retries()  # Re-visit prop
        retry_configuration[transport_layer_properties.CONNECTION_ATTEMPTS_TIMEOUT] = \
            strategy.get_retry_interval()
        logger.debug('Connection configuration with retry strategy')
        return retry_configuration


class RetryStrategy(ABC):
    """
     This is an abstract base class that provides static methods for generating specific retry strategies.
    """

    @abstractmethod
    def get_retries(self) -> int:  # pylint: disable=missing-function-docstring
        # this method will get the retries count
        # not a public interface
        ...  # pragma: no cover

    @abstractmethod
    def get_retry_interval(self) -> int:  # pylint: disable=missing-function-docstring
        # this method will get the retries interval
        # not a public interface
        ...  # pragma: no cover

    @staticmethod
    def forever_retry(retry_interval: int = None) -> 'RetryStrategy':
        """
        Creates an instance for automatic retries with a given retry interval.

        When created with forever_retry() the configuration will never terminate retry attempts.

        Args:
            retry_interval (int) : retry interval in milliseconds. The valid range for retry interval is 0 - 60000.
        
        Returns:
            RetryStrategy: An instance of the retry strategy to configure automatic retry without termination.
        """
        if retry_interval is None:
            logger.debug('Forever retry with retry strategy.')
            return _RetryStrategy(-1, DEFAULT_RECONNECT_RETRY_INTERVAL_TIMER_MS)
        Util.is_type_matches(retry_interval, int)
        if retry_interval < 0 or retry_interval > MAX_RETRY_INTERVAL_MS:
            logger.warning("%s [0-%d]", VALUE_OUT_OF_RANGE, MAX_RETRY_INTERVAL_MS)
            raise IllegalArgumentError(f"{VALUE_OUT_OF_RANGE} [0-{MAX_RETRY_INTERVAL_MS}]")
        logger.debug('Applied forever retry strategy. Retry interval: %d', retry_interval)
        return _RetryStrategy(-1, retry_interval)

    @staticmethod
    def never_retry() -> 'RetryStrategy':
        """
        Creates an instance for a retry strategy that has no retry attempts.

        When created with never_retry() the configuration will never retry a connection attempt or
        attempt a reconnection at all.

        Returns:
            RetryStrategy: A RetryStrategy instance to configure that no retries be made.
        """
        logger.debug('Never retry strategy applied.')
        return _RetryStrategy(0, DEFAULT_RECONNECT_RETRY_INTERVAL_TIMER_MS)

    @staticmethod
    def parametrized_retry(retries: int, retry_interval: int) -> 'RetryStrategy':
        """
        Creates an instance with retry properties defined by the parameters.

        Args:
            retries (int): The maximum number of retry attempts.
            retry_interval (int): The time (in milliseconds) to wait between retries.

        Returns:
            RetryStrategy: A RetryStrategy instance to configure the retry strategy.
        """
        Util.is_type_matches(retry_interval, int)
        Util.is_type_matches(retries, int)
        if retries < 0:
            logger.warning(VALUE_CANNOT_BE_NEGATIVE)
            raise IllegalArgumentError(VALUE_CANNOT_BE_NEGATIVE)
        if retries < 0 or retry_interval > MAX_RETRY_INTERVAL_MS:
            logger.warning("%s[0-%d]", VALUE_OUT_OF_RANGE, MAX_RETRY_INTERVAL_MS)
            raise IllegalArgumentError(f"{VALUE_OUT_OF_RANGE} [0-{MAX_RETRY_INTERVAL_MS}]")
        logger.debug('Parametrized retry strategy applied. Retries: [%d], Retry interval: [%d]',
                     retries, retry_interval)
        return _RetryStrategy(retries, retry_interval)


class _RetryStrategy(RetryStrategy):  # pylint: disable=missing-class-docstring
    def __init__(self, retries=None, retry_interval=None):
        logger.debug('[%s] initialized', type(self).__name__)
        self._retries: int = retries
        self._retry_interval: int = retry_interval

    def get_retries(self) -> int:
        """this method will get the retries count"""
        logger.debug('Get retry count')
        return self._retries

    def get_retry_interval(self) -> int:
        """this method will get the retry interval value"""
        logger.debug('Get retry interval')
        return self._retry_interval

    def __str__(self) -> str:
        """this method will convert to string TO"""
        logger.debug('Convert retry strategy to string')
        return f"retries : {self._retries} retryInterval : {self._retry_interval}"
