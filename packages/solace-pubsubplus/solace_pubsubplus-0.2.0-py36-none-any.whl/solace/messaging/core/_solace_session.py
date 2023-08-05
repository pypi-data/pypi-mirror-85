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


# """   # pylint: disable=missing-module-docstring
# Module contains classes to interact with underlying c api
# """
import ctypes
import datetime
import enum
import logging
import os
import platform
import threading
import weakref
from ctypes import Structure, pointer, byref, sizeof, POINTER, util
from ctypes import cdll, py_object, c_void_p, c_char_p, c_int
from functools import reduce
from os.path import dirname
from queue import Queue
from struct import calcsize

import solace
from solace.messaging.config.ccsmp_property_mapping import CCSMP_SESSION_PROP_MAPPING, default_props
from solace.messaging.config.sol_constants import SOLCLIENT_CALLBACK_OK, SOLCLIENT_LOG_DEFAULT_FILTER, \
    SOLCLIENT_OK, SOLCLIENT_SESSION_EVENT_RECONNECTING_NOTICE, \
    SOLCLIENT_SESSION_EVENT_RECONNECTED_NOTICE, SOLCLIENT_SESSION_EVENT_CAN_SEND, SOLCLIENT_SESSION_EVENT_DOWN_ERROR, \
    SOLCLIENT_SESSION_EVENT_CONNECT_FAILED_ERROR, SOLCLIENT_SESSION_EVENT_UP_NOTICE, \
    SOLCLIENT_SESSION_EVENT_ACKNOWLEDGEMENT, SOLCLIENT_SESSION_EVENT_REJECTED_MSG_ERROR, SolClientSubCode
from solace.messaging.config.solace_message_constants import CCSMP_SUB_CODE, UNABLE_TO_LOAD_SOLCLIENT_LIBRARY, \
    CCSMP_SUB_CODE_OK, SESSION_FORCE_DISCONNECT, \
    ESTABLISH_SESSION_ON_HOST, CCSMP_SUB_CODE_LOGIN_FAILURE, CCSMP_SUB_CODE_FAILED_TO_LOAD_TRUST_STORE, \
    FAILED_TO_LOAD_TRUST_STORE, CCSMP_SUB_CODE_UNRESOLVED_HOST, UNRESOLVED_SESSION, \
    FAILED_TO_LOADING_CERTIFICATE_AND_KEY, CCSMP_SUB_CODE_FAILED_LOADING_CERTIFICATE_AND_KEY, \
    BAD_CREDENTIALS, CCSMP_SUBCODE_UNTRUSTED_CERTIFICATE, UNTRUSTED_CERTIFICATE_MESSAGE, CCSMP_INFO_SUB_CODE
from solace.messaging.config.solace_properties import transport_layer_security_properties, transport_layer_properties
from solace.messaging.core._core_api_utility import context_destroy, session_disconnect, session_force_failure, \
    session_destroy, session_connect, session_create, prepare_array
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError, \
    ServiceUnreachableError, AuthenticationError, MessageRejectedByBrokerError, \
    MessageDestinationDoesNotExistError
from solace.messaging.messaging_service import _ServiceEvent
from solace.messaging.solace_logging.core_api_log import last_error_info
from solace.messaging.utils.solace_utilities import Util

logger = logging.getLogger('solace.messaging.core')


