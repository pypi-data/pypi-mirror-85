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

"""Module contains the implementation cass and methods for the DirectMessageReceiver"""
# pylint: disable=duplicate-code

import concurrent
import copy
import logging
import queue
import threading
from concurrent.futures.thread import ThreadPoolExecutor
from ctypes import Structure, c_int, c_uint32, c_void_p, py_object, CFUNCTYPE
from queue import Queue

from solace.messaging.config.sol_constants import SOLCLIENT_CALLBACK_TAKE_MSG, SOLCLIENT_OK, SOLCLIENT_FAIL, \
    GRACE_PERIOD_MIN_MS, GRACE_PERIOD_MAX_MS
from solace.messaging.config.solace_message_constants import CANNOT_START_RECEIVER, \
    RECEIVER_CANNOT_BE_STARTED_EXCEPTION_MESSAGE, RECEIVER_NOT_STARTED, RECEIVER_TERMINATED, \
    UNABLE_TO_SUBSCRIBE_TO_TOPIC, UNABLE_TO_UNSUBSCRIBE_TO_TOPIC, INVALID_DATATYPE, DISPATCH_FAILED, \
    VALUE_CANNOT_BE_NEGATIVE, NO_INCOMING_MESSAGE, TOPIC_NAME_TOO_LONG, RECEIVER_SERVICE_DOWN_EXIT_MESSAGE
from solace.messaging.core import _solace_session
from solace.messaging.core._solace_message import _SolaceMessage
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError, \
    IllegalStateError, InvalidDataTypeError, IllegalArgumentError, IncompleteMessageDeliveryError
from solace.messaging.receiver._impl._inbound_message import _InboundMessage
from solace.messaging.receiver.direct_message_receiver import DirectMessageReceiver
from solace.messaging.receiver.inbound_message import InboundMessage
from solace.messaging.receiver.inbound_message_utility import topic_subscribe_with_dispatch, \
    topic_unsubscribe_with_dispatch
from solace.messaging.receiver.message_receiver import MessageHandler, MessageReceiverState
from solace.messaging.resources.topic_subscription import TopicSubscription

logger = logging.getLogger('solace.messaging.receiver')


