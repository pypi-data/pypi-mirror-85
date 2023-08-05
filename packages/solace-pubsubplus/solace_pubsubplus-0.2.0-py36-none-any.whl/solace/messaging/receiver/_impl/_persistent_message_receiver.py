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

"""Module contains the implementation class and methods for the PersistentMessageReceiver"""
# pylint: disable=too-many-instance-attributes, too-many-arguments, missing-function-docstring
# pylint: disable=duplicate-code
import concurrent
import copy
import ctypes
import logging
import queue
import threading
import time
import weakref
from concurrent.futures._base import Future
from concurrent.futures.thread import ThreadPoolExecutor
from ctypes import Structure, c_void_p, py_object, CFUNCTYPE, c_int, POINTER, c_char_p, cast, byref, sizeof
from queue import Queue

import solace
from solace.messaging.config.ccsmp_property_mapping import end_point_props, CCSMP_SESSION_PROP_MAPPING
from solace.messaging.config.ccsmp_property_mapping import flow_props
from solace.messaging.config.missing_resources_creation_configuration import MissingResourcesCreationStrategy
from solace.messaging.config.receiver_activation_passivation_configuration import ReceiverStateChangeListener
from solace.messaging.config.sol_constants import SOLCLIENT_OK, SOLCLIENT_FLOW_PROP_BIND_NAME, \
    SOLCLIENT_FLOW_PROP_BIND_ENTITY_DURABLE, SOLCLIENT_CALLBACK_TAKE_MSG, SOLCLIENT_CALLBACK_OK, SolClientSubCode, \
    SOLCLIENT_ENDPOINT_PROP_NAME, SolClientFlowEvent, SOLCLIENT_DISPATCH_TYPE_CALLBACK, HIGH_THRESHOLD, LOW_THRESHOLD, \
    SOLCLIENT_ENDPOINT_PROP_ACCESSTYPE, SOLCLIENT_ENDPOINT_PROP_ACCESSTYPE_NONEXCLUSIVE, SOLCLIENT_FLOW_PROP_SELECTOR, \
    SOLCLIENT_FLOW_PROP_ACKMODE, SOLCLIENT_FLOW_PROP_ACKMODE_AUTO, SOLCLIENT_FAIL, GRACE_PERIOD_MIN_MS, \
    GRACE_PERIOD_MAX_MS
from solace.messaging.config.solace_message_constants import UNABLE_TO_SUBSCRIBE_TO_TOPIC, DISPATCH_FAILED, \
    RECEIVER_NOT_STARTED, RECEIVER_TERMINATED, RECEIVER_CANNOT_BE_STARTED_EXCEPTION_MESSAGE, \
    UNABLE_TO_UNSUBSCRIBE_TO_TOPIC, FLOW_PAUSE, FLOW_RESUME, \
    INVALID_DATATYPE, VALUE_CANNOT_BE_NEGATIVE, NO_INCOMING_MESSAGE, TOPIC_NAME_TOO_LONG, \
    RECEIVER_SERVICE_DOWN_EXIT_MESSAGE, STATE_CHANGE_LISTENER_SERVICE_DOWN_EXIT_MESSAGE
from solace.messaging.core import _solace_session
from solace.messaging.core._core_api_utility import prepare_array
from solace.messaging.core._solace_message import _SolaceMessage
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError, \
    IllegalStateError, InvalidDataTypeError, IllegalArgumentError, IncompleteMessageDeliveryError
from solace.messaging.receiver._impl._inbound_message import _InboundMessage
from solace.messaging.receiver.inbound_message import InboundMessage
from solace.messaging.receiver.inbound_message_utility import acknowledge_message, pause, resume, \
    flow_topic_subscribe_with_dispatch, flow_topic_unsubscribe_with_dispatch, end_point_provision
from solace.messaging.receiver.message_receiver import MessageHandler, MessageReceiverState
from solace.messaging.receiver.persistent_message_receiver import PersistentMessageReceiver
from solace.messaging.resources.topic_subscription import TopicSubscription
from solace.messaging.solace_logging.core_api_log import last_error_info

logger = logging.getLogger('solace.messaging.receiver')


def flow_cleanup(flow_p, session_p):
    """function to clean-up the flow pointer"""
    try:
        if session_p and flow_p:  # proceed to clean-up only if we still have  the session
            return_code = solace.CORE_LIB.solClient_flow_destroy(ctypes.byref(flow_p))
            if return_code != SOLCLIENT_OK:
                logger.warning(last_error_info(return_code, "flow_cleanup"))
    except PubSubPlusClientError as exception:
        logger.warning('Flow cleanup failed. Exception: %s %s', str(exception), str(flow_p))


