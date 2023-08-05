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
# this is an internal utility module, used by implementors of the API. # pylint: disable=missing-function-docstring
# pylint: disable=protected-access
import ctypes
from ctypes import c_char_p, sizeof, byref, POINTER
from functools import reduce

import solace
from solace.messaging.config.sol_constants import MAX_SESSION_PROPS


def session_create(arr, context_p, session_p, session_func_info):
    # """Creates a new Session within a specified Context, The session properties are supplied as an array
    # of name/value pointer pairs in the form of strings and if the values are not provided
    # the default values will be provided
    # Args:
    #     arr: c-types character array
    #     context_p: the context pointer
    #     session_p: session pointer
    #     session_func_info: the session function info pointer in bytes
    #
    # Returns:
    #     the created session
    # """
    return solace.CORE_LIB.solClient_session_create(ctypes.cast(arr, POINTER(c_char_p)), context_p, byref(session_p),
                                                    byref(session_func_info), sizeof(session_func_info))


def session_connect(session_p):
    # """function to connect to the session
    # Args:
    #     session_p:  the session pointer
    #
    # Returns:
    #     returns the connected session status
    # """
    return solace.CORE_LIB.solClient_session_connect(session_p)


def session_disconnect(session_p):
    # """function to disconnect the specified session, Once disconnected, topics/subscriptions can no longer be
    # added or removed from the Session, messages can no longer be received for the Session, and messages
    # cannot be sent to the Session, But the Session definition remains, and the Session can be connected again
    # (using solClient_session_connect())
    # Args:
    #     session_p: the session pointer
    #
    # Returns:
    #     returns the disconnected session status
    # """
    return solace.CORE_LIB.solClient_session_disconnect(session_p)


def session_destroy(session_p):
    # """function to destroy a session which is already created
    # Args:
    #     session_p: session pointer
    #
    # Returns:
    #     returns the session destroyed status
    # """
    return solace.CORE_LIB.solClient_session_destroy(byref(session_p))


def session_force_failure(session_p):
    # """function to force failure the session
    # Args:
    #     session_p: session pointer
    #
    # Returns:
    #     returns the force disconnected status
    # """
    return solace.CORE_LIB._solClient_session_forceFailure(session_p, 0)


def context_destroy(context_p):
    # """function for destroying the context
    #
    # Args:
    #     context_p: context pointer
    # """
    return solace.CORE_LIB.solClient_context_destroy(ctypes.byref(context_p))


def prepare_array(config):
    props_list = list(reduce(lambda x, y: x + y, config.items()))
    props_list = [e.encode() for e in props_list]
    props_list.append(c_char_p(None))  # add NULL at the end of array
    return (c_char_p * (2 * MAX_SESSION_PROPS + 1))(*props_list)