class _SolaceApiLibrary:  # pylint: disable=missing-class-docstring, missing-function-docstring
    # """
    # Singleton class to load dll
    # """
    _core_lib = None  # it is a protected member, and is used for holding the C Library
    _instance = None  # it is a protected member, and it holds the instance of the _SolaceApiLibrary super class
    _global_config = None

    def __new__(cls, *args, **kwargs):
        """
        return: instance of Solace Library
        """
        if cls._instance is None:
            cls._instance = super(_SolaceApiLibrary, cls).__new__(cls, *args, **kwargs)
            cls._core_lib = cls.__load_core_library()
            cls.__init_api()
        return cls._instance

    @staticmethod
    def _get_shared_lib_default_path(platform_os: str) -> str:
        # used to find shared_lib_config_default path based on platform
        # returns the default native library path or None if no matching
        # platform is found
        void_pointer_struct_char = 'P'
        is32bit = (calcsize(void_pointer_struct_char) * 8) == 32
        # get relative path of package installed library
        path_default_base = os.path.join(dirname(dirname(__file__)), "lib")
        lib_arch_32bit = {"Windows": "32"}
        lib_arch_64bit = {"Linux": "-x86_64", "Darwin": "-x86_64", "Windows": "-amd64"}
        lib_platform_name = {"Linux": "linux", "Darwin": "macosx", "Windows": "win"}
        lib_arch = lib_arch_32bit if is32bit else lib_arch_64bit
        arch = lib_arch.get(platform_os, None)
        platform_name = lib_platform_name.get(platform_os, None)
        if arch is not None and platform_name is not None:
            return os.path.join(path_default_base, "%s%s" % (platform_name, arch))

        return None

    @staticmethod
    def __load_core_library():
        # """ method to load dll based on OS
        #     Raises:
        #         PubSubPlusClientError: if library is missing
        # """
        # shared_lib_config_optional holds the key:value pairs for the the names
        # of shared libraries that can be used for accessing shared libraries in
        # user-customized locations. shared_lib_config_optional is different
        # from shared_lib_config_default because of different methods are used
        # to find the shared library in each case. util.find_library is required
        # to find custom installations of a shared library since it uses the
        # PATH on Windows or the LD_LIBRARY_PATH on Linux to find the custom
        # installation, and in Linux the shared library name passed to the
        # find_library() function must not have the 'lib' prefix or '.so'
        # suffix. In contrast, the default installation of the shared library
        # is within this package so it is always in the same place. Therefore,
        # the relative path from this file to the location of the default
        # installation of the shared library can be used to find it and load
        # it.

        shared_lib_config_optional = {"Linux": 'solclient', "Windows": 'libsolclient.dll',
                                      "Darwin": 'libsolclient.dylib'}

        # get the shared library name for this platform
        shared_lib_name_optional = shared_lib_config_optional.get(platform.system(), None)
        if shared_lib_name_optional:
            # search the PATH variable on Windows and the LD_LIBRARY_PATH on
            # Linux for a custom installation of a Solace CCSMP shared library
            shared_lib_path_optional = util.find_library(shared_lib_name_optional)
            if shared_lib_path_optional is not None:
                # if the custom shared library was found, load and return it
                try:
                    return cdll.LoadLibrary(shared_lib_path_optional)  # pragma: no cover
                except PubSubPlusClientError as exception:  # pragma: no cover
                    logger.info('%s from custom location [%s]. Exception: %s', UNABLE_TO_LOAD_SOLCLIENT_LIBRARY,
                                shared_lib_path_optional, str(exception))
                # if a custom installation of a CCSMP shared library was not
                # found, assume that the default shared library included in the
                # distribution should be loaded
            shared_lib_config_default = {"Linux": 'libsolclient.so', "Windows": 'libsolclient.dll',
                                         "Darwin": 'libsolclient.dylib'}
            # get the shared library name for this platform
            shared_lib_name_default = shared_lib_config_default.get(platform.system(), None)
            if shared_lib_name_default:
                # join the relative path from this file to the shared
                # library file
                # prepend the current directory path to the relative path
                # from the this file to the shared library file
                shared_lib_path_default = _SolaceApiLibrary._get_shared_lib_default_path(platform.system())
                if shared_lib_path_default is not None:
                    shared_lib_path_default = os.path.join(
                        _SolaceApiLibrary._get_shared_lib_default_path(platform.system()),
                        shared_lib_name_default)
                    if shared_lib_path_default is not None:
                        try:
                            # if the default installation was found, load and return it
                            return cdll.LoadLibrary(shared_lib_path_default)
                        except Exception as exception:  # pragma: no cover
                            logger.error('%s from [%s]. Exception: %s', UNABLE_TO_LOAD_SOLCLIENT_LIBRARY,
                                         shared_lib_path_default, str(exception))
                            raise PubSubPlusClientError(message=f'{UNABLE_TO_LOAD_SOLCLIENT_LIBRARY} '
                                                                f'from [{shared_lib_path_default}]. '
                                                                f'Exception: {exception}') from exception
        # if neither the custom nor default location of the shared library
        # contain the required shared library, throw the relevant error and
        logger.error(UNABLE_TO_LOAD_SOLCLIENT_LIBRARY)  # pragma: no cover
        raise PubSubPlusClientError(message=UNABLE_TO_LOAD_SOLCLIENT_LIBRARY)  # pragma: no cover

    @classmethod
    def __init_api(cls):
        # ssl & crypt config begins
        # if cls._global_config is None:
        #     location = cls._get_shared_lib_default_path(platform.system())
        #     ssl_crypt = {"Linux": {"GLOBAL_CRYPTO_LIB": SOLCLIENT_GLOBAL_PROP_DEFAULT_CRYPTO_LIB_UNIX,
        #                            "GLOBAL_SSL_LIB": SOLCLIENT_GLOBAL_PROP_DEFAULT_SSL_LIB_UNIX},
        #                  "Windows": {"GLOBAL_CRYPTO_LIB": SOLCLIENT_GLOBAL_PROP_DEFAULT_CRYPTO_LIB_WINDOWS,
        #                              "GLOBAL_SSL_LIB": SOLCLIENT_GLOBAL_PROP_DEFAULT_SSL_LIB_WINDOWS},
        #                  "Darwin": {"GLOBAL_CRYPTO_LIB": SOLCLIENT_GLOBAL_PROP_DEFAULT_CRYPTO_LIB_MACOSX,
        #                             "GLOBAL_SSL_LIB": SOLCLIENT_GLOBAL_PROP_DEFAULT_SSL_LIB_MACOSX}}
        #     lib = dict()
        #     for prop, file in ssl_crypt[platform.system()].items():
        #         lib[prop] = os.path.join(location, file)
        #
        #     cls._global_config = prepare_array(lib)
        # log setup begins
        cls._core_lib.solClient_log_setFile(ctypes.c_char_p(None))
        cls._core_lib.solClient_initialize(SOLCLIENT_LOG_DEFAULT_FILTER, cls._global_config)
        cls.__set_version(cls._core_lib)
        cls._core_lib.solClient_log_setFilterLevel(0, 1)

    @property
    def solclient_core_library(self):
        # """
        # property to return the dll
        # return: Returns loaded dll
        # """
        return self._core_lib

    @staticmethod
    def __set_version(core_lib):
        # """ Get and Set version using Core lib """

        class SolClientVersionInfo(Structure):  # pylint: disable=too-few-public-methods
            """ Conforms to SolClient_version_info """
            _fields_ = [
                ("version_p", c_char_p),
                ("dateTime_p", c_char_p),
                ("variant_p", c_char_p)
            ]

        version_pointer = pointer(SolClientVersionInfo())
        get_result = core_lib.solClient_version_get(byref(version_pointer))
        if get_result == SOLCLIENT_OK:
            app_name = Util.read_key_from_config('solace_props', 'solace.messaging.client.app')
            core_api_name = 'C API'

            core_api_version = version_pointer.contents.version_p.decode("utf-8")
            core_api_date = version_pointer.contents.dateTime_p.decode("utf-8")
            core_api_variant = version_pointer.contents.variant_p.decode("utf-8")

            time_stamp = datetime.date.today().strftime("%b %d %Y %H:%M:%S")

            new_version = f'{app_name} / {core_api_name} {core_api_version}'
            new_date = f'{app_name} {time_stamp} / {core_api_name} {core_api_date}'
            new_variant = f'{app_name} / {core_api_variant}'

            updated_details = SolClientVersionInfo(c_char_p(new_version.encode('utf-8')),
                                                   c_char_p(new_date.encode('utf-8')),
                                                   c_char_p(new_variant.encode('utf-8')))

            return_code = core_lib._solClient_version_set(byref(updated_details))  # pylint: disable=protected-access
            if return_code != SOLCLIENT_OK:  # pragma: no cover
                logger.warning('Unable to set version')
        else:  # pragma: no cover
            logger.warning('Unable to set version')


