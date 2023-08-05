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

"""Module contains the implementation class and methods for the MessagePublisher"""
# pylint: disable=missing-function-docstring, too-many-branches

import concurrent
import datetime
import enum
import logging
import queue
import threading
import typing
from concurrent.futures.thread import ThreadPoolExecutor
from typing import Union

from solace.messaging.config.publisher_back_pressure_configuration import PublisherBackPressure
from solace.messaging.config.sol_constants import SOLCLIENT_WOULD_BLOCK, SOLCLIENT_OK, \
    SOLCLIENT_DELIVERY_MODE_PERSISTENT, SOLCLIENT_DELIVERY_MODE_DIRECT, GRACE_PERIOD_MIN_MS, GRACE_PERIOD_MAX_MS
from solace.messaging.config.solace_message_constants import PUBLISHER_NOT_STARTED, PUBLISHER_TERMINATED, \
    WOULD_BLOCK_EXCEPTION_MESSAGE, PUBLISH_FAILED_MESSAGING_SERVICE_NOT_CONNECTED, \
    PUBLISHER_CANNOT_BE_STARTED_EXCEPTION_MESSAGE, QUEUE_FULL_EXCEPTION_MESSAGE, PUBLISHER_NOT_READY, \
    UNCLEANED_TERMINATION_EXCEPTION_MESSAGE, PUBLISHER_TERMINATING, PUBLISHER_READINESS_SERVICE_DOWN_EXIT_MESSAGE, \
    PUBLISHER_SERVICE_DOWN_EXIT_MESSAGE
from solace.messaging.core import _solace_session
from solace.messaging.core._publish import _SolacePublish
from solace.messaging.errors.pubsubplus_client_error import IllegalStateError, PublisherOverflowError, \
    InvalidDataTypeError, PubSubPlusClientError, IllegalArgumentError, IncompleteMessageDeliveryError
from solace.messaging.publisher._impl import _direct_message_publisher
from solace.messaging.publisher._impl._outbound_message import _OutboundMessageBuilder, _OutboundMessage
from solace.messaging.publisher.message_publisher import MessagePublisher
from solace.messaging.publisher.outbound_message import OutboundMessage
from solace.messaging.publisher.outbound_message_utility import add_message_properties, set_correlation_tag_ptr
from solace.messaging.publisher.publishable import Publishable
from solace.messaging.publisher.publisher_health_check import PublisherReadinessListener
from solace.messaging.resources.topic import Topic
from solace.messaging.utils.solace_utilities import Util

if typing.TYPE_CHECKING:
    from solace.messaging.messaging_service import MessagingService
logger = logging.getLogger('solace.messaging.publisher')


