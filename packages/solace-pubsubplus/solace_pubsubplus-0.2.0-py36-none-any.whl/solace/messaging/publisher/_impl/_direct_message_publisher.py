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

"""Module contains the Implementation classes and methods for the DirectMessagePublisher"""
import logging
import time
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Union

from solace.messaging.config.sol_constants import SOLCLIENT_DELIVERY_MODE_DIRECT
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError
from solace.messaging.publisher._impl._message_publisher import _MessagePublisher
from solace.messaging.publisher.direct_message_publisher import DirectMessagePublisher
from solace.messaging.publisher.outbound_message import OutboundMessage
from solace.messaging.publisher.publishable import Publishable
from solace.messaging.resources.topic import Topic

logger = logging.getLogger('solace.messaging.publisher')


class _DirectMessagePublisher(_MessagePublisher, DirectMessagePublisher) \
        :  # pylint: disable=R0904, missing-function-docstring, too-many-instance-attributes, missing-class-docstring, too-many-ancestors
    # class for direct message publisher

    def __init__(self, direct_message_publisher: '_DirectMessagePublisherBuilder'):
        # """
        # Args:
        #     messaging_service (MessageService):
        #     publisher_back_pressure_type (PublisherBackPressure):
        #     buffer_capacity (int):
        #     buffer_time_out ():
        # """
        logger.debug('[%s] initialized', type(self).__name__)
        super().__init__(direct_message_publisher, SOLCLIENT_DELIVERY_MODE_DIRECT)
        self._error_notification_dispatcher: PublishFailureNotificationDispatcher = \
            PublishFailureNotificationDispatcher()

    def set_publish_failure_listener(self, listener: 'PublishFailureListener') -> None:
        logger.debug('SET: Direct Publish failure listener')
        self._error_notification_dispatcher.set_publish_failure_listener(listener)

    def publish(self, message: Union[bytearray, str, OutboundMessage], destination: Topic,
                additional_message_properties=None):
        super().message_publish(message, destination, additional_message_properties=additional_message_properties)


class FailedPublishEvent:
    """
    FailedPublishEvent carries the details of a failed attempt to publish.

    When the application registers a
    py:class:`~solace.messaging.publisher.direct_message_publisher.PublishFailureListener`. the listener
    will be informed of failures with a FailedPublishEvent containing:

    - Message: OutboundMessage that failed.
    - Destination: The topic of the message.
    - Exception:  The exception that occurred on publish
    - Timestamp:  The time of the failure.

    """

    def __init__(self, message: OutboundMessage, destination: str, exception: PubSubPlusClientError,
                 timestamp: int = None):
        self._message: OutboundMessage = message
        self._destination: str = destination
        self._exception: PubSubPlusClientError = exception
        self._timestamp: int = timestamp

    def get_message(self) -> OutboundMessage:
        """ Retrieves :py:class:`~solace.messaging.publisher.outbound_message.OutboundMessage` """
        return self._message

    def get_destination(self) -> str:
        """Retrieves message destination (topic) on the failed message"""
        return self._destination

    def get_timestamp(self) -> int:
        """Retrieves the timestamp of the event"""
        return self._timestamp

    def get_exception(self) -> PubSubPlusClientError:
        """Retrieves exception associated with a given event"""
        return self._exception

    def __str__(self):
        return f"message : {str(self._message)}  timestamp : {self._timestamp} exception : {self._exception}"


class ScheduledFailureNotification:  # pylint: disable=missing-class-docstring, missing-function-docstring
    # """class contains methods for scheduling an failure notification"""
    def __init__(self, exception: Exception, time_stamp: int, publishable: Publishable = None):
        self._exception = exception
        self._time_stamp = time_stamp
        self._publishable = publishable
        if self._publishable is None:
            self._publishable = Publishable.none()

    def call(self) -> None:
        # """this method schedules the notification by calling the on_failed_publish() """
        listener: 'PublishFailureListener' = \
            PublishFailureNotificationDispatcher.publish_failure_listener
        if listener is None:
            # the listener was removed/un-set , skip
            return
        listener.on_failed_publish(FailedPublishEvent(self._publishable.get_message(),
                                                      self._publishable.get_destination().get_name(),
                                                      self.map_exception(self._exception),
                                                      self._time_stamp))

    @staticmethod
    def map_exception(exception: Exception) -> PubSubPlusClientError:
        # """this method returns the exception map"""
        if isinstance(exception, PubSubPlusClientError):
            return exception
        return PubSubPlusClientError(exception)


class PublishFailureNotificationDispatcher:  # pylint: disable=missing-class-docstring, missing-function-docstring
    # """Dispatcher class for notifying the publish failures"""
    failure_notification_executor_service = ThreadPoolExecutor(max_workers=1)
    publish_failure_listener: 'PublishFailureListener' = None

    @staticmethod
    def on_exception(exception_occurred: Exception, publishable: Publishable = None,
                     time_stamp: int = int(time.time())):
        # """method to invoke the listener thread when publish mechanism fails
        #
        # Args:
        #     exception_occurred: occurred exception message
        #     publishable: Publishable object which contains the message and the destination name
        #     time_stamp: current time stamp in Epoch milliseconds.
        # """

        listener: 'PublishFailureListener' = PublishFailureNotificationDispatcher.publish_failure_listener

        if listener is None or exception_occurred is None:
            return

        if publishable is None:
            notification: 'ScheduledFailureNotification' = ScheduledFailureNotification(exception_occurred, time_stamp)
        else:
            notification: 'ScheduledFailureNotification' = ScheduledFailureNotification(exception_occurred, time_stamp,
                                                                                        publishable)

        try:
            PublishFailureNotificationDispatcher.failure_notification_executor_service.submit(notification.call)
        except PubSubPlusClientError as exception:
            logger.exception(exception)
            # if the thread fails to call the notification.call() we explicitly call it to
            # run on same thread when scheduler is full
            try:
                notification.call()
            except PubSubPlusClientError as exception:
                logger.exception(exception)

    @staticmethod
    def set_publish_failure_listener(publish_failure_listener: 'PublishFailureListener') -> None:
        # """method for setting the PublishFailureListener
        #
        # Args:
        #     publish_failure_listener: is of type PublishFailureListener
        # """
        PublishFailureNotificationDispatcher.publish_failure_listener = publish_failure_listener
