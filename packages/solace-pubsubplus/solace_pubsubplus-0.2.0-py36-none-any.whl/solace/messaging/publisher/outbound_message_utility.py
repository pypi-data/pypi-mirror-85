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
from ctypes import c_uint32, c_char_p, byref

import solace
from solace.messaging.config import sol_constants

logger = logging.getLogger('solace.messaging.core.api')


def close_map(map_p):
    # Finish a map or stream. This action makes the opaque container pointer invalid and fixes the
    # structured data in memory.
    return solace.CORE_LIB.solClient_container_closeMapStream(byref(map_p))


def container_add_int64(map_p, property_value, property_key):
    # """function for adding 64 bit integer value to the container"""
    solace.CORE_LIB.solClient_container_addInt64(map_p, property_value,
                                                 c_char_p(property_key.encode(sol_constants.ENCODING_TYPE)))


def container_add_string(map_p, property_value, property_key):
    # """function for adding the string in the container"""
    solace.CORE_LIB.solClient_container_addString(map_p, property_value,
                                                  c_char_p(property_key.encode(sol_constants.ENCODING_TYPE)))


def container_add_byte_array(map_p, property_value, property_key):
    # """function for adding the byte array in the container"""
    solace.CORE_LIB.solClient_container_addByteArray(map_p, property_value, c_uint32(len(property_value)),
                                                     property_key.encode(sol_constants.ENCODING_TYPE))


def get_next_field(map_p, sol_client_field_t, key_p):
    # """function to get the next field"""
    return solace.CORE_LIB.solClient_container_getNextField(map_p, ctypes.byref(sol_client_field_t),
                                                            ctypes.sizeof(sol_client_field_t),
                                                            ctypes.byref(key_p))


def set_correlation_tag_ptr(msg_p, correlation_tag):
    # """
    #     Given a msg_p, set the Correlation Tag to the given pointer. The Correlation Tag is a
    #     local reference used by applications generating Guaranteed messages. Messages that are
    #     sent in either PERSISTENT or non-PERSISTENT mode can set the Correlation Tag,
    #     which is returned when the ::SOLCLIENT_SESSION_EVENT_ACKNOWLEDGEMENT event
    #     is later received. The solClient_session_eventCallbackInfo structured returned with the
    #     event contains a (void *) correlation_p which will be the same pointer the application
    #     initializes with this method.
    #     Important: <b>The Correlation Tag is not included in the
    #     transmitted message and is only used with the local API</b>.
    #
    #     This function is provided for high-performance applications that
    #     must be aware that the data referenced cannot be modified until the send
    #     operation completes.
    # """
    return solace.CORE_LIB.solClient_msg_setCorrelationTagPtr(msg_p,
                                                              ctypes.c_char_p(correlation_tag),
                                                              c_uint32(8))  # size is ignored


def add_message_properties(configuration, solace_message):
    from solace.messaging.publisher._impl._outbound_message import SolaceMap

    user_props = set(list(configuration.keys())) - set(
        list(solace_message.message_properties_mapping.keys()))
    # set the solace defined message properties
    solace_message.handle_message_properties(configuration)
    solace_map_dup = SolaceMap.get_map_from_message(solace_message)
    if solace_map_dup is None:
        solace_map_dup = SolaceMap(solace_message)
    for key, value in configuration.items():
        # only add user defined props skip the  properties defined by Solace
        if key in user_props:
            SolaceMap.add_user_props_to_container(solace_map_dup.map_p, key, value)