class PublisherReadinessListenerThread(threading.Thread) \
        :  # pylint: disable=too-few-public-methods, missing-class-docstring, missing-function-docstring
    # """ Thread to let the callback know about readiness of direct message publisher when is actually ready. """

    def __init__(self, message_publisher: 'MessagePublisher', messaging_service: 'MessagingService', *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug('THREAD: [%s] initialized', type(self).__name__)
        self._message_publisher: 'MessagePublisher' = message_publisher
        self._publisher_readiness_listener = message_publisher.listener
        self._stop_listening_event = message_publisher.publisher_readiness_listener_thread_stop_event
        self._messaging_service: 'MessagingService' = messaging_service

    def run(self):
        # """ Start running thread
        # to INVOKE callback is being SET in SET_PUBLISHER_READINESS_LISTENER.
        # WOULD_BLOCK event should have occurred in API while direct PUBLISHing message AND
        # at the same time API will emit CAN_SEND_RECEIVED AND IS_READY method should return TRUE,
        # meanwhile notification SHOULDN'T BE SENT already
        # """
        logger.debug('THREAD: [%s] started', type(self).__name__)
        while not self._stop_listening_event.is_set():
            if self._messaging_service.api.message_service_state == _solace_session.MessagingServiceState.DOWN:
                # call the publisher's terminate method to ensure proper cleanup of thread
                logger.warning(PUBLISHER_READINESS_SERVICE_DOWN_EXIT_MESSAGE)
                break
            while not self._messaging_service.api.can_send_received.is_set():
                logger.debug('THREAD: [%s] is waiting for CAN_SEND event', type(self).__name__)
                self._messaging_service.api.can_send_received.wait()

            if self._message_publisher.is_ready() and \
                    not self._message_publisher.is_publisher_readiness_listener_notification_sent:
                logger.debug('IS_READY: True. Invoking [%s]', type(self).__name__)
                self._publisher_readiness_listener.ready()
                self._message_publisher.is_publisher_readiness_listener_notification_sent = True
                self._message_publisher.would_block_received.clear()


class MessagePublisherThread(threading.Thread):  # pylint: disable=missing-class-docstring, too-many-instance-attributes
    # """message publisher thread"""

    def __init__(self, message_publisher, messaging_service, asked_to_terminate, *args, **kwargs):

        super().__init__(*args, **kwargs)
        logger.debug('THREAD: [%s] initialized', type(self).__name__)
        self._message_publisher = message_publisher
        self._publisher_buffer_queue = message_publisher.message_publisher_buffer_queue
        self._publisher_thread_stop_event = message_publisher.publisher_thread_stop_event
        self._publisher_thread_can_peek_buffer_event = message_publisher.can_peek_buffer_event
        self._retry_count = 0
        self._messaging_service = messaging_service
        self._asked_to_terminate = asked_to_terminate
        self._publisher_empty = message_publisher.publisher_empty

    def run(self):  # pylint: disable= missing-function-docstring
        # """ Start running thread when
        # Publisher buffer/queue should not be empty and WOULD_BLOCK SESSION event not happened,
        # if WOULD_BLOCK received, ensure it receives CAN_SEND SESSION event received"""
        logger.debug('THREAD: [%s] started', type(self).__name__)
        while not self._publisher_thread_stop_event.is_set():
            if self._messaging_service.api.message_service_state == _solace_session.MessagingServiceState.DOWN:
                # notify about the publish failure only in direct mode
                if self._message_publisher.delivery_mode == SOLCLIENT_DELIVERY_MODE_DIRECT:
                    while True:
                        try:
                            element: tuple = self._publisher_buffer_queue.get_nowait()
                            self._message_publisher.notify_publish_error(
                                PubSubPlusClientError("Service Down"),
                                _OutboundMessage(element[1].get_message()),
                                element[1].get_destination())
                        except queue.Empty:
                            break
                if self._message_publisher.message_publisher_state == MessagePublisherState.TERMINATING:
                    self._publisher_empty.set()  # wakeup main thread when the service is down while terminating
                # call the publisher's terminate method to ensure proper cleanup of thread
                logger.warning(PUBLISHER_SERVICE_DOWN_EXIT_MESSAGE)
                break
            else:
                if self._message_publisher.message_publisher_state != MessagePublisherState.TERMINATING and \
                        not self._publisher_thread_can_peek_buffer_event.is_set() and \
                        self._publisher_buffer_queue.qsize() == 0:
                    self._publisher_thread_can_peek_buffer_event.wait()
                # don't attempt to publish  when we are  terminating
                if (not self._message_publisher.would_block_received.is_set()
                    and self._publisher_buffer_queue.qsize() > 0) \
                        or (self._message_publisher.would_block_received.is_set()
                            and self._messaging_service.api.can_send_received.is_set()
                            and self._publisher_buffer_queue.qsize() > 0) and not self._publisher_empty.is_set():
                    message_publisher, publishable = self._publisher_buffer_queue.queue[0]
                    self._publish(message_publisher, publishable)

                elif self._message_publisher.would_block_received.is_set() and \
                        not self._messaging_service.api.can_send_received.is_set():
                    logger.debug('THREAD: [%s] is waiting for CAN_SEND event', type(self).__name__)
                    self._messaging_service.api.can_send_received.wait()
                if self._publisher_buffer_queue.qsize() == 0 and not self._asked_to_terminate and \
                        self._message_publisher.message_publisher_state != MessagePublisherState.TERMINATING:
                    # let the thread wait for can_peek event
                    self._publisher_thread_can_peek_buffer_event.clear()
                # signaling that message publisher buffer is empty and can proceed to cleanup
                if self._message_publisher.message_publisher_state == MessagePublisherState.TERMINATING and \
                        self._publisher_buffer_queue.qsize() == 0 and not self._publisher_empty.is_set():
                    self._publisher_empty.set()

    def stop(self):  # pylint: disable=missing-function-docstring
        # """ this method is to stop the receiver """
        logger.debug('STOPPING THREAD: [%s]', type(self).__name__)
        self._publisher_thread_stop_event.set()

    def _publish(self, message_publisher: 'MessagePublisher', publishable: 'TopicPublishable'):
        try:
            status_code = message_publisher.do_publish(publishable)
            if status_code == SOLCLIENT_OK:
                self._publisher_buffer_queue.get_nowait()
            elif status_code == SOLCLIENT_WOULD_BLOCK:
                self._retry_count += 1
        except PubSubPlusClientError as exception:  # pragma: no cover
            logger.error('%s', str(exception))


class MessagePublisherState(enum.Enum):  # pylint: disable=too-few-public-methods,missing-class-docstring
    # """enum class for defining the  message publisher state"""
    NOT_STARTED = 0
    STARTED = 1
    TERMINATING = 2
    TERMINATED = 3
    NOT_READY = 4
    READY = 5


class _MessagePublisher(MessagePublisher) \
        :  # pylint: disable=R0904, missing-function-docstring, too-many-instance-attributes, missing-class-docstring

    # class for message publisher

    def __init__(self, message_publisher: Union['DirectMessagePublisher', '_PersistentMessagePublisher'],
                 delivery_mode: str):  # ToDo type hinting will be fixed later
        # """
        # Args:
        #     messaging_service (MessageService):
        #     delivery_mode
        # """
        logger.debug('[%s] initialized', type(self).__name__)
        self._messaging_service = message_publisher.messaging_service
        self._delivery_mode = delivery_mode
        self._publisher_back_pressure_type = message_publisher.publisher_back_pressure_type
        self._message_publisher_buffer_queue = None
        if self._publisher_back_pressure_type != PublisherBackPressure.No:
            self._message_publisher_buffer_queue = queue.Queue(maxsize=message_publisher.buffer_capacity)
        self._publisher_readiness_listener_thread = None
        self._listener = None
        self._message_publisher_thread = None
        self._message_publisher_state = MessagePublisherState.NOT_STARTED
        self._is_notified = False
        self._would_block_received = threading.Event()
        self._publishable = None
        self._publisher_thread_stop_event = threading.Event()
        self._outbound_message_builder = _OutboundMessageBuilder()
        self._publisher_readiness_listener_thread_stop_event = threading.Event()
        self._can_peek_buffer_event = threading.Event()
        self._can_peek_id = "can_peek_" + str(hex(id(self)))
        setattr(self._messaging_service.api,
                self._can_peek_id, self._can_peek_buffer_event)
        self._messaging_service.api.can_peek.append(self._can_peek_id)
        self._asked_to_terminate = False
        self._message = None
        self._publisher_empty = threading.Event()  # to signal publisher
        # buffer is empty in terminating state
        self._delivery_receipt_empty = threading.Event()  # to signal delivery receipt listener
        # buffer is empty in terminating state
        self._delivery_listener = None
        self._error_notification_dispatcher: _direct_message_publisher.PublishFailureNotificationDispatcher = \
            _direct_message_publisher.PublishFailureNotificationDispatcher()

    @property
    def delivery_mode(self):
        return self._delivery_mode

    @property
    def publisher_empty(self):
        return self._publisher_empty

    @property
    def publisher_thread_stop_event(self):
        """property to hold and return the publisher thread stop event"""
        return self._publisher_thread_stop_event

    @property
    def publisher_readiness_listener_thread_stop_event(self):
        """property to hold and return the publisher readiness listener thread stop event"""
        return self._publisher_readiness_listener_thread_stop_event

    @property
    def can_peek_buffer_event(self):
        """property to hold and return the can peek into buffer event"""
        return self._can_peek_buffer_event

    def is_ready(self) -> bool:
        # """
        # Non-blocking check if publisher can potentially publish messages.
        # Returns:
        #     bool: False if MessagePublisher is not STARTED or
        #     MessagePublisher is NOT_READY[WOULD_BLOCK occurred AND CAN_SEND_RECEIVED not SET],
        #     else True and set MessagePublisherState to READY
        #
        # """
        if self._message_publisher_state == MessagePublisherState.TERMINATED \
                or self._message_publisher_state == MessagePublisherState.TERMINATING:
            logger.debug('[%s] is [%s]. State: [%s]',
                         type(self).__name__, MessagePublisherState.NOT_READY.name,
                         self._message_publisher_state.name)
            return False

        # When we have buffer availability when backPressure is ON, then MessagePublisher is READY
        if self._message_publisher_buffer_queue is not None and not self._message_publisher_buffer_queue.full():
            self._message_publisher_state = MessagePublisherState.READY
            logger.debug('[%s] is [%s]. MessagePublisher buffer/queue is not full',
                         type(self).__name__, MessagePublisherState.READY.name)
            return True

        # if this is MessagePublisher NOT_READY, WOULD_BLOCK should have occurred,
        # so check if CAN_SEND_RECEIVED event is SET
        if self._message_publisher_state == MessagePublisherState.NOT_READY and \
                self.would_block_received.is_set() and self._messaging_service.api.can_send_received.is_set():
            # WOULD_BLOCK should have occurred, at the same time CAN_SEND_RECEIVED event should be SET,
            # to decide MessagePublisher is READY
            self._message_publisher_state = MessagePublisherState.READY
            logger.debug('[%s] is [%s]. CAN_SEND received', type(self).__name__, MessagePublisherState.READY.name)
            return True

        # either MessagePublisher should be STARTED or READY and WOULD_BLOCK event should not have occurred
        if (self._message_publisher_state == MessagePublisherState.STARTED or
            self._message_publisher_state == MessagePublisherState.READY) and not \
                self.would_block_received.is_set():
            self._message_publisher_state = MessagePublisherState.READY
            logger.debug('[%s] is [%s/%s]', type(self).__name__, MessagePublisherState.READY.name,
                         MessagePublisherState.STARTED.name)
            return True

        logger.debug('[%s] status: [%s]. is CAN_SEND SET?: %s',
                     type(self).__name__, self._message_publisher_state,
                     self._messaging_service.api.can_send_received.is_set())
        return False

    def set_publisher_readiness_listener(self, listener: PublisherReadinessListener) -> 'MessagePublisher':
        # """
        # Sets a publisher state listener
        # Args:
        #     listener: listener to observe publisher state
        # Returns:
        #
        # """
        Util.is_type_matches(listener, PublisherReadinessListener)
        if self._listener is None:
            self._listener = listener
            logger.debug('\nNOTIFICATION SCHEDULED')
            self._publisher_readiness_listener_thread = PublisherReadinessListenerThread(self, self._messaging_service)
            self._publisher_readiness_listener_thread.daemon = True
            self._publisher_readiness_listener_thread.start()
            self.is_publisher_readiness_listener_notification_sent = False

        return self

    def notify_when_ready(self):
        #  """
        # Non-blocking request to notify PublisherReadinessListener.
        # This method helps to overcome race condition between completion of the exception
        # processing on publishing of 'ready' aka can send event
        # Returns:
        #     None : returns none
        #  """
        if self._listener is None:
            logger.warning("%s is not set", PublisherReadinessListener)
            raise PubSubPlusClientError(message=f"{PublisherReadinessListener} is not set")
        if self.is_publisher_readiness_listener_notification_sent:
            logger.debug('NOTIFICATION SCHEDULED')
        self.is_publisher_readiness_listener_notification_sent = False

    def start(self):
        self._is_message_service_connected()
        self._message_publisher_state = MessagePublisherState.STARTED
        logger.debug('[%s] is %s. Publisher back-pressure Type: %s', type(self).__name__,
                     MessagePublisherState.STARTED.name, self._publisher_back_pressure_type)

    def start_async(self) -> concurrent.futures.Future:
        # """
        # method to check  message service connection status asynchronously, and set state to STARTED if connected
        # Raises:
        #     IllegalStateError: if message_service not connected
        # """
        with ThreadPoolExecutor(max_workers=1) as executor:
            return executor.submit(self.start)

    def notify_publish_error(self, exception, message, destination):
        # """this method triggers the PublishFailureNotificationDispatcher's on exception method
        #  Args:
        #      exception: exception message stack trace
        #      message: published message
        #      destination: destination topic
        #  """
        publishable = Publishable.of(message, destination)
        self._error_notification_dispatcher.on_exception(exception_occurred=exception, publishable=publishable)

    def do_publish(self, publishable: 'TopicPublishable'):  # pylint: disable=missing-function-docstring
        # """
        # method to call underlying CORE publish method
        # Args:
        #     publishable (TopicPublishable): TopicPublishable instance contains OutboundMessage & Topic
        # Returns:
        #     publish status code
        # """
        try:
            publish_status = _SolacePublish(self._messaging_service).publish(publishable.get_message(),
                                                                             publishable.get_destination())
            if self._delivery_mode == SOLCLIENT_DELIVERY_MODE_PERSISTENT and publish_status == SOLCLIENT_WOULD_BLOCK \
                    and self._publisher_back_pressure_type == PublisherBackPressure.No:
                raise PublisherOverflowError(WOULD_BLOCK_EXCEPTION_MESSAGE)

            if publish_status == SOLCLIENT_WOULD_BLOCK and \
                    self._publisher_back_pressure_type != PublisherBackPressure.No:
                self._process_would_block_status()
            return publish_status
        except (PubSubPlusClientError, PublisherOverflowError) as exception:
            if self._publisher_back_pressure_type != PublisherBackPressure.No and \
                    self._delivery_mode == SOLCLIENT_DELIVERY_MODE_DIRECT:
                self.notify_publish_error(exception, publishable.get_message(), publishable.get_destination())
            else:
                if not self._messaging_service.is_connected:
                    logger.warning(PUBLISH_FAILED_MESSAGING_SERVICE_NOT_CONNECTED)
                    raise IllegalStateError(PUBLISH_FAILED_MESSAGING_SERVICE_NOT_CONNECTED) from exception
                logger.warning(exception)  # pragma: no cover
                raise exception  # pragma: no cover

    def message_publish(self, message: Union[bytearray, str, OutboundMessage], destination: Topic,
                        additional_message_properties=None, correlation_tag=None):  # pylint: disable=too-many-branches
        # """
        #     Sends message to the given destination(Topic)
        # Args:
        #         destination: Topic endpoint
        #         message: message payload
        #         additional_message_properties :
        #         correlation_tag
        # Raises:
        #     IllegalStateError: When publisher is NOT_STARTED/TERMINATED/NOT_READY
        #     PublisherOverflowError: When buffer queue is full
        #     SolaceWouldBlockException: When publisher receive WOULD_BLOCK
        #     PubSubPlusClientError: When unable to send message
        # """
        if not self.is_ready():
            if self._message_publisher_state == MessagePublisherState.NOT_STARTED:
                logger.warning(PUBLISHER_NOT_STARTED)
                raise IllegalStateError(PUBLISHER_NOT_STARTED)
            elif self._message_publisher_state == MessagePublisherState.TERMINATED:
                logger.warning(PUBLISHER_TERMINATED)
                raise IllegalStateError(PUBLISHER_TERMINATED)
            elif self._message_publisher_state == MessagePublisherState.TERMINATING:
                logger.warning(PUBLISHER_TERMINATING)
                raise IllegalStateError(PUBLISHER_TERMINATING)
            elif self._message_publisher_state == MessagePublisherState.NOT_READY:
                logger.warning(PUBLISHER_NOT_READY)
                raise PublisherOverflowError(PUBLISHER_NOT_READY)

        logger.debug('[%s] enabled', self._publisher_back_pressure_type)
        if not isinstance(message, (OutboundMessage, str, bytearray)):
            raise InvalidDataTypeError(f"{type(message)} is unsupported at the "
                                       f"moment to publish a message")

        # convert bytearray & string type messages to OutboundMessage
        if not isinstance(message, OutboundMessage):
            self._message = self._outbound_message_builder.build(message)
        else:
            self._message = message
        if additional_message_properties:
            add_message_properties(additional_message_properties, self._message.solace_message)
        if correlation_tag:
            set_correlation_tag_ptr(self._message.solace_message.msg_p, correlation_tag)

        self._message.solace_message.set_delivery_mode(self._delivery_mode)
        self._publishable = Publishable.of(self._message.solace_message, destination)
        if correlation_tag:
            if correlation_tag.startswith(b'publish_await'):  # inform  the broker to send ack ASAP
                # when its comes to  messages published via publish await acknowledgement method
                self._publishable.get_message().set_ack_immediately(True)
        if self._publisher_back_pressure_type != PublisherBackPressure.No:
            self._start_message_publisher_thread()
            self._handle_back_pressure(self._publishable)
        else:
            self.do_publish(self._publishable)

    def _cleanup(self):
        self._message_publisher_state = MessagePublisherState.TERMINATED
        self._stop_publisher_thread()
        self._stop_publisher_readiness_listener_thread()
        logger.info(PUBLISHER_TERMINATED)

    def terminate_now(self):
        self._message_publisher_state = MessagePublisherState.TERMINATING
        self._cleanup()
        if self._message_publisher_buffer_queue is not None and self._message_publisher_buffer_queue.qsize() != 0:
            message = f'{UNCLEANED_TERMINATION_EXCEPTION_MESSAGE}. ' \
                      f'Failed message count: [{self._message_publisher_buffer_queue.qsize()}]'
            logger.warning(message)
            raise IncompleteMessageDeliveryError(message)

    def terminate(self, grace_period: int = GRACE_PERIOD_MAX_MS):
        if grace_period < GRACE_PERIOD_MIN_MS:
            raise IllegalArgumentError(f"grace_period must be >= {GRACE_PERIOD_MIN_MS}")
        grace_period_in_seconds = grace_period / 1000
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=grace_period_in_seconds)
        self._message_publisher_state = MessagePublisherState.TERMINATING
        self._can_peek_buffer_event.set()  # wake up thread
        if self._message_publisher_thread:  # wait for the grace period only
            # for back pressure scenario
            self._publisher_empty.wait(timeout=grace_period_in_seconds)  # first we are waiting for publisher
            # buffer to drain empty
            remaining_time = (end_time - datetime.datetime.now()).total_seconds()
            remaining_time = 0 if 0 > remaining_time else remaining_time
        if self._delivery_listener:  # now we are waiting for ack buffer to drain empty with whatever
            # time remaining of grace_period if we have publisher
            # thread else whole grace period we will wait for delivery listener thread,
            timeout = remaining_time if self._message_publisher_thread else grace_period_in_seconds
            self._delivery_receipt_empty.wait(timeout=timeout)
        self.terminate_now()

    def terminate_async(self, grace_period: int = GRACE_PERIOD_MAX_MS) -> concurrent.futures.Future:
        # """method for terminating the publisher in non blocking mode"""
        if grace_period < GRACE_PERIOD_MIN_MS:
            raise IllegalArgumentError(f"grace_period must be >= {GRACE_PERIOD_MIN_MS}")
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(self.terminate, grace_period)
        return future

    def is_running(self) -> bool:
        # """
        # method to validate publisher state is running
        # Returns:
        #     bool: True, if message publisher state is running else False
        # """
        is_running = self._message_publisher_state in [MessagePublisherState.STARTED,
                                                       MessagePublisherState.READY]
        logger.debug('[%s] is running?: %s', type(self).__name__, is_running)
        return is_running

    def is_terminated(self) -> bool:
        # """
        # method to validate publisher state is terminated
        # Returns:
        #     bool: True, if message publisher state is terminated else False
        # """
        is_terminated = self._message_publisher_state == MessagePublisherState.TERMINATED
        logger.debug('[%s] is terminated?: %s', type(self).__name__, is_terminated)
        return is_terminated

    def is_terminating(self) -> bool:
        # """
        # method to validate publisher state is terminating
        # Returns:
        #     bool: True, if message publisher state is terminating else False
        # """
        is_terminating = self._message_publisher_state == MessagePublisherState.TERMINATING
        logger.info('[%s] is terminating?: %s', type(self).__name__, is_terminating)
        return is_terminating

    def publisher_thread(self):  # pylint: disable=missing-function-docstring
        # """method for returning the publisher thread instance"""
        return self._message_publisher_thread

    def publisher_readiness_thread(self):  # pylint: disable=missing-function-docstring
        # """method for returning the publisher readiness thread instance"""
        return self._publisher_readiness_listener_thread

    def publisher_buffer_queue(self):  # pylint: disable=missing-function-docstring
        # """method for returning the publisher buffer queue"""
        return self._message_publisher_buffer_queue

    def is_publisher_buffer_queue_full(self) -> bool:  # pylint: disable=missing-function-docstring
        # """
        # method to validate publisher_buffer_queue is full
        # Returns:
        #     bool: True if buffer full else False
        # """
        is_buffer_full = self._message_publisher_buffer_queue.full()
        logger.debug('Is %s buffer/queue FULL? %s', type(self).__name__, is_buffer_full)
        return is_buffer_full

    @property
    def message_publisher_buffer_queue(self):  # pylint: disable=missing-function-docstring
        # """returns the publisher buffer queue"""
        return self._message_publisher_buffer_queue

    @property
    def listener(self):  # pylint: disable=missing-function-docstring
        # """returns the listener instance"""
        return self._listener

    @property
    def would_block_received(self):  # pylint: disable=missing-function-docstring
        # """returns the flag if the would block is being received"""
        if self._would_block_received.is_set():
            logger.debug('Is WOULD_BLOCK received?: %s', self._would_block_received.is_set())
        return self._would_block_received

    @would_block_received.setter
    def would_block_received(self, status: bool):  # pylint: disable=missing-function-docstring
        # """setter for would block, if occurs"""
        logger.debug('Set WOULD_BLOCK received status: %s', status)
        self._would_block_received = status

    @property
    def is_publisher_readiness_listener_notification_sent(self):  # pylint: disable=missing-function-docstring
        # """get publisher readiness listener notification sent status"""
        logger.debug('Is publisher readiness notified? %s', self._is_notified)
        return self._is_notified

    @is_publisher_readiness_listener_notification_sent.setter
    def is_publisher_readiness_listener_notification_sent(self, sent_status: bool):
        # """set publisher readiness listener notification sent status"""
        logger.debug('Set publisher readiness notification sent status: %s', self._is_notified)
        self._is_notified = sent_status

    @property
    def message_publisher_state(self):
        return self._message_publisher_state

    def _start_message_publisher_thread(self):
        # """method to starting the message publisher thread"""
        if self._message_publisher_thread is None:
            self._message_publisher_thread = MessagePublisherThread(self, self._messaging_service,
                                                                    self._asked_to_terminate
                                                                    )
            self._message_publisher_thread.daemon = False
            self._message_publisher_thread.start()

    def _handle_back_pressure(self, publishable: 'TopicPublishable'):
        # """
        # method for handling the back pressure
        # Args:
        #   publishable(TopicPublishable) : publishable object
        # Raises:
        #     SolaceWouldBlockException: if WOULD-BLOCK received
        #     PublisherOverflowError: if buffer FULL
        # """
        try:
            logger.debug('Enqueue message to buffer/queue')
            self.can_peek_buffer_event.set()  # let the publisher thread peek the buffer
            if self._publisher_back_pressure_type == PublisherBackPressure.Reject:
                self._message_publisher_buffer_queue.put((self, publishable), block=False)
            else:
                self._message_publisher_buffer_queue.put((self, publishable))
        except queue.Full:
            self._handle_queue_full()

    def _is_message_service_connected(self):
        # """
        # method to check message_service connected or not
        # Returns:
        #     True if connected
        # Raises:
        #     IllegalStateError: if message_service not connected
        # """
        if not self._messaging_service.is_connected:
            logger.warning(PUBLISHER_CANNOT_BE_STARTED_EXCEPTION_MESSAGE)
            raise IllegalStateError(PUBLISHER_CANNOT_BE_STARTED_EXCEPTION_MESSAGE)
        return True

    def _process_would_block_status(self):
        # """
        # Method to update message publisher state if WOULD_BLOCK received.
        # Reset can_send_received EVENT and SET would_block_received event
        # """
        if self._publisher_back_pressure_type == PublisherBackPressure.No:
            logger.info('WOULD_BLOCK received. MessagingService status: %s',
                        self._messaging_service.api.message_service_state)
        else:
            logger.info('WOULD_BLOCK received. Queue Size: %d. MessagingService status: %s',
                        self._message_publisher_buffer_queue.qsize(),
                        self._messaging_service.api.message_service_state)

        self._messaging_service.api.can_send_received.clear()  # the moment we get WOULD_BLOCK, reset this
        self.would_block_received.set()  # the moment we get WOULD_BLOCK, SET this event, to know WOULD_BLOCK occurred
        if self._publisher_back_pressure_type == PublisherBackPressure.No:
            self._message_publisher_state = MessagePublisherState.NOT_READY
            logger.warning(WOULD_BLOCK_EXCEPTION_MESSAGE)
            raise PublisherOverflowError(WOULD_BLOCK_EXCEPTION_MESSAGE)
        if self.is_publisher_buffer_queue_full():
            self._message_publisher_state = MessagePublisherState.NOT_READY

    def _handle_queue_full(self):  # this method will raise an exception if the queue is full
        current_size = self._message_publisher_buffer_queue.qsize()
        raise PublisherOverflowError(f'{QUEUE_FULL_EXCEPTION_MESSAGE} Size: {current_size}')

    def _stop_publisher_thread(self):
        # """ this method is to stop publisher thread """
        if self._message_publisher_thread is not None:
            self._asked_to_terminate = True
            self._can_peek_buffer_event.set()
            self._messaging_service.api.can_send_received.set()
            self._publisher_thread_stop_event.set()
            self._message_publisher_thread.join()

    def _stop_publisher_readiness_listener_thread(self):
        # """ this method is to stop publisher readiness listener thread """
        if self._publisher_readiness_listener_thread is not None:
            self._messaging_service.api.can_send_received.set()
            self._publisher_readiness_listener_thread_stop_event.set()
            self._publisher_readiness_listener_thread.join()

    def __is_eligible_for_termination(self):
        if self._message_publisher_state == MessagePublisherState.TERMINATING:
            logger.warning('Direct Message publisher termination is in-progress')
            return False
        elif self._message_publisher_state == MessagePublisherState.TERMINATED:
            logger.warning('Direct Message publisher already terminated')
            return False
        return True
