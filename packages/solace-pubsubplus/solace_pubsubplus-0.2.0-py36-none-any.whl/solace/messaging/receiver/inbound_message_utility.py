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


# module contains the class and functions which actually make the call to ccsmp #pylint:disable=missing-module-docstring
# this is an internal utility module, used by implementors of the API.
# pylint: disable=missing-function-docstring
import ctypes
import logging
from ctypes import c_char_p, sizeof, byref

import solace
from solace.messaging.config.sol_constants import SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM, SOLCLIENT_OK, \
    SOLCLIENT_PROVISION_FLAGS_WAITFORCONFIRM
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError

logger = logging.getLogger('solace.messaging.core.api')


def topic_subscribe_with_dispatch(session_p, subscription, dispatch_info):
    # """A function to subscribe a topic with dispatch.
    # Args:
    #     session_p: session pointer
    #     subscription: topic subscription
    #     dispatch_info: topic dispatch info
    # """
    return solace.CORE_LIB.solClient_session_topicSubscribeWithDispatch(
        session_p, ctypes.c_int(SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM),
        c_char_p(subscription.encode()), byref(dispatch_info), sizeof(dispatch_info))


def topic_unsubscribe_with_dispatch(session_p, subscription, dispatch_info):
    # """function to unsubscribe a topic with dispatch
    # Args:
    #     session_p: session pointer
    #     subscription: the topic subscription
    #     dispatch_info: topic dispatch info
    # """
    return solace.CORE_LIB.solClient_session_topicUnsubscribeWithDispatch(
        session_p, ctypes.c_int(SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM), c_char_p(subscription.encode()),
        byref(dispatch_info), ctypes.sizeof(dispatch_info))


def get_message_id(msg_p):
    msg_id = ctypes.c_uint64()
    return_code = solace.CORE_LIB.solClient_msg_getMsgId(msg_p, byref(msg_id))
    if return_code != SOLCLIENT_OK:
        raise PubSubPlusClientError('Unable to get message id')
    return msg_id


def acknowledge_message(flow_p, msg_id):
    return solace.CORE_LIB.solClient_flow_sendAck(flow_p, msg_id)


def pause(flow_p):
    # """"
    #  Closes the receiver on the specified Flow. This method will close the Flow
    #  window to the appliance so further messages will not be received until
    #  solClient_flow_start() is called. Messages in transit when this method is
    #  called will still be delivered to the application. So the application must
    #  expect that the receive message callback can be called even after calling
    #  solClient_flow_stop(). The maximum number of messages that may be
    #  in transit at any one time is controlled by ::SOLCLIENT_FLOW_PROP_WINDOWSIZE
    #  and ::SOLCLIENT_FLOW_PROP_MAX_UNACKED_MESSAGES (see solClient_flow_setMaxUnAcked()).
    #
    #  A Flow can be created with the window closed by setting the Flow property ::SOLCLIENT_FLOW_PROP_START_STATE
    #  to ::SOLCLIENT_PROP_DISABLE_VAL. When a Flow is created in this way, messages will not be received
    #  on the Flow until after ::solClient_flow_start() is called.
    # """
    return solace.CORE_LIB.solClient_flow_stop(flow_p)


def resume(flow_p):
    # """
    #     Opens the receiver on the specified Flow. This method opens the Flow window
    #     to the appliance so further messages can be received. For browser flows (::SOLCLIENT_FLOW_PROP_BROWSER),
    #     applications have to call the function to get more messages.
    #
    #     A Flow may be created with the window closed by setting the Flow property ::SOLCLIENT_FLOW_PROP_START_STATE
    #     to ::SOLCLIENT_PROP_DISABLE_VAL. When a Flow is created in this way, messages will not be received
    #     on the Flow until after ::solClient_flow_start() is called.
    # Args:
    #     flow_p ():
    #
    # Returns:
    #
    # """
    return solace.CORE_LIB.solClient_flow_start(flow_p)


def flow_topic_subscribe_with_dispatch(flow_p, subscription, dispatch_info):
    # """function to subscribe a topic with dispatch
    # Args:
    #     flow_p: flow pointer
    #     subscription: topic subscription
    #     dispatch_info: topic dispatch info
    # """
    return solace.CORE_LIB.solClient_flow_topicSubscribeWithDispatch(
        flow_p, ctypes.c_int(SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM),
        c_char_p(subscription.encode()), byref(dispatch_info), sizeof(dispatch_info))


def flow_topic_unsubscribe_with_dispatch(flow_p, subscription, dispatch_info):
    # """function to unsubscribe a topic with dispatch
    # Args:
    #     flow_p: flow pointer
    #     subscription: topic subscription
    #     dispatch_info: topic dispatch info
    # """
    return solace.CORE_LIB.solClient_flow_topicUnsubscribeWithDispatch(
        flow_p, ctypes.c_int(SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM),
        c_char_p(subscription.encode()), byref(dispatch_info), sizeof(dispatch_info))


def end_point_provision(props, session_p):
    return solace.CORE_LIB.solClient_session_endpointProvision(ctypes.cast(props, ctypes.POINTER(c_char_p)),
                                                               session_p,
                                                               ctypes.c_int(SOLCLIENT_PROVISION_FLAGS_WAITFORCONFIRM),
                                                               ctypes.c_char_p(), c_char_p(),
                                                               ctypes.c_int(0))