def context_cleanup(context_pointer):  # pylint: disable=missing-function-docstring
    # """function for cleaning up the context"""
    try:
        if context_pointer and context_pointer.value is not None:
            context_destroy(context_pointer)
    except PubSubPlusClientError as exception:  # pragma: no cover
        logger.error(exception)


class _SolaceApiContext:  # pylint: disable=missing-class-docstring, missing-function-docstring
    # """
    # Class to create context
    # """

    def __init__(self):
        """
        return: instance of Solace context
        """
        self.__context_p = c_void_p(None)  # it is a protected member, which holds the context pointer of
        # type (ctypes)
        return_code = self._create_context()
        self._finalizer = weakref.finalize(self, context_cleanup, self.__context_p)
        if return_code != SOLCLIENT_OK:  # pragma: no cover
            logger.warning("Failed to create solace context")
            raise PubSubPlusClientError("Failed to create solace context")

    def _create_context(self):
        # """ Method to create context"""

        class SolClientContextCreateRegisterFdFuncInfo \
                    (Structure):  # pylint: disable=too-few-public-methods, trailing-whitespace
            # """ Conforms to solClient_context_createRegisterFdFuncInfo_t
            #  .. _class solClient_context_createRegisterFdFuncInfo:
            #
            #  Function is set on a per-Context basis. Providing these functions is optional. If provided, both
            #  function information for file descriptor registration and file descriptor un-registration functions.
            #  Tht be non-NULL, and if not provided, both must be NULL.
            #
            # These functions are used when the application wants to own event generation, and they supply file
            # descriptor events to the API. Such applications typically want to poll several different devices,
            # of which the API is only one. When these functions are provided, the API does not manage its own
            # devices. Instead, when a device is created, the provided 'register' function is called to register the
            # device file descriptor for read and/or write events. It is the responsibility of the application to
            # call back into API when the appropriate event occurs on the device file descriptor. The API callback is
            # provided to the register function (see ::solClient_context_registerFdFunc_t). If this interface is
            # chosen, the application <b>must</b> also call solClient_context_timerTick() at regular intervals.
            #
            #  Normally these are not used, and the API owns event registrations. If an internal Context thread is used
            #  by enabling ::SOLCLIENT_CONTEXT_PROP_CREATE_THREAD
            #  (see also ::SOLCLIENT_CONTEXT_PROPS_DEFAULT_WITH_CREATE_THREAD),
            #  the API takes care of all devices and timers and no action is required by the application.
            #  If the internal thread is
            #  not enabled, the application must call solClient_context_processEvents() to provide scheduling time to
            #   the API.
            #
            # When the API owns event registrations, it also provides file descriptor register/unregister service to
            # the application. solClient_context_registerForFdEvents() and solClient_context_unregisterForFdEvents()
            # can be used by applications to pass file descriptors to the API for managing, keeping event generation
            # localized to the internal thread or the thread that calls solClient_context_processEvents(). """
            _fields_ = [
                ("reg_fd_func_p", c_void_p),
                ("unreg_fd_func_p", c_void_p),
                ("user_p", c_void_p)
            ]

        class SolClientContextCreateFuncInfo(Structure):  # pylint: disable=too-few-public-methods
            # """ Conforms to solClient_context_createFuncInfo_t"""
            _fields_ = [
                ("reg_fd_info", SolClientContextCreateRegisterFdFuncInfo)
            ]

        # create native context
        context_props = pointer(c_char_p.in_dll(self.solclient_core_library,
                                                "_solClient_contextPropsDefaultWithCreateThread"))
        context_func_info = SolClientContextCreateFuncInfo()
        context_func_info.reg_fd_info = \
            SolClientContextCreateRegisterFdFuncInfo(None, None, None)  # pylint: disable=attribute-defined-outside-init
        return_code = self.solclient_core_library.solClient_context_create(context_props, byref(self.__context_p),
                                                                           byref(context_func_info),
                                                                           sizeof(context_func_info))
        return return_code

    @property
    def context_p(self):
        # """
        #     Get underlying c api pointer
        #     return:Returns contexts pointer
        # """
        return self.__context_p

    @property
    def solclient_core_library(self):
        # """
        # property to return the dll
        # return: Returns loaded dll
        # """
        return _SolaceApiLibrary().solclient_core_library


