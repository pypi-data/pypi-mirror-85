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
# this is an internal utility module, used by implementors of the API. #pylint:disable=missing-function-docstring
import ctypes
from ctypes import c_int, byref

import solace


def get_transmitted_statistics(session_p, arr):
    # """function to get the transmitted statistics
    # Args:
    #     session_p: session pointer
    #     arr: c-types integer array
    # """
    return solace.CORE_LIB.solClient_session_getTxStats(session_p, arr, c_int(len(arr)))


def get_received_statistics(session_p, arr):
    # """function to get the received statistics
    # Args:
    #     session_p: session pointer
    #     arr: c-types integer array
    # """
    return solace.CORE_LIB.solClient_session_getRxStats(session_p, arr, c_int(len(arr)))


def get_transmitted_statistic(session_p, index):
    # """function to get the transmitted statistic
    #     Args:
    #         session_p: session pointer
    #         index(int): statistic index value in array
    #     """
    stat = ctypes.c_uint64()
    solace.CORE_LIB.solClient_session_getTxStat(session_p, index, byref(stat))
    return stat.value


def get_received_statistic(session_p, index: int):
    # """
    # function to get the received statistic
    #
    # Args:
    #     session_p ():
    #     index (int):
    #
    # Returns (int):
    #
    # """

    stat = ctypes.c_uint64()
    solace.CORE_LIB.solClient_session_getRxStat(session_p, index, byref(stat))
    return stat.value


def reset_statistics(session_p):
    # """function for resetting the statistics"""
    return solace.CORE_LIB.solClient_session_clearStats(session_p)
