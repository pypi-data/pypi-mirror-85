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

# pylint: disable=too-few-public-methods, missing-class-docstring, missing-module-docstring, missing-function-docstring

import ctypes
import logging
from typing import Union, TypeVar

from solace.messaging._impl._interoperability_support import _RestInteroperabilitySupport
from solace.messaging.config.sol_constants import SOLCLIENT_NOT_FOUND, SOLCLIENT_OK, SOLCLIENT_FAIL
from solace.messaging.config.solace_message_constants import FAILED_TO_RETRIEVE, FAILED_TO_GET_APPLICATION_TYPE
from solace.messaging.core._message import _Message
from solace.messaging.core._solace_message import _SolaceMessage
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError
from solace.messaging.receiver.inbound_message import InboundMessage
from solace.messaging.receiver.inbound_message_utility import get_message_id
from solace.messaging.utils.converter import BytesToObject
from solace.messaging.utils.solace_utilities import Util

logger = logging.getLogger('solace.messaging.receiver')


class _InboundMessage(_Message, InboundMessage):
    # """ implementation class for InboundMessage"""

    T = TypeVar('T')

    def __init__(self, solace_message: _SolaceMessage):
        logger.debug('[%s] initialized', type(self).__name__)
        super().__init__(solace_message)
        self._get_http_content_type = None
        self._get_http_content_encoding = None
        self.__process_rest_interoperability(self.solace_message)
        self.__discard_notification: 'InboundMessage.MessageDiscardNotification' = \
            _InboundMessage.MessageDiscardNotification(self._solace_message)
        self.__rest_interoperability_support = _RestInteroperabilitySupport(self._get_http_content_type,
                                                                            self._get_http_content_encoding)

    @property
    def message_id(self):
        return get_message_id(self.solace_message.msg_p)

    def get_and_convert_payload(self, converter: BytesToObject[T], output_type: type) -> type:
        # """
        # Get payload and converts to the target type using given converter
        # Args:
        #     converter:
        #     output_type:
        # Returns:
        # """
        received_message = self.get_binary_attachment()
        bytes_to_object = converter.convert(received_message)
        if isinstance(bytes_to_object, output_type):
            logger.debug('Get and convert payload')
            return bytes_to_object
        logger.warning("Incompatible message, provided converter can't be used")  # pragma: no cover
        raise PubSubPlusClientError(
            message="Incompatible message, provided converter can't be used")  # pragma: no cover

    def get_destination_name(self) -> str:  # type: ignore
        # """
        # Get name of the destination on which message was received (topic or queue)
        # Returns:
        #     destination (str) : destination name
        # """

        class SolClientDestination(ctypes.Structure):  # pylint: disable=too-few-public-methods
            """ Conforms to solClient_destination_t """
            _fields_ = [
                ("dest_type", ctypes.c_int),
                ("dest", ctypes.c_char_p)
            ]

        destination = SolClientDestination()
        return_code = self.solace_message.get_destination(destination)
        if return_code == SOLCLIENT_OK:
            return destination.dest.decode('utf-8')
        if return_code == SOLCLIENT_NOT_FOUND:  # pragma: no cover
            return None
        logger.warning("Failed to get destination name. Status code: %d", return_code)  # pragma: no cover
        raise PubSubPlusClientError(
            message=f"Failed to get destination name. Status code: {return_code}")  # pragma: no cover

    def get_time_stamp(self) -> [int, None]:
        # """
        # Get the timestamp of the message when it arrived on a broker in ms
        # Returns:
        #     timestamp (int) : timestamp in ms
        # """
        timestamp_p = ctypes.c_uint64()
        return_code = self.solace_message.get_message_timestamp(timestamp_p)
        if return_code == SOLCLIENT_OK:
            timestamp_in_ms = timestamp_p.value
            logger.debug('Message receive timestamp: %d', timestamp_in_ms)
            return timestamp_in_ms
        if return_code == SOLCLIENT_NOT_FOUND:
            return None
        logger.warning("Unable to get message receive timestamp. Status code: %d", return_code)
        raise PubSubPlusClientError(message=f"Unable to get message receive timestamp. "
                                            f"Status code: {return_code}")  # pragma: no cover

    def get_sender_timestamp(self) -> [int, None]:
        # """
        # Gets the sender's timestamp. This field is mostly set automatically during message publishing.
        # Returns:
        #     timestamp (int) : timestamp (in ms, from midnight, January 1, 1970 UTC) or null if not set
        # """
        timestamp_p = ctypes.c_uint64()
        return_code = self.solace_message.get_message_sender_timestamp(timestamp_p)
        if return_code == SOLCLIENT_OK:
            timestamp_in_ms = timestamp_p.value
            logger.debug('Message sender timestamp: %d', timestamp_in_ms)
            return timestamp_in_ms
        if return_code == SOLCLIENT_NOT_FOUND:
            return None
        logger.warning("Unable to get message send timestamp. Status code: %d", return_code)  # pragma: no cover
        raise PubSubPlusClientError('Unable to get message sender timestamp')  # pragma: no cover

    def get_application_message_type(self) -> Union[str, None]:
        # """
        # Gets the application message type. This value is used by applications only, and is passed
        # through the API untouched
        # Returns:
        #     msg_type ( str/None) :application message type or null if not set
        # """
        app_msg_type = ctypes.c_char_p()

        return_code = self.solace_message.get_application_msg_type(app_msg_type)
        if return_code != SOLCLIENT_OK:
            logger.warning('%s Status code: %d', FAILED_TO_GET_APPLICATION_TYPE, return_code)
            return None
        msg_type = app_msg_type.value.decode('utf-8')  # type: ignore
        logger.debug('Get application message type: [%s]', msg_type)
        return msg_type

    def get_rest_interoperability_support(self) -> '_RestInteroperabilitySupport':
        # """Get RestInteroperabilitySupport object to invoke it's methods"""
        return self.__rest_interoperability_support

    def get_message_discard_notification(self) -> 'InboundMessage.MessageDiscardNotification':
        return self.__discard_notification

    class MessageDiscardNotification(InboundMessage.MessageDiscardNotification) \
            :  # pylint: disable=missing-class-docstring
        def __init__(self, msg_p: _SolaceMessage):
            self.has_discard_notification = msg_p.has_discard_indication()

        def has_broker_discard_indication(self) -> bool:  # pylint: disable=no-else-return
            """ Retrieve Broker Discard Indication

            When the PubSub+ broker discards messages before sending them, the next message successfully
            sent to the receiver will have Discard Indication set.

            Returns: true if PubSub+ broker has discarded one or more messages prior to the current message.
            """
            if not isinstance(self.has_discard_notification, int):  # pragma: no cover
                logger.warning("Core api doesn't return boolean flag, and it has [%s]", self.has_discard_notification)
                return False
            if self.has_discard_notification not in [0, 1]:  # pragma: no cover
                logger.warning("Core api doesn't return boolean flag, and it has [%s]", self.has_discard_notification)
                return False
            result = bool(self.has_discard_notification)
            logger.debug('Has discard indication!: [%s]', result)
            return result

    def __process_rest_interoperability(self, msg_p: _SolaceMessage):  # pragma: no cover
        content_type_p = ctypes.c_char_p()
        encoding_p = ctypes.c_char_p()
        content_type_return_code = msg_p.get_message_http_content_type(content_type_p)
        content_encoding_return_type = msg_p.get_message_http_content_encoding(encoding_p)
        self._get_http_content_type = self.__process_rest_data(content_type_return_code, content_type_p)
        self._get_http_content_encoding = self.__process_rest_data(content_encoding_return_type, encoding_p)

    @staticmethod
    def __process_rest_data(return_code, ptr_value):  # pragma: no cover
        if return_code == SOLCLIENT_OK:
            return ptr_value.value.decode('utf-8')
        if return_code in [SOLCLIENT_NOT_FOUND, SOLCLIENT_FAIL]:
            if return_code == SOLCLIENT_FAIL:
                logger.warning(FAILED_TO_RETRIEVE)
            return None
        return None

    def __str__(self):
        return self.solace_message.get_message_dump()