class SolClientServiceEventCallbackInfo(Structure):  # pylint: disable=too-few-public-methods, missing-class-docstring
    # """ Conforms to solClient_session_eventCallbackInfo_t """
    # this is a C structure incorporated using c-types module for providing the session event callback info
    _fields_ = [
        ("session_event", ctypes.c_int32),
        ("response_code", ctypes.c_uint32),
        ("info_p", c_char_p),
        ("correlation_p", c_void_p)
    ]


class MessagingServiceState(enum.Enum):  # pylint: disable=too-few-public-methods, missing-class-docstring
    NOT_CONNECTED = -1
    CONNECTING = 0
    CONNECTED = 1
    RECONNECTING = 2
    RECONNECTED = 3
    DISCONNECTED = 4
    DOWN = 5


def _session_cleanup(session_pointer):  # pylint: disable=missing-function-docstring
    try:
        if session_pointer:
            session_destroy(session_pointer)
    except PubSubPlusClientError as exception:  # pragma: no cover
        logger.error(exception)


class _SolaceApi:  # pylint: disable=too-many-instance-attributes, missing-class-docstring, missing-function-docstring
    # """
    # class to interact with underlying C core functionality
    # """
    _event_callback = None  # this is an protected member, and is used for event callback
    _msg_callback = None  # this is an protected member, and is used for message callback
    # _log_callback = None
    #  solclient_session_event_callback_info_pt ia an public member which is used for holding
    #  the pointer object of SolClientServiceEventCallbackInfo
    solclient_session_event_callback_info_pt = POINTER(SolClientServiceEventCallbackInfo)
    # protected member, holds c-type event callback function type
    _event_callback_func_type = ctypes.CFUNCTYPE(ctypes.c_int, c_void_p,
                                                 solclient_session_event_callback_info_pt,
                                                 py_object)
    _msg_callback_func_type = ctypes.CFUNCTYPE(ctypes.c_int, c_void_p, c_void_p, py_object)

    # it is an protected member, holds the message callback function type of c-types

    def __init__(self):
        """
        This method is used to initialize _SolaceApiContext() for creating context
        """
        self._core_lib = solace.CORE_LIB
        self._core_lib.solClient_returnCodeToString.restype = c_char_p
        self._core_lib.solClient_returnCodeToString.argtypes = [c_int]
        self._session_func_info = None
        self._context = _SolaceApiContext()
        self._context_p = self._context.context_p
        self._attempt_listeners = set()
        self._reconnection_listeners = set()
        self._service_interruption_listeners = set()
        self._connection_can_listen = threading.Event()  # common for event 12,13,1
        self._listener_queue = None  # common for event 12,13,1
        self._host = None  # it holds the host value
        self._can_send_received = threading.Event()  # this sets the threading event based on the can send received
        self._messaging_service_state = MessagingServiceState.NOT_CONNECTED  # defines the msg service state
        self._can_listen = threading.Event()
        self._can_listen_to_ack = threading.Event()
        # this is a private member & is used for holding session pointer which is of c-types
        self.__session_p = c_void_p(None)
        self._finalizer = weakref.finalize(self, _session_cleanup, self.__session_p)
        self._can_receive = list()  # will have receiver's id to set can_receive_event
        self._can_peek = list()  # will have publisher's id to set can_peek_event
        self._state_change = list()  # will have receiver's id to set state_change_event

    @property
    def can_receive(self):
        return self._can_receive

    @property
    def can_peek(self):
        return self._can_peek

    @property
    def state_change(self):
        return self._state_change

    @property
    def service_interruption_listeners(self):
        return self._service_interruption_listeners

    @property
    def attempt_listeners(self):
        return self._attempt_listeners

    @property
    def reconnection_listeners(self):
        return self._reconnection_listeners

    @property
    def listener_queue(self):
        return self._listener_queue

    @listener_queue.setter
    def listener_queue(self, val: Queue):
        self._listener_queue = val

    @property
    def connection_can_listen(self):
        return self._connection_can_listen

    @property
    def can_send_received(self):
        return self._can_send_received

    @property
    def can_listen_to_ack(self):
        return self._can_listen_to_ack

    @property
    def can_listen(self):
        return self._can_listen

    def _session_connect(self) -> int:
        # """
        # connects to broker in  blocking mode
        #
        # Returns:
        #     int :  returns   the return code from do_connect() i.e (-1 to 8)
        # """
        return self.__do_connect()

    def session_disconnect(self) -> int:
        # """
        #  Disconnects the specified Session by the help of the C API solClient_session_disconnect,
        #  if the session is disconnected then the return code will be SOLCLIENT_OK else this method
        #  will raise exception.
        #
        # Returns:
        #     int :  returns  0 or -1
        #  Raises:
        #         PubSubPlusClientError: if we didn't receive 1 as return code
        # """
        self._core_lib.solClient_session_disconnect.argtypes = [c_void_p]

        return_code = session_disconnect(self.__session_p)
        if return_code != SOLCLIENT_OK:  # pragma: no cover
            logger.warning("Unable to disconnect session. Failure code: %d", return_code)
            raise PubSubPlusClientError(message=f"Unable to disconnect session. Failure code: {return_code}")

        # NOTE: Once after successful session disconnect, we're clearing __session_p object since we don't have
        # business of reconnecting the session again, but if we introduce re-connection mechanism inside
        # (actually RetryStrategy are wrapped inside C api) wrapper api then we can't assign None to __session_p
        self._messaging_service_state = MessagingServiceState.DISCONNECTED
        return return_code

    def session_force_disconnect(self) -> int:  # Instead use toxiproxy
        # """
        # function to disconnect with event broker. HIGH RISK: We should use this only for testing.
        # In ideal scenario, we won't FORCE DISCONNECT SESSION
        #
        # Returns:
        #     int :  returns  0 or -1
        #  Raises:
        #         PubSubPlusClientError: if we didn't receive 1 as return code
        # """
        self._core_lib.solClient_session_disconnect.argtypes = [c_void_p]
        return_code = session_force_failure(self.__session_p)
        if return_code != SOLCLIENT_OK:  # pragma: no cover
            logger.warning("Unable to FORCE disconnect service with  return code : %d", return_code)
            raise PubSubPlusClientError(message=f"Unable to FORCE disconnect service with  return code : "
                                                f"{return_code}")
        self._messaging_service_state = MessagingServiceState.DISCONNECTED
        logger.warning(SESSION_FORCE_DISCONNECT)
        return return_code

    def service_cleanup(self):
        self._messaging_service_state = MessagingServiceState.DISCONNECTED
        self.session_destroy()
        context_cleanup(self._context_p)

    def session_destroy(self) -> int:  # pragma: no cover
        # """
        # Destroys the specified session. On return, the opaque Context pointer
        # is set to NULL. This operation must not be performed in a Context callback
        # for the Context being destroyed. This includes all Sessions on the Context,
        # timers on the Context, and application-supplied register file descriptor
        # functions.
        # Returns:
        #      int :  returns  0 or -1
        # Raises:
        #      PubSubPlusClientError: if we didn't receive 1 as return code
        # """
        if self.__session_p:
            self._core_lib.solClient_session_destroy.argtypes = [c_void_p]
            return_code_on_destroy = session_destroy(self.__session_p)
            if return_code_on_destroy != SOLCLIENT_OK:
                logger.warning(last_error_info(return_code_on_destroy, "session destroy"))
                logger.warning("Unable to destroy session. Failure code: %d", return_code_on_destroy)
                raise PubSubPlusClientError(message=f"Unable to destroy session. Failure code: "
                                                    f"{return_code_on_destroy}")
            return return_code_on_destroy
            # </editor-fold>

    def create_session(self, config: dict) -> int:
        # """
        # When creating the Context, specify that the Context thread be
        # created automatically instead of having the application create its own
        # Context thread.
        # Args:
        #     config (dict):Configuration has been sent in the form of key value pairs.
        #
        # Returns:
        #     int : returns return code from solClient_session_create and value will be '0' for success
        # Raises:
        #         PubSubPlusClientError: if we didn't receive 1 as return code
        # """
        arr = self.__prepare_session_props(config)
        self._session_func_info = self.__create_session_func_info()
        return_code = session_create(arr, self._context_p, self.__session_p,
                                     self._session_func_info)

        logger.info('%s [%s]', ESTABLISH_SESSION_ON_HOST, config[transport_layer_properties.HOST])
        if return_code != SOLCLIENT_OK:
            core_exception_msg = last_error_info(status_code=return_code, caller_desc="Session Creation")
            exception_message = core_exception_msg[CCSMP_SUB_CODE]
            logger.debug('CORE API error: %s', core_exception_msg)
            if f"unspecified property '" \
               f"{CCSMP_SESSION_PROP_MAPPING[transport_layer_security_properties.TRUST_STORE_PATH]}'" \
                    in core_exception_msg:
                logger.warning("HOST: %s is secured, %s param is expected to establish SESSION",
                               config[transport_layer_properties.HOST],
                               transport_layer_security_properties.TRUST_STORE_PATH)
                raise PubSubPlusClientError(message=f"HOST: {config[transport_layer_properties.HOST]} is secured, "
                                                    f"{transport_layer_security_properties.TRUST_STORE_PATH} "
                                                    f"param is expected to establish SESSION")
            logger.error(core_exception_msg[CCSMP_SUB_CODE])
            if exception_message == CCSMP_SUB_CODE_FAILED_TO_LOAD_TRUST_STORE:
                logger.error(FAILED_TO_LOAD_TRUST_STORE)
                raise PubSubPlusClientError(message=FAILED_TO_LOAD_TRUST_STORE)
            if exception_message == CCSMP_SUB_CODE_UNRESOLVED_HOST:
                logger.error(UNRESOLVED_SESSION)
                raise ServiceUnreachableError(UNRESOLVED_SESSION)
            if exception_message == CCSMP_SUB_CODE_FAILED_LOADING_CERTIFICATE_AND_KEY:
                logger.error(FAILED_TO_LOADING_CERTIFICATE_AND_KEY)
                raise PubSubPlusClientError(message=FAILED_TO_LOADING_CERTIFICATE_AND_KEY)

        return return_code

    def send_message(self, msg_p) -> int:
        # """method to send the message using ccsmp
        # Args:
        #     msg_p: message pointer
        # """
        return self._core_lib.solClient_session_sendMsg(self.session_pointer, msg_p)

    @property
    def is_session_connected(self) -> bool:
        # """
        # property to know whether we are connected to session or not
        # Returns :
        # bool : True or False
        # """
        if self._messaging_service_state in [MessagingServiceState.CONNECTED, MessagingServiceState.RECONNECTED]:
            return True
        return False

    @property
    def message_service_state(self) -> MessagingServiceState:
        # """
        # property to know the state of messaging service
        # Returns :
        # MessagingServiceState
        # """
        return self._messaging_service_state

    @property
    def session_pointer(self):
        # """ this method will return the underlying  C-api session pointer"""
        return self.__session_p

    def __do_connect(self) -> int:
        # """
        # this method establishes the connection to the service, if the connection is established
        # the return code will be zero stating SOLCLIENT_OK, if the connection is not established properly
        # then the return_code will be anything other than zero, in order to handle exception the return code
        # is sent to the __handle_exception_message() along with the caller description.
        #
        # Returns:
        #     int: returns the return code ranging from (-1 to 8)
        # """
        self._messaging_service_state = MessagingServiceState.CONNECTING
        return_code = session_connect(self.__session_p)
        if return_code != SOLCLIENT_OK:
            self.__handle_exception_message(return_code=return_code, caller_desc='do_connect')
        return return_code

    def __handle_exception_message(self, return_code, caller_desc='SessionConnect') \
            :  # pylint: disable=no-self-use
        core_exception_msg = last_error_info(status_code=return_code, caller_desc=caller_desc)
        core_sub_code = core_exception_msg[CCSMP_SUB_CODE]
        if core_sub_code == CCSMP_SUBCODE_UNTRUSTED_CERTIFICATE:
            logger.warning('%s %s', UNTRUSTED_CERTIFICATE_MESSAGE, core_exception_msg)
            raise PubSubPlusClientError(message=f'{UNTRUSTED_CERTIFICATE_MESSAGE} {core_exception_msg}')
        if core_sub_code == CCSMP_SUB_CODE_FAILED_LOADING_CERTIFICATE_AND_KEY:
            logger.warning('%s %s', FAILED_TO_LOADING_CERTIFICATE_AND_KEY, core_exception_msg)
            raise PubSubPlusClientError(message=f'{FAILED_TO_LOADING_CERTIFICATE_AND_KEY} {core_exception_msg}')
        if core_sub_code == CCSMP_SUB_CODE_LOGIN_FAILURE:
            logger.warning('%s %s', BAD_CREDENTIALS, core_exception_msg)
            raise AuthenticationError(message=f'{BAD_CREDENTIALS} {core_exception_msg}')
        logger.warning(core_exception_msg)
        raise PubSubPlusClientError(message=core_exception_msg)

    def __create_session_func_info(self):
        # """ Create session function information needed for session creation. """

        class SolClientServiceCreateRxCallbackFuncInfo(Structure):  # pylint: disable=too-few-public-methods
            # """ Conforms to solClient_session_createRxCallbackFuncInfo_t (deprecated)
            # Applications should use solClient_session_createRxMsgCallbackFuncInfo.
            # Callback information for Session message receive callback. This is set on a per-Session basis.
            # """
            _fields_ = [
                ("callback_p", c_void_p),
                ("user_p", c_void_p)
            ]

        class SolClientServiceCreateEventCallbackFuncInfo(Structure):  # pylint: disable=too-few-public-methods
            # """ Conforms to solClient_session_createEventCallbackFuncInfo_t """
            _fields_ = [
                ("callback_p", self._event_callback_func_type),
                ("user_p", py_object)
            ]

        class SolClientServiceCreateRxMsgCallbackFuncInfo(Structure):  # pylint: disable=too-few-public-methods
            # """ Conforms to solClient_session_createRxMsgCallbackFuncInfo_t
            # Applications should use solClient_session_createRxMsgCallbackFuncInfo.
            # Callback information for Session message receive callback. This is set on a per-Session basis"""
            _fields_ = [
                ("callback_p", self._msg_callback_func_type),
                ("user_p", py_object)
            ]

        class SolClientServiceCreateFuncInfo(Structure):  # pylint: disable=too-few-public-methods

            # """ Conforms to solClient_session_createFuncInfo_t and
            # this function uses above three classes as arguments """

            _fields_ = [
                ("rx_info", SolClientServiceCreateRxCallbackFuncInfo),  # deprecated
                ("event_info", SolClientServiceCreateEventCallbackFuncInfo),
                ("rx_msg_info", SolClientServiceCreateRxMsgCallbackFuncInfo)
            ]

        if not self._event_callback and not self._msg_callback:
            self._event_callback = self._event_callback_func_type(self.__service_event_callback_routine)

            self._msg_callback = self._msg_callback_func_type(self.__service_msg_rx_callback_routine)

        session_func_info = SolClientServiceCreateFuncInfo(
            (c_void_p(None), c_void_p(None)),
            (self._event_callback, py_object),
            (self._msg_callback, py_object))
        return session_func_info

    def __service_event_callback_routine \
                    (self, _opaque_session_p, event_info_p, _pyobject):  # pylint: disable=too-many-branches
        # """
        # conforms to eventCallback
        #     The event callback function is mandatory for session creation.
        # Args:
        #     _opaque_session_p: The Session event that has occurred
        #     event_info_p: A pointer to a NULL-terminated string providing further information about the event,
        #      when available.
        #     _pyobject: Application-supplied correlation pointer where applicable
        # Returns: int
        # """
        info = event_info_p
        correlation_tag = b''
        if info.contents.correlation_p:
            correlation_tag = ctypes.cast(info.contents.correlation_p, ctypes.c_char_p).value
        event = info.contents.session_event

        message = info.contents.info_p.decode()
        response_code = info.contents.response_code
        error_info = last_error_info(status_code=response_code,
                                     caller_desc="From service event callback")
        exception = None
        if error_info[CCSMP_SUB_CODE] != CCSMP_SUB_CODE_OK:
            logger.warning(error_info)
            exception = PubSubPlusClientError(message=error_info)
            if error_info[CCSMP_INFO_SUB_CODE] == SolClientSubCode.SOLCLIENT_SUBCODE_PUBLISH_ACL_DENIED.value:
                exception = MessageRejectedByBrokerError(message=error_info)
            elif error_info[CCSMP_INFO_SUB_CODE] == SolClientSubCode.SOLCLIENT_SUBCODE_NO_SUBSCRIPTION_MATCH.value:
                exception = MessageDestinationDoesNotExistError(message=error_info)

        if event == SOLCLIENT_SESSION_EVENT_UP_NOTICE:
            self._messaging_service_state = MessagingServiceState.CONNECTED

        if event == SOLCLIENT_SESSION_EVENT_RECONNECTING_NOTICE:
            self._messaging_service_state = MessagingServiceState.RECONNECTING
            if self.listener_queue and self.attempt_listeners:
                self.connection_can_listen.set()

            for listener in self.attempt_listeners:
                self.__put_session_event(listener, self.listener_queue, message, exception)
            self.connection_can_listen.clear()

        if event == SOLCLIENT_SESSION_EVENT_RECONNECTED_NOTICE:
            self._messaging_service_state = MessagingServiceState.RECONNECTED
            if self.reconnection_listeners and self.listener_queue:
                self.connection_can_listen.set()

            for listener in self.reconnection_listeners:
                self.__put_session_event(listener, self.listener_queue, message, exception)
            self.connection_can_listen.clear()

        if event == SOLCLIENT_SESSION_EVENT_CAN_SEND:
            self.can_send_received.set()

        if event == SOLCLIENT_SESSION_EVENT_DOWN_ERROR:
            self._messaging_service_state = MessagingServiceState.DOWN
            self.can_send_received.set()  # wake up publisher readiness listener thread
            self._can_listen_to_ack.set()  # wake up persistent delivery listener thread
            for e in self._can_receive:
                if hasattr(self, e):
                    # get the receiver's can_receive event,  set it to wake up the thread
                    getattr(self, e).set()

            for e in self._can_peek:
                if hasattr(self, e):
                    # get the publisher's can_peek event, set it to wake up the thread
                    getattr(self, e).set()
            for e in self._state_change:
                if hasattr(self, e):
                    # get the receiver's state_change event, set it to wake up the thread
                    getattr(self, e).set()

            if self.service_interruption_listeners and self.listener_queue:
                self.connection_can_listen.set()

            for listener in self.service_interruption_listeners:
                self.__put_session_event(listener, self.listener_queue, message, exception)
            self.connection_can_listen.clear()

        if event == SOLCLIENT_SESSION_EVENT_CONNECT_FAILED_ERROR:
            self._messaging_service_state = MessagingServiceState.DISCONNECTED
        # TODO handle SOLCLIENT_SESSION_EVENT_RX_MSG_TOO_BIG_ERROR
        if event in [SOLCLIENT_SESSION_EVENT_ACKNOWLEDGEMENT, SOLCLIENT_SESSION_EVENT_REJECTED_MSG_ERROR]:
            # Based on the correlation tag ack is sent to respective publisher's queue
            if correlation_tag:
                # get publisher queue attribute reference name
                attr_name = correlation_tag.decode()
                # check if session has the publisher queue attribute
                if hasattr(self, attr_name):
                    # get the publisher queue
                    queue_name = getattr(self, correlation_tag.decode())
                    # the publisher queue can be None if the publisher was terminated
                    if queue_name is not None:
                        queue_name.put((event, exception))
                    else:
                        # publisher has been terminated
                        logger.info('Received message acknowledgement with [%s] without a publisher queue',
                                    correlation_tag)
                else:
                    # no matching publisher
                    logger.info('Received message acknowledgement with [%s] without a publisher', correlation_tag)
                self.can_listen_to_ack.set()

        return SOLCLIENT_CALLBACK_OK

    def __service_msg_rx_callback_routine(self, _opaque_session_p, _msg_p, _pyobject):  # pylint: disable=no-self-use
        # """
        # conforms to messageReceiveCallback
        #  The message receive callback function is mandatory for session creation
        # Args:
        #     _opaque_session_p:The Session event that has occurred
        #     _msg_p : pointer to message
        #     _pyobject : Application-supplied correlation pointer where applicable
        # Returns:
        #     int : return value 0
        # """
        return SOLCLIENT_CALLBACK_OK

    def __put_session_event(self, listener, listener_queue, message, exception):
        # """method for adding service event"""

        obj = _ServiceEvent(self._host, exception, message, datetime.datetime.now().timestamp())
        listener_queue.put((listener, obj))

    def __prepare_session_props(self, config: dict) -> ctypes.Array:
        # """
        #     Prepares the session props by comparing their instances and type casting the property value
        #     and finally adding the key value pairs to the dictionary
        #     Args:
        #     config: has key prop_value pairs of session property
        #     Returns:Array of config needed for session creation which got from config argument
        #     """
        self._host = config[transport_layer_properties.HOST]
        config = dict(
            (CCSMP_SESSION_PROP_MAPPING[k], str(int(v)) if isinstance(v, bool) else str(v)) for k, v in config.items())
        config = {**config, **default_props}  # merge the config with default props
        config_list = list(reduce(lambda x, y: x + y, config.items()))
        config_list = [e.encode() for e in config_list]
        config_list.append(c_char_p(None))  # add NULL at the end of array
        return prepare_array(config)