class _DirectMessageReceiverThread(threading.Thread):  # pylint: disable=missing-class-docstring
    # """ Thread used to dispatch received messages on a receiver. """

    def __init__(self, direct_message_receiver, messaging_service, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug('THREAD: [%s] initialized', type(self).__name__)
        self._message_receiver = direct_message_receiver
        self._direct_message_receiver_queue = self._message_receiver.receiver_queue
        self._message_handler = self._message_receiver.message_handler
        self._stop_event = self._message_receiver.stop_event  # we receive this from direct message impl class
        self._can_receive_event = self._message_receiver.can_receive_event
        self._receiver_empty_event = self._message_receiver.receiver_empty_event
        self._messaging_service = messaging_service

    def run(self):  # pylint: disable=missing-function-docstring
        # """ Start running thread """
        logger.debug('THREAD: [%s] started', type(self).__name__)
        while not self._stop_event.is_set():
            if self._messaging_service.api.message_service_state == _solace_session.MessagingServiceState.DOWN:
                # call the receiver's terminate method to ensure proper cleanup of thread
                logger.warning(RECEIVER_SERVICE_DOWN_EXIT_MESSAGE)
                if self._message_receiver.receiver_state == MessageReceiverState.TERMINATING:
                    self._receiver_empty_event.set()  # wakeup main thread when the service is down
                break
            else:
                if not self._can_receive_event.is_set() and \
                        self._message_receiver.receiver_state != MessageReceiverState.TERMINATING:
                    self._can_receive_event.wait()
                # don't attempt to retrieve message once buffer is declared as empty  at terminating
                # state( there is a chance we may keep receiving message callback which are in transit)
                if self._direct_message_receiver_queue.qsize() > 0 and not self._receiver_empty_event.is_set():
                    inbound_message = self._direct_message_receiver_queue.get()
                    if inbound_message:
                        try:
                            self._message_handler.on_message(inbound_message)
                        except Exception as exception:  # pylint: disable=broad-except
                            logger.warning("%s %s", DISPATCH_FAILED, str(exception))

                # don't block the thread at terminating state
                elif self._message_receiver.receiver_state != MessageReceiverState.TERMINATING:
                    self._can_receive_event.clear()

                if self._direct_message_receiver_queue.qsize() == 0 and \
                        self._message_receiver.receiver_state == MessageReceiverState.TERMINATING and \
                        not self._receiver_empty_event.is_set():
                    self._receiver_empty_event.set()  # let the main thread stop waiting in terminating state


class _DirectMessageReceiver(DirectMessageReceiver) \
        :  # pylint: disable=too-many-ancestors, too-many-instance-attributes, missing-class-docstring, missing-module-docstring, duplicate-code
    # """ class for direct message receiver, it is the base class used to receive direct messages """

    class SolClientReceiverCreateRxMsgDispatchFuncInfo(Structure) \
            :  # pylint: disable=too-few-public-methods, missing-class-docstring
        # """ Conforms to solClient_session_rxMsgDispatchFuncInfo """

        _fields_ = [
            ("dispatch_type", c_uint32),  # The type of dispatch described
            ("callback_p", CFUNCTYPE(c_int, c_void_p, c_void_p, py_object)),  # An application-defined callback
            # function; may be NULL if there is no callback.
            ("user_p", py_object),  # A user pointer to return with the callback; must be NULL if callback_p is NULL.
            ("rffu", c_void_p)  # Reserved for Future use; must be NULL
        ]

    def __init__(self, messaging_service, config):
        logger.debug('[%s] initialized', type(self).__name__)
        self._running = False
        self._messaging_service = messaging_service
        self._direct_message_receiver_queue = Queue()  # queue does not have max size
        self._message_handler = None
        self._can_receive_event = threading.Event()
        self._can_receive_id = "can_receive_" + str(hex(id(self)))
        setattr(self._messaging_service.api,
                self._can_receive_id, self._can_receive_event)
        self._messaging_service.api.can_receive.append(self._can_receive_id)
        self._direct_message_receiver_thread = None
        self._direct_message_receiver_thread_stop_event = threading.Event()
        self._msg_wait_time = None
        self._msg_callback_func_routine = self.msg_callback_func_type(self.__message_receive_callback_routine)
        self._topic_dict = {}
        self._group_name = None
        self._receiver_empty_event = threading.Event()
        self._is_unsubscribed = False
        key = "subscriptions"
        if key in config:
            subscription = config[key]
            if isinstance(subscription, str):
                self._topic_dict[subscription] = False  # not applied
            else:
                for topic in subscription:
                    self._topic_dict[topic] = False  # not applied
        key = "group_name"
        if key in config:
            self._group_name = config[key]
        self._direct_message_receiver_state = MessageReceiverState.NOT_STARTED

    def is_running(self) -> bool:
        is_running = self._direct_message_receiver_state == MessageReceiverState.STARTED
        logger.debug('[%s] is running?: %s', DirectMessageReceiver.__name__, is_running)
        return is_running

    def is_terminated(self) -> bool:
        is_terminated = MessageReceiverState.TERMINATED == self._direct_message_receiver_state
        logger.debug('[%s] is terminated?: %s', DirectMessageReceiver.__name__, is_terminated)
        return is_terminated

    def is_terminating(self) -> bool:
        is_terminating = MessageReceiverState.TERMINATING == self._direct_message_receiver_state
        logger.debug('[%s] is terminating?', is_terminating)
        return is_terminating

    def start(self) -> DirectMessageReceiver:
        # """ Start the DirectMessageReceiver synchronously (blocking). """
        self._direct_message_receiver_state = MessageReceiverState.STARTING
        logger.debug('[%s] is %s', DirectMessageReceiver.__name__, MessageReceiverState.STARTING.name)
        self.__is_message_service_connected()
        self.__do_start()
        return self

    def start_async(self) -> concurrent.futures.Future:
        # """ Start the DirectMessageReceiver asynchronously (non-blocking). """
        with ThreadPoolExecutor() as executor:
            return executor.submit(self.start)

    def receive_message(self, timeout: int = None) -> InboundMessage:
        # """ Get a message, blocking for the time configured in the receiver builder. """
        if timeout is not None:
            if not isinstance(timeout, int):
                raise InvalidDataTypeError(f'{INVALID_DATATYPE} Expected type: [{type(int)}], '
                                           f'but actual [{type(timeout)}]')
            if timeout < 0:
                raise IllegalArgumentError(VALUE_CANNOT_BE_NEGATIVE)
            timeout_in_seconds = timeout / 1000 if timeout is not None else None
            self._msg_wait_time = timeout_in_seconds
        logger.debug('Get message from queue/buffer')
        try:
            message = self._direct_message_receiver_queue.get(True, self._msg_wait_time)
            return message
        except queue.Empty as exception:
            raise PubSubPlusClientError(NO_INCOMING_MESSAGE) from exception

    @property
    def receiver_state(self):
        return self._direct_message_receiver_state

    @property
    def receiver_queue(self):
        return self._direct_message_receiver_queue

    @property
    def message_handler(self):
        return self._message_handler

    @property
    def stop_event(self):
        return self._direct_message_receiver_thread_stop_event

    @property
    def can_receive_event(self):
        return self._can_receive_event

    @property
    def receiver_empty_event(self):
        return self._receiver_empty_event

    def receive_async(self, message_handler: MessageHandler):
        # """ Specify the asynchronous message handler. """
        if not isinstance(message_handler, MessageHandler):
            logger.warning('%s Expected type: [%s], but actual [%s]', INVALID_DATATYPE, type(MessageHandler),
                           type(message_handler))
            raise InvalidDataTypeError(f'{INVALID_DATATYPE} Expected type: [{type(MessageHandler)}], '
                                       f'but actual [{type(message_handler)}]')
        if self.__is_receiver_started():
            if message_handler != self._message_handler and self._direct_message_receiver_thread is not None:
                self._direct_message_receiver_queue.put(None)
                self._direct_message_receiver_thread.join()
                self._direct_message_receiver_thread = None
            self._message_handler = message_handler
            self._direct_message_receiver_thread = _DirectMessageReceiverThread(self, self._messaging_service)
            self._direct_message_receiver_thread.daemon = True
            self._direct_message_receiver_thread.start()
        return self

    def add_subscription(self, another_subscription: TopicSubscription):
        # """ Subscribe to a topic synchronously (blocking). """
        self.__do_subscribe(another_subscription.get_name())

    def add_subscription_async(self, topic_subscription: TopicSubscription) -> concurrent.futures.Future:
        # """subscribe a topic from an async receiver"""
        with ThreadPoolExecutor() as executor:
            return executor.submit(self.add_subscription, topic_subscription)

    def remove_subscription(self, subscription: TopicSubscription):
        # """ Unsubscribe from a topic synchronously (blocking). """
        if isinstance(subscription, TopicSubscription):
            self.__do_unsubscribe(subscription.get_name())
        else:  # pragma: no cover
            logger.warning('Subscription is not type of [%s]', str(type(TopicSubscription)))
            raise PubSubPlusClientError(message=f'Subscription is not type of [{type(TopicSubscription)}]')

    def remove_subscription_async(self, topic_subscription: TopicSubscription):
        # """unsubscribe in an asynchronous receiver"""
        with ThreadPoolExecutor() as executor:
            return executor.submit(self.remove_subscription, topic_subscription)

    def __unsubscribe(self):
        # called as part of terminate
        # self._can_receive_event.set()  # dont block the thread while terminating
        if self._topic_dict and self._messaging_service.is_connected:
            self._is_unsubscribed = True
            topics = [*copy.deepcopy(self._topic_dict)]
            # unsubscribe topics as part of teardown activity
            for topic in topics:
                try:
                    self.__do_unsubscribe(topic)
                except PubSubPlusClientError as exception:  # pragma: no cover
                    logger.warning(exception)

    def _cleanup(self):
        self._direct_message_receiver_state = MessageReceiverState.TERMINATED
        if self._direct_message_receiver_thread is not None:
            # set thread termination flag before waking delivery thread
            # to ensure clean exit from python message delivery thread
            self._direct_message_receiver_thread_stop_event.set()

            self._can_receive_event.set()  # dont block the thread while terminating
            # wake message delivery thread
            # join on python message delivery thread
            self._direct_message_receiver_thread.join()

    def terminate_now(self):
        self._direct_message_receiver_state = MessageReceiverState.TERMINATING
        if not self._is_unsubscribed:  # unsubscribe only if its not done already
            self.__unsubscribe()
        self._cleanup()
        if self._direct_message_receiver_queue is not None and self._direct_message_receiver_queue.qsize() != 0:
            raise IncompleteMessageDeliveryError(f"Undelivered message count: "
                                                 f"[{self._direct_message_receiver_queue.qsize()}]")

    def terminate(self, grace_period: int = GRACE_PERIOD_MAX_MS):
        # """ Stop the receiver - put None in the queue which will stop our asynchronous
        #             dispatch thread, or the app will get if it asks for another message via sync. """
        if grace_period < GRACE_PERIOD_MIN_MS:
            raise IllegalArgumentError(f"grace_period must be >= {GRACE_PERIOD_MIN_MS}")
        grace_period_in_seconds = grace_period / 1000
        self._direct_message_receiver_state = MessageReceiverState.TERMINATING
        if not self._is_unsubscribed:  # unsubscribe only if its not done already
            self.__unsubscribe()
        self._can_receive_event.set()  # stop the thread from waiting
        if self._direct_message_receiver_thread:
            self._receiver_empty_event.wait(timeout=grace_period_in_seconds)
        self._cleanup()

    def terminate_async(self, grace_period: int = GRACE_PERIOD_MAX_MS):
        if grace_period < GRACE_PERIOD_MIN_MS:
            raise IllegalArgumentError(f"grace_period must be >= {GRACE_PERIOD_MIN_MS}")
        with ThreadPoolExecutor() as executor:
            return executor.submit(self.terminate, grace_period)

    def __is_message_service_connected(self):
        # """Method to validate message service is connected or not"""
        if not self._messaging_service.is_connected:
            self._direct_message_receiver_state = MessageReceiverState.NOT_STARTED
            logger.debug('[%s] is %s. MessagingService NOT connected', DirectMessageReceiver.__name__,
                         MessageReceiverState.NOT_STARTED.name)
            raise IllegalStateError(RECEIVER_CANNOT_BE_STARTED_EXCEPTION_MESSAGE)
        return True

    def __is_receiver_started(self) -> bool:
        # """Method to validate receiver is properly started or not"""
        self.__is_message_service_connected()
        if self._direct_message_receiver_state == MessageReceiverState.NOT_STARTED or \
                self._direct_message_receiver_state == MessageReceiverState.STARTING:
            raise IllegalStateError(RECEIVER_NOT_STARTED)
        if self._direct_message_receiver_state == MessageReceiverState.TERMINATING or \
                self._direct_message_receiver_state == MessageReceiverState.TERMINATED:
            raise IllegalStateError(RECEIVER_TERMINATED)
        if self._direct_message_receiver_state != MessageReceiverState.STARTED:
            raise IllegalStateError(RECEIVER_NOT_STARTED)
        logger.debug('[%s] %s', DirectMessageReceiver.__name__, MessageReceiverState.STARTED.name)
        return True

    def __do_start(self):
        # """ start the DirectMessageReceiver (always blocking). """
        errors = None
        for topic, subscribed in self._topic_dict.items():
            if not subscribed:
                try:
                    self.add_subscription(TopicSubscription.of(topic))
                    self._topic_dict[topic] = True
                except PubSubPlusClientError as exception:  # pragma: no cover
                    errors = str(exception) if errors is None else errors + "; " + str(exception)
                    self._direct_message_receiver_state = MessageReceiverState.NOT_STARTED
                    logger.warning("%s %s", CANNOT_START_RECEIVER, str(errors))
                    raise PubSubPlusClientError(message=f"{CANNOT_START_RECEIVER}{str(errors)}") from exception
                    # pragma: no cover
        self._running = True
        self._direct_message_receiver_state = MessageReceiverState.STARTED
        logger.debug('[%s] is %s', DirectMessageReceiver.__name__, MessageReceiverState.STARTED.name)

    def __do_subscribe(self, topic_subscription: str):
        # """ Subscribe to a topic (always blocking). """
        if self._group_name is None or self._group_name == '':
            subscribe_to = topic_subscription
        else:
            subscribe_to = "#share/" + self._group_name + "/" + topic_subscription
        logger.debug('SUBSCRIBE to: [%s]', subscribe_to)

        dispatch_info = self.SolClientReceiverCreateRxMsgDispatchFuncInfo(
            c_uint32(1),
            self._msg_callback_func_routine,
            py_object(self),
            c_void_p(None))

        return_code = topic_subscribe_with_dispatch(
            session_p=self._messaging_service.session_pointer,
            subscription=subscribe_to,
            dispatch_info=dispatch_info)
        if return_code == SOLCLIENT_OK:
            self._topic_dict[topic_subscription] = True
        elif return_code == SOLCLIENT_FAIL and len(topic_subscription) > 250:
            logger.warning("%s, name is %d bytes", TOPIC_NAME_TOO_LONG, len(topic_subscription))
            raise PubSubPlusClientError(message=f'{TOPIC_NAME_TOO_LONG}, name is {len(topic_subscription)} bytes')
        else:
            logger.warning('%s %s. Status code: %d',
                           UNABLE_TO_SUBSCRIBE_TO_TOPIC, subscribe_to, return_code)  # pragma: no cover
            raise PubSubPlusClientError(message=f'{UNABLE_TO_SUBSCRIBE_TO_TOPIC} {subscribe_to}. '
                                                f'Status code: {return_code}')  # pragma: no cover

    def __do_unsubscribe(self, topic_subscription: str):
        # """ Unsubscribe from a topic (always blocking)."""
        if self._group_name is None or self._group_name == '':
            unsubscribe_to = topic_subscription
        else:
            unsubscribe_to = "#share/" + self._group_name + "/" + topic_subscription
        logger.debug('UNSUBSCRIBE to: [%s]', unsubscribe_to)
        dispatch_info = self.SolClientReceiverCreateRxMsgDispatchFuncInfo(c_uint32(1), self._msg_callback_func_routine,
                                                                          py_object(self), c_void_p(None))

        return_code = topic_unsubscribe_with_dispatch(
            session_p=self._messaging_service.session_pointer, subscription=unsubscribe_to,
            dispatch_info=dispatch_info)
        if topic_subscription in self._topic_dict:
            del self._topic_dict[topic_subscription]
        if return_code != SOLCLIENT_OK:
            logger.warning('%s [%s]. Status code: %d',
                           UNABLE_TO_UNSUBSCRIBE_TO_TOPIC, unsubscribe_to, return_code)  # pragma: no cover
            raise PubSubPlusClientError(message=f'{UNABLE_TO_UNSUBSCRIBE_TO_TOPIC} [{unsubscribe_to}]. '
                                                f'Status code: {return_code}')  # pragma: no cover

    def __message_receive_callback_routine(self, opaque_session_p, msg_p, user_p) \
            :  # pragma: no cover  # pylint: disable=unused-argument
        # """The message callback is invoked for each Direct message received by the Session """
        try:
            solace_message = _SolaceMessage(c_void_p(msg_p))
            rx_msg = _InboundMessage(solace_message)
            self._direct_message_receiver_queue.put(rx_msg)
            self._can_receive_event.set()
            logger.debug('PUT message to %s buffer/queue', {DirectMessageReceiver.__name__})
        except Exception as exception:
            logger.error(exception)
            raise PubSubPlusClientError(message=exception) from exception
        return SOLCLIENT_CALLBACK_TAKE_MSG  # we took the received message

    def __is_eligible_for_termination(self):
        if self._direct_message_receiver_state == MessageReceiverState.TERMINATING:
            logger.warning('Message receiver termination is in-progress')
            return False
        elif self._direct_message_receiver_state == MessageReceiverState.TERMINATED:
            logger.warning('Message receiver already terminated')
            return False
        return True
