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
This module contains classes and functions for accessing the API logs.
"""
# pylint: disable = missing-function-docstring
import ctypes
import enum
import logging
from ctypes import c_char_p, c_int
from typing import Dict, Any

import solace
from solace.messaging.config.solace_message_constants import CCSMP_SUB_CODE, CCSMP_INFO_SUB_CODE, \
    CCSMP_INFO_CONTENTS, CCSMP_CALLER_DESC, CCSMP_RETURN_CODE

logger = logging.getLogger('solace.messaging.core.api')


class SolClientLogLevel(enum.Enum):  # pylint: disable=missing-class-docstring
    # enum class to define the SolClient log levels for mapping with the python layers
    SOLCLIENT_LOG_EMERGENCY = 0
    SOLCLIENT_LOG_ALERT = 1
    SOLCLIENT_LOG_CRITICAL = 2
    SOLCLIENT_LOG_ERROR = 3
    SOLCLIENT_LOG_WARNING = 4
    SOLCLIENT_LOG_NOTICE = 5
    SOLCLIENT_LOG_INFO = 6
    SOLCLIENT_LOG_DEBUG = 7


log_level = {"DEBUG": SolClientLogLevel.SOLCLIENT_LOG_DEBUG.value, "INFO": SolClientLogLevel.SOLCLIENT_LOG_INFO.value,
             "WARNING": SolClientLogLevel.SOLCLIENT_LOG_WARNING.value,
             "ERROR": SolClientLogLevel.SOLCLIENT_LOG_ERROR.value,
             "CRITICAL": SolClientLogLevel.SOLCLIENT_LOG_CRITICAL.value}


def set_core_api_log_level(level):
    # """function to set the core api log levels
    # Args:
    #     level: str value, holds the log level
    # """
    level = log_level.get(level.upper(), SolClientLogLevel.SOLCLIENT_LOG_WARNING.value)
    solace.CORE_LIB.solClient_log_setFilterLevel(0, level)


def set_log_file(log_file):
    if log_file is None:
        file_p = ctypes.c_char_p(None)
    else:
        file_p = ctypes.c_char_p(log_file.encode())
    solace.CORE_LIB.solClient_log_setFile(file_p)


def last_error_info(status_code: int = None, caller_desc: str = None) -> Dict[str, Any]:
    # """ Fetch the last C core API error and format an exception.
    # :param status_code: core api response code
    # :param caller_desc: description about the caller of this log
    # :return: KVP of core api error details
    # """
    solace.CORE_LIB.solClient_returnCodeToString.restype = c_char_p
    solace.CORE_LIB.solClient_returnCodeToString.argtypes = [c_int]
    solace.CORE_LIB.solClient_subCodeToString.restype = c_char_p
    solace.CORE_LIB.solClient_subCodeToString.argtypes = [c_int]
    solace.CORE_LIB.solClient_getLastErrorInfo.restype = ctypes.POINTER(SolClientErrorInfo)
    err_info = solace.CORE_LIB.solClient_getLastErrorInfo()
    return_code_str = solace.CORE_LIB.solClient_returnCodeToString(
        status_code) if status_code is not None else ''
    sub_code_str = solace.CORE_LIB.solClient_subCodeToString(err_info.contents.subCode)
    core_api_error = {CCSMP_CALLER_DESC: caller_desc, CCSMP_RETURN_CODE: return_code_str.decode(),
                      CCSMP_SUB_CODE: sub_code_str.decode(),
                      CCSMP_INFO_SUB_CODE: err_info.contents.subCode,
                      CCSMP_INFO_CONTENTS: ' '.join(err_info.contents.errorInfo.decode().split())}
    return core_api_error


class SolClientErrorInfo(ctypes.Structure):  # pylint: disable=too-few-public-methods, missing-class-docstring
    # """ Conforms to solClient_errorInfo_t """
    _fields_ = [
        ("subCode", c_int),
        ("response_code", c_int),
        ("errorInfo", ctypes.c_char * 256)  # array of bytes that is NULL-terminated
    ]