class PersistentStateChangeListenerThread(threading.Thread) \
        :  # pylint: disable=missing-class-docstring, too-many-instance-attributes, too-many-arguments
    # """ Thread used to dispatch received flow state on a receiver. """

    def __init__(self, state_change_queue: Queue, receiver_state_change_listener: ReceiverStateChangeListener,
                 can_listen_event, stop_event, messaging_service, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug('THREAD: [%s] initialized', type(self).__name__)
        self._state_change_queue = state_change_queue
        self.receiver_state_change_listener = receiver_state_change_listener
        self._running = False
        self._stop_event = stop_event
        self._can_listen_event = can_listen_event
        self._messaging_service_state = messaging_service.api.message_service_state

    def run(self):  # pylint: disable=missing-function-docstring
        # """ Start running thread """
        logger.debug('THREAD: [%s] started', type(self).__name__)
        while not self._stop_event.is_set():
            if self._messaging_service_state == _solace_session.MessagingServiceState.DOWN:
                # call the receiver's terminate method to ensure proper cleanup of thread
                logger.warning(STATE_CHANGE_LISTENER_SERVICE_DOWN_EXIT_MESSAGE)
                break
            else:
                if not self._can_listen_event.is_set():
                    self._can_listen_event.wait()
                if self._state_change_queue.qsize() > 0:
                    old_state, new_state, time_stamp = self._state_change_queue.get()
                    try:
                        self.receiver_state_change_listener.on_change(old_state, new_state, time_stamp)
                    except Exception as exception:  # pylint: disable=broad-except
                        logger.warning("%s %s", DISPATCH_FAILED, str(exception))
                else:
                    self._can_listen_event.clear()


class PersistentMessageReceiverThread(threading.Thread):  # pylint: disable=missing-class-docstring
    # """ Thread used to dispatch received messages on a receiver. """
    def __init__(self, persistent_message_receiver,
                 message_pop_func, messaging_service,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug('THREAD: [%s] initialized', type(self).__name__)
        self._persistent_message_receiver = persistent_message_receiver
        self._persistent_message_receiver_queue = self._persistent_message_receiver.receiver_queue
        self._message_handler = self._persistent_message_receiver.message_handler
        self._block_event = self._persistent_message_receiver.stop_event  # we receive this from persistent message impl class
        self._can_receive_event = self._persistent_message_receiver.can_receive_event
        self._persistent_message_receiver_state = self._persistent_message_receiver.receiver_state
        self._receiver_empty_event = self._persistent_message_receiver.receiver_empty_event
        # closure function to return an inbound message
        # function signature is parameterless
        self._message_pop = message_pop_func
        self._messaging_service = messaging_service

    def run(self):  # pylint: disable=missing-function-docstring
        # """ Start running thread """
        logger.debug('THREAD: [%s] started', type(self).__name__)
        while not self._block_event.is_set():
            if self._messaging_service.api.message_service_state == _solace_session.MessagingServiceState.DOWN:
                # call the receiver's terminate method to ensure proper cleanup of thread
                logger.warning(RECEIVER_SERVICE_DOWN_EXIT_MESSAGE)
                if self._persistent_message_receiver.receiver_state == MessageReceiverState.TERMINATING:
                    self._receiver_empty_event.set()  # wakeup main thread when the service is down while terminating
                break
            else:
                if not self._can_receive_event.is_set() and \
                        self._persistent_message_receiver.receiver_state != MessageReceiverState.TERMINATING:
                    self._can_receive_event.wait()
                # don't attempt to retrieve message once buffer is declared as empty  at terminating
                # state( there is a chance we may keep receiving message callback which are in transit)
                if self._persistent_message_receiver_queue.qsize() > 0 and not self._receiver_empty_event.is_set():
                    inbound_message = self._message_pop()
                    if inbound_message:
                        try:
                            self._message_handler.on_message(inbound_message)
                        except Exception as exception:  # pylint: disable=broad-except
                            logger.warning("%s [%s] %s", DISPATCH_FAILED, type(self._message_handler), str(exception))
                elif self._persistent_message_receiver.receiver_state != MessageReceiverState.TERMINATING:
                    self._can_receive_event.clear()
                # wakeup main thread to proceed to call clean-up
                if self._persistent_message_receiver_queue.qsize() == 0 and \
                        self._persistent_message_receiver.receiver_state == MessageReceiverState.TERMINATING and \
                        not self._receiver_empty_event.is_set():
                    self._receiver_empty_event.set()  # let the main thread stop waiting in terminating state
        logger.debug('THREAD: [%s] stopped', type(self).__name__)


class _PersistentMessageReceiver(PersistentMessageReceiver) \
        :  # pylint: disable=missing-class-docstring, too-many-ancestors, too-many-instance-attributes
    class SolClientFlowEventCallbackInfo(Structure):  # pylint: disable=too-few-public-methods
        """ Conforms to solClient_flow_eventCallbackInfo_t """
        _fields_ = [
            ("flow_event", c_int),
            ("response_code", c_int),
            ("info_p", c_char_p),
        ]

    class SolClientFlowCreateRxCallbackFuncInfo(Structure) \
            :  # pylint: disable=too-few-public-methods, missing-class-docstring
        # """ Conforms to solClient_flow_rxMsgDispatchFuncInfo_t """

        _fields_ = [
            ("dispatch_type", ctypes.c_uint32),  # The type of dispatch described
            ("callback_p", CFUNCTYPE(c_int, c_void_p, c_void_p, py_object)),  # An application-defined callback
            # function; may be NULL if there is no callback.
            ("user_p", py_object),
            # A user pointer to return with the callback; must be NULL if callback_p is NULL.
            ("rffu", c_void_p)  # Reserved for Future use; must be NULL
        ]

    msg_callback_func_type = CFUNCTYPE(c_int, c_void_p, c_void_p, py_object)
    flow_msg_callback_func_type = CFUNCTYPE(c_int, c_void_p, c_void_p, py_object)
    solClient_flow_eventCallbackInfo_pt = POINTER(SolClientFlowEventCallbackInfo)

    _event_callback_func_type = CFUNCTYPE(c_int, c_void_p,
                                          solClient_flow_eventCallbackInfo_pt, py_object)
    _event_callback_func_routine = None
    _flow_msg_callback_func_routine = None

    def __init__(self, persistent_message_receiver: '_PersistentMessageReceiverBuilderImpl'):
        self._flow_p = c_void_p(None)
        self._persistent_message_receiver = persistent_message_receiver
        self._messaging_service = self._persistent_message_receiver.messaging_service
        self._missing_resource_strategy = self._persistent_message_receiver.strategy
        self._is_durable = self._persistent_message_receiver.endpoint_to_consume_from.is_durable()
        self._is_exclusive = self._persistent_message_receiver.endpoint_to_consume_from.is_exclusively_accessible()
        self._queue_name = self._persistent_message_receiver.endpoint_to_consume_from.get_name()
        self._message_handler = None
        self._topics = self._persistent_message_receiver.topics
        self._msg_wait_time = None
        self._stop_event = threading.Event()
        self._can_receive_event = threading.Event()
        self._can_receive_id = "can_receive_" + str(hex(id(self)))
        setattr(self._messaging_service.api,
                self._can_receive_id, self._can_receive_event)
        self._messaging_service.api.can_receive.append(self._can_receive_id)
        self._receiver_empty_event = threading.Event()
        self._persistent_message_receiver_queue = Queue()
        self._persistent_message_receiver_thread = None
        self._receiver_state_change_listener = self._persistent_message_receiver.receiver_state_change_listener
        self._flow_state = list()  # to keep track of flow state when listener is provided
        self._running = False  # used for pause & resume when True application callbacks should be dispatching
        self._flow_stopped = False  # used for flow control to close the flow message window
        self._end_point_arr = None
        if self._receiver_state_change_listener:
            self._state_change_listener_queue = Queue()
            self._state_change_can_listen_event = threading.Event()
            self._state_change_id = "state_change_" + str(hex(id(self)))
            setattr(self._messaging_service.api,
                    self._state_change_id, self._state_change_can_listen_event)
            self._messaging_service.api.state_change.append(self._state_change_id)
            self._state_change_stop_event = threading.Event()
            self._state_change_listener_thread = None
        else:
            self._state_change_listener_queue = None
        self._flow_msg_callback_func_routine = self.flow_msg_callback_func_type(
            self._flow_message_receive_callback_routine)
        self._topic_dict = dict()
        self._persistent_message_receiver_state = MessageReceiverState.NOT_STARTED
        # tmp_valid_props = [var for var in vars(valid_receiver_properties) if not var.startswith('__')]
        self._config = dict()
        # add props received from builder
        for key, value in self._persistent_message_receiver.config.items():
            if key in CCSMP_SESSION_PROP_MAPPING:
                if type(value) is int:  # pylint: disable=unidiomatic-typecheck
                    value = str(value)
                elif type(value) is bool:  # pylint: disable=unidiomatic-typecheck
                    value = str(int(value))
                self._config[CCSMP_SESSION_PROP_MAPPING[key]] = value
        self._config[SOLCLIENT_FLOW_PROP_BIND_NAME] = self._queue_name
        self._config[SOLCLIENT_FLOW_PROP_BIND_ENTITY_DURABLE] = str(int(self._is_durable))
        if self._persistent_message_receiver.message_selector:  # message selector applied here
            self._config[SOLCLIENT_FLOW_PROP_SELECTOR] = self._persistent_message_receiver.message_selector
        if self._persistent_message_receiver.auto_ack:  # auto ack enabled here
            self._config[SOLCLIENT_FLOW_PROP_ACKMODE] = SOLCLIENT_FLOW_PROP_ACKMODE_AUTO
        self._event_callback_func_routine = self._event_callback_func_type(self._event_callback_routine)
        self._flow_msg_callback_func_routine = self.msg_callback_func_type(self._flow_message_receive_callback_routine)

        self._config = {**flow_props, **self._config}  # merge & override happens here
        self._flow_arr = prepare_array(self._config)

        self._finalizer = weakref.finalize(self, flow_cleanup, self._flow_p,
                                           self._messaging_service.api.session_pointer)  # clean-up the flow as part of gc

    @property
    def flow_p(self):
        # """property which holds and returns the flow pointer"""
        return self._flow_p

    def _start_state_listener(self):
        # """This mehod is used to start the receiver state change listener thread"""
        if self._receiver_state_change_listener:
            self._state_change_listener_thread = PersistentStateChangeListenerThread(
                self._state_change_listener_queue, self._receiver_state_change_listener,
                self._state_change_can_listen_event, self._state_change_stop_event, self._messaging_service)
            self._state_change_listener_thread.daemon = True
            self._state_change_listener_thread.start()

    def _flow_message_receive_callback_routine(self, opaque_flow_p, msg_p, user_p) \
            :  # pragma: no cover  # pylint: disable=unused-argument
        # """The message callback is invoked for each Persistent message received by the Session """
        # only enqueue message while the receiver is live
        if self._persistent_message_receiver_state not in [MessageReceiverState.STARTING, MessageReceiverState.STARTED]:
            # Unfortunately its not possible to determine how many
            # in-flight messages remaining in the flow message window on shutdown.
            # Drop messages while terminating to prevent a race between 
            # native layer message dispatch and draining the python
            # internal message queue for graceful terminate.
            return SOLCLIENT_CALLBACK_OK  # return the received message to native layer
        # python receiver is life enqueue native message to python delivery queue
        try:
            solace_message = _SolaceMessage(c_void_p(msg_p))
            rx_msg = _InboundMessage(solace_message)
            self._msg_queue_put(rx_msg)
            if self._running:
                # only signal message dispatch thread if python message dispatch is running
                self._can_receive_event.set()
            logger.debug('PUT message to %s buffer/queue', {PersistentMessageReceiver.__name__})
        except Exception as exception:
            logger.error(exception)
            raise PubSubPlusClientError(message=exception) from exception
        return SOLCLIENT_CALLBACK_TAKE_MSG  # we took the received message

    def _event_callback_routine(self, opaque_flow_p, event_info_p, user_p):  # pylint: disable=unused-argument
        """ Flow event callback from the C API. """
        event = event_info_p.contents.flow_event
        if self._state_change_listener_queue:
            events = {SolClientFlowEvent.SOLCLIENT_FLOW_EVENT_ACTIVE.value:
                          (SolClientFlowEvent.SOLCLIENT_FLOW_EVENT_INACTIVE,
                           SolClientFlowEvent.SOLCLIENT_FLOW_EVENT_ACTIVE),
                      SolClientFlowEvent.SOLCLIENT_FLOW_EVENT_INACTIVE.value:
                          (SolClientFlowEvent.SOLCLIENT_FLOW_EVENT_ACTIVE,
                           SolClientFlowEvent.SOLCLIENT_FLOW_EVENT_INACTIVE)}
            if event in events:
                old_state, new_state = events[event]
                self._state_change_can_listen_event.set()
                self._state_change_listener_queue.put((old_state, new_state, time.time()))

        return SOLCLIENT_CALLBACK_OK

    def _create_end_point(self):

        # create only for durable Queue, non-durable(temporary) Queue will be created during flow creation automatically
        if self._missing_resource_strategy:
            if self._missing_resource_strategy.value == MissingResourcesCreationStrategy.CREATE_ON_START.value and \
                    self._is_durable:
                end_point_props[SOLCLIENT_ENDPOINT_PROP_NAME] = self._queue_name  # set Queue name
                if not self._is_exclusive:
                    end_point_props[SOLCLIENT_ENDPOINT_PROP_ACCESSTYPE] = \
                        SOLCLIENT_ENDPOINT_PROP_ACCESSTYPE_NONEXCLUSIVE
                self._end_point_arr = prepare_array(end_point_props)
                return_code = end_point_provision(self._end_point_arr,
                                                  self._messaging_service.api.session_pointer)
                error_info = last_error_info(status_code=return_code, caller_desc="Endpoint Creation ")
                if return_code != SOLCLIENT_OK:
                    if error_info['sub_code'] == SolClientSubCode.SOLCLIENT_SUBCODE_ENDPOINT_ALREADY_EXISTS:
                        logger.info("%s already exists", self._queue_name)
                    elif error_info['sub_code'] in [SolClientSubCode.SOLCLIENT_SUBCODE_PERMISSION_NOT_ALLOWED,
                                                    SolClientSubCode.SOLCLIENT_SUBCODE_ENDPOINT_PROPERTY_MISMATCH]:
                        logger.warning("%s creation failed with the following sub code %s", self._queue_name,
                                       error_info['sub_code'])
                        raise PubSubPlusClientError(f"{self._queue_name}creation failed with the"
                                                    f" following sub code{error_info['sub_code']} ")
                elif return_code == SOLCLIENT_OK:
                    logger.info("%s endpoint is created successfully", self._queue_name)

    def start(self) -> 'PersistentMessageReceiver':
        # """implementation method to start the receiver"""
        self._persistent_message_receiver_state = MessageReceiverState.STARTING
        self.__is_message_service_connected()
        self._create_end_point()
        self._start_state_listener()
        self._do_start()
        if self._topics:
            for topic in self._topics:
                self.add_subscription(topic)
        self._persistent_message_receiver_state = MessageReceiverState.STARTED
        self._running = True
        return self

    def start_async(self) -> concurrent.futures.Future:
        # """ Start the PersistentMessageReceiver asynchronously (non-blocking). """
        with ThreadPoolExecutor() as executor:
            return executor.submit(self.start)

    @property
    def receiver_state(self):
        return self._persistent_message_receiver_state

    @property
    def receiver_queue(self):
        return self._persistent_message_receiver_queue

    @property
    def message_handler(self):
        return self._message_handler

    @property
    def stop_event(self):
        return self._stop_event

    @property
    def can_receive_event(self):
        return self._can_receive_event

    @property
    def receiver_empty_event(self):
        return self._receiver_empty_event

    def receive_async(self, message_handler: 'MessageHandler'):
        # """receives the messages asynchronously"""
        if not isinstance(message_handler, MessageHandler):
            logger.warning('%s Expected type: [%s], but actual [%s]', INVALID_DATATYPE, type(MessageHandler),
                           type(message_handler))
            raise InvalidDataTypeError(f'{INVALID_DATATYPE} Expected type: [{type(MessageHandler)}], '
                                       f'but actual [{type(message_handler)}]')
        if self.__is_receiver_started():
            if message_handler != self._message_handler and self._persistent_message_receiver_thread is not None:
                self._persistent_message_receiver_queue.put(None)
                self._persistent_message_receiver_thread.join()
                self._persistent_message_receiver_thread = None
            self._message_handler = message_handler

            def _receiver_thread_msg_queue_pop():
                logger.debug('Receiver [%s]: dispatching message, for endpoint [%s]', type(self).__name__,
                             self._queue_name)
                return self._msg_queue_get()

            self._persistent_message_receiver_thread = \
                PersistentMessageReceiverThread(self, _receiver_thread_msg_queue_pop, self._messaging_service)
            self._persistent_message_receiver_thread.daemon = True
            self._persistent_message_receiver_thread.start()
        return self

    def _msg_queue_put(self, message: 'InboundMessage'):
        self._persistent_message_receiver_queue.put(message)
        if self._persistent_message_receiver_queue.qsize() >= HIGH_THRESHOLD and not self._flow_stopped:
            # close c layer flow message window
            return_code = pause(self._flow_p)
            if return_code == SOLCLIENT_OK:
                # set c layer flow stopped state flag to stopped
                self._flow_stopped = True
                logger.info(FLOW_PAUSE)

    def _msg_queue_get(self, block: bool = True, timeout: float = None):
        logger.debug(f'Get message from queue/buffer with block {block} timeout {timeout}')
        # if block is not None:
        # wait for queue message blocking for timeout
        # can raise exception on timeout
        msg = self._persistent_message_receiver_queue.get(block, timeout)
        # else:
        #     msg = self._persistent_message_receiver_queue.get()
        # resume flow messaging if enough messages are processed and receiver state is Started
        if self._persistent_message_receiver_queue.qsize() <= LOW_THRESHOLD \
                and self._flow_stopped \
                and self._persistent_message_receiver_state == MessageReceiverState.STARTED:
            # open c layer flow message window
            return_code = resume(self._flow_p)
            if return_code == SOLCLIENT_OK:
                # set c layer flow stopped state flag to started
                self._flow_stopped = False
                logger.info(FLOW_RESUME)
        return msg

    def receive_message(self, timeout: int = None) -> InboundMessage:
        # """ Get a message, blocking for the time passed in timeout """
        if timeout is not None:
            if not isinstance(timeout, int):
                raise InvalidDataTypeError(f'{INVALID_DATATYPE} Expected type: [{type(int)}], '
                                           f'but actual [{type(timeout)}]')
            if timeout < 0:
                raise IllegalArgumentError(VALUE_CANNOT_BE_NEGATIVE)
            timeout_in_seconds = timeout / 1000 if timeout is not None else None
            self._msg_wait_time = timeout_in_seconds
        try:
            return self._msg_queue_get(block=True, timeout=self._msg_wait_time)
        except queue.Empty as exception:
            raise PubSubPlusClientError(NO_INCOMING_MESSAGE) from exception

    def _cleanup(self):
        # """method to stop the receiver thread and set the stop event"""
        self._persistent_message_receiver_state = MessageReceiverState.TERMINATED
        if self._topic_dict and self._messaging_service.is_connected:
            self._is_unsubscribed = True
            topics = [*copy.deepcopy(self._topic_dict)]
            # unsubscribe topics as part of teardown activity
            for topic in topics:
                try:
                    self._do_unsubscribe(topic)
                except PubSubPlusClientError as exception:  # pragma: no cover
                    logger.warning(exception)
        if self._persistent_message_receiver_thread is not None:
            # stop the receiver thread
            # set termination flag first
            self._stop_event.set()  # this stops the thread
            # then wake up receiver thread to end run function
            self._can_receive_event.set()  # this wake up the thread
            self._persistent_message_receiver_thread.join()

            # stop the state change listener thread
        if self._receiver_state_change_listener:
            self._state_change_can_listen_event.set()
            self._state_change_stop_event.set()
            self._state_change_listener_thread.join()
        session_p = self._messaging_service.api.session_pointer \
            if self._messaging_service.api \
               and self._messaging_service.api.session_pointer \
            else c_void_p(None)
        # release c resources
        flow_cleanup(self._flow_p, session_p)
        # notify application of any remaining buffered data
        if self._persistent_message_receiver_queue is not None and self._persistent_message_receiver_queue.qsize() != 0:
            raise IncompleteMessageDeliveryError(f" undelivered message count :"
                                                 f" {self._persistent_message_receiver_queue.qsize()}")

    def __stop_flow(self):
        # """ shutdown all c api message dispatching """
        if not self._flow_stopped and self._messaging_service.api.session_pointer:  # pause the flow of inbound messages only if its not done already
            # close the c layer flow emssage window to stop receiver new messages for dispatch
            return_code = pause(self._flow_p)
            # confirm success
            if return_code != SOLCLIENT_OK:
                raise PubSubPlusClientError(last_error_info(return_code, "Flow Pause"))
            else:
                # update c layer flow start stop state flag
                self._flow_stopped = True

    def __prepare_terminate(self, grace_period):
        if grace_period < GRACE_PERIOD_MIN_MS:
            raise IllegalArgumentError(f"grace_period must be >= {GRACE_PERIOD_MIN_MS}")
        # set receiver state to TERMINATING this will prevent the native message
        # dispatch from enqueing new message for python delivery.
        # Only messages in the internal python message delivery queue
        # will be dispatch will be delivered to the application during
        # terminate
        self._persistent_message_receiver_state = MessageReceiverState.TERMINATING

    def terminate_now(self):
        self._persistent_message_receiver_state = MessageReceiverState.TERMINATING
        # Shutdown c layer flow message dispatch.
        # A protocol window of messages in-flight may still
        # dispatched from the native layer. These must be drop in python
        # See native flow message callback function for more details
        self.__stop_flow()
        # cleanup receiver resources
        self._cleanup()

    def terminate(self, grace_period: int = GRACE_PERIOD_MAX_MS):
        # """ Stop the receiver - put None in the queue which will stop our asynchronous
        #             dispatch thread, or the app will get if it asks for another message via sync. """
        self.__prepare_terminate(grace_period)
        grace_period_in_seconds = grace_period / 1000
        self.__stop_flow()
        # note this wakes the message delivery even when receiver is paused
        # this is better then blocking for the whole grace period
        self._can_receive_event.set()  # stop the thread from waiting
        if self._persistent_message_receiver_thread:
            self._receiver_empty_event.wait(timeout=grace_period_in_seconds)
        self.terminate_now()

    def terminate_async(self, grace_period: int = GRACE_PERIOD_MAX_MS) -> concurrent.futures:
        # """ Terminate the PersistentMessageReceiver asynchronously (non-blocking). """
        self.__prepare_terminate(grace_period)
        with ThreadPoolExecutor() as executor:
            return executor.submit(self.terminate, grace_period)

    def is_running(self) -> bool:
        # """Checks if process was successfully started and not stopped yet"""
        is_running = self._persistent_message_receiver_state == MessageReceiverState.STARTED
        logger.debug('[%s] is running?: %s', MessageReceiverState.__name__, is_running)
        return is_running

    def is_terminated(self) -> bool:
        # """Checks if message delivery process is terminated"""
        is_terminated = MessageReceiverState.TERMINATED == self._persistent_message_receiver_state
        logger.debug('[%s] is terminated?: %s', MessageReceiverState.__name__, is_terminated)
        return is_terminated

    def is_terminating(self) -> bool:
        # """Checks if message delivery process termination is ongoing"""
        is_terminating = MessageReceiverState.TERMINATING == self._persistent_message_receiver_state
        logger.debug('[%s] is terminating?', is_terminating)
        return is_terminating

    def pause(self):
        # """Pause message delivery to an asynchronous message handler or stream"""
        self._running = False
        self._can_receive_event.clear()

    def resume(self):
        # """Resumes previously paused message delivery."""
        self._running = True
        self._can_receive_event.set()

    def add_subscription(self, another_subscription: TopicSubscription):
        # """method to add the topic subscription"""
        self._do_subscribe(another_subscription.get_name())
        return self

    def remove_subscription(self, subscription: TopicSubscription):
        # """method to remove topic subscriptions"""
        self._do_unsubscribe(subscription.get_name())
        return self

    def add_subscription_async(self, topic_subscription: TopicSubscription) -> Future:
        # """method to add the subscription asynchronously"""
        with ThreadPoolExecutor() as executor:
            return executor.submit(self.add_subscription, topic_subscription)

    def remove_subscription_async(self, topic_subscription: TopicSubscription) -> Future:
        # """method to remove the subscription asynchronously"""
        with ThreadPoolExecutor() as executor:
            return executor.submit(self.remove_subscription, topic_subscription)

    def ack(self, message: 'InboundMessage'):
        # """method to ack the message"""
        return_code = acknowledge_message(self._flow_p, message.message_id)
        if return_code != SOLCLIENT_OK:
            raise PubSubPlusClientError(last_error_info(return_code, "Ack Message"))

    def _do_start(self):  # pylint: disable=no-else-raise
        # """method to start"""
        class SolClientFlowCreateRxCallbackFuncInfo(Structure):  # pylint: disable=too-few-public-methods
            """ Conforms to solClient_flow_createRxCallbackFuncInfo_t (deprecated) """
            _fields_ = [
                ("callback_p", c_void_p),
                ("user_p", c_void_p)
            ]

        class SolClientFlowCreateEventCallbackFuncInfo(Structure):  # pylint: disable=too-few-public-methods
            """ Conforms to solClient_flow_createEventCallbackFuncInfo_t """
            _fields_ = [
                ("callback_p", self._event_callback_func_type),
                ("user_p", py_object)
            ]

        class SolClientFlowCreateRxMsgCallbackFuncInfo(Structure):  # pylint: disable=too-few-public-methods
            """ Conforms to solClient_flow_createRxMsgCallbackFuncInfo_t """
            _fields_ = [
                ("callback_p", _PersistentMessageReceiver.msg_callback_func_type),
                ("user_p", py_object)
            ]

        class SolClientFlowCreateFuncInfo(Structure):  # pylint: disable=too-few-public-methods
            """ Conforms to solClient_flow_createFuncInfo_t """
            _fields_ = [
                ("rx_info", SolClientFlowCreateRxCallbackFuncInfo),  # deprecated
                ("event_info", SolClientFlowCreateEventCallbackFuncInfo),
                ("rx_msg_info", SolClientFlowCreateRxMsgCallbackFuncInfo)
            ]

        flow_func_info = SolClientFlowCreateFuncInfo(
            (c_void_p(None), c_void_p(None)),
            (self._event_callback_func_routine, self),
            (self._flow_msg_callback_func_routine, self))
        return_code = solace.CORE_LIB.solClient_session_createFlow(cast(self._flow_arr, POINTER(c_char_p)),
                                                                   self._messaging_service.api.session_pointer,
                                                                   byref(self._flow_p),
                                                                   byref(flow_func_info),

                                                                   sizeof(flow_func_info))
        if return_code != SOLCLIENT_OK:  # pylint: disable=no-else-raise
            error_info = last_error_info(status_code=return_code, caller_desc="flow topic add sub ")
            logger.warning("Flow creation failed for Queue[%s] with sub code [%s]",
                           self._queue_name, error_info['sub_code'])
            raise PubSubPlusClientError(error_info)
        else:
            self._persistent_message_receiver_state = MessageReceiverState.STARTED
            self._flow_stopped = False

    def _do_subscribe(self, topic_subscription):
        # """method to subscribe"""
        if self._flow_p.value is None:
            logger.warning("Flow Pointer is NULL")
            return
        dispatch_info = _PersistentMessageReceiver.SolClientFlowCreateRxCallbackFuncInfo(
            ctypes.c_uint32(SOLCLIENT_DISPATCH_TYPE_CALLBACK), self._flow_msg_callback_func_routine,
            py_object(self), c_void_p(None))
        return_code = flow_topic_subscribe_with_dispatch(self._flow_p, topic_subscription, dispatch_info)
        if return_code == SOLCLIENT_OK:
            self._topic_dict[topic_subscription] = True
        elif return_code == SOLCLIENT_FAIL and len(topic_subscription) > 250:
            logger.warning("%s, name is %d bytes", TOPIC_NAME_TOO_LONG, len(topic_subscription))
            raise PubSubPlusClientError(message=f'{TOPIC_NAME_TOO_LONG}, name is {len(topic_subscription)} bytes')
        else:
            logger.warning('%s %s. Status code: %d',
                           UNABLE_TO_SUBSCRIBE_TO_TOPIC, topic_subscription, return_code)  # pragma: no cover
            raise PubSubPlusClientError(message=f'{UNABLE_TO_SUBSCRIBE_TO_TOPIC} {topic_subscription}. '
                                                f'Status code: {return_code}, with reason : '
                                                f'{last_error_info(return_code, " subscription")}'
                                        )  # pragma: no cover

    def _do_unsubscribe(self, topic_subscription):
        # """method to unsubscribe"""
        if self._flow_p.value is None:
            logger.warning("Flow Pointer is NULL")
            return
        dispatch_info = _PersistentMessageReceiver. \
            SolClientFlowCreateRxCallbackFuncInfo(ctypes.c_uint32(SOLCLIENT_DISPATCH_TYPE_CALLBACK),
                                                  self._flow_msg_callback_func_routine, py_object(self), c_void_p(None))

        return_code = flow_topic_unsubscribe_with_dispatch(self._flow_p, topic_subscription, dispatch_info)
        if return_code == SOLCLIENT_OK:
            logger.debug('Unsubscribed [%s]', topic_subscription)
            if topic_subscription in self._topic_dict:
                del self._topic_dict[topic_subscription]
        else:
            logger.warning(last_error_info(return_code, "unsubscribe"))  # pragma: no cover
            raise PubSubPlusClientError(message=f'{UNABLE_TO_UNSUBSCRIBE_TO_TOPIC} {topic_subscription}. '
                                                f'Status code: {return_code}')  # pragma: no cover

    def __is_eligible_for_termination(self):
        if self._persistent_message_receiver_state == MessageReceiverState.TERMINATING:
            logger.warning('Message receiver termination is in-progress')
            return False
        elif self._persistent_message_receiver_state == MessageReceiverState.TERMINATED:
            logger.warning('Message receiver already terminated')
            return False
        return True

    def __is_message_service_connected(self):
        # """Method to validate message service is connected or not"""
        if not self._messaging_service.is_connected:
            self._persistent_message_receiver_state = MessageReceiverState.NOT_STARTED
            logger.debug('[%s] is %s. MessagingService NOT connected', PersistentMessageReceiver.__name__,
                         MessageReceiverState.NOT_STARTED.name)
            raise IllegalStateError(RECEIVER_CANNOT_BE_STARTED_EXCEPTION_MESSAGE)
        return True

    def __is_receiver_started(self) -> bool:
        # """Method to validate receiver is properly started or not"""
        self.__is_message_service_connected()
        if self._persistent_message_receiver_state == MessageReceiverState.NOT_STARTED or \
                self._persistent_message_receiver_state == MessageReceiverState.STARTING:
            raise IllegalStateError(RECEIVER_NOT_STARTED)
        if self._persistent_message_receiver_state == MessageReceiverState.TERMINATING or \
                self._persistent_message_receiver_state == MessageReceiverState.TERMINATED:
            raise IllegalStateError(RECEIVER_TERMINATED)
        if self._persistent_message_receiver_state != MessageReceiverState.STARTED:
            raise IllegalStateError(RECEIVER_NOT_STARTED)
        logger.debug('[%s] %s', PersistentMessageReceiver.__name__, MessageReceiverState.STARTED.name)
        return True
