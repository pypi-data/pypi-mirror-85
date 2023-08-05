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

"""Module contains the Implementation class and methods for the OutboundMessageBuilder and OutboundMessage"""
import ctypes
import logging
import weakref
from ctypes import c_int64, c_char_p
from typing import TypeVar, Any

from solace.messaging.config import sol_constants
from solace.messaging.config.sol_constants import SOLCLIENT_OK, SOLCLIENT_FAIL
from solace.messaging.core._message import _Message
from solace.messaging.core._solace_message import _SolaceMessage
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError
from solace.messaging.publisher.outbound_message import OutboundMessageBuilder, OutboundMessage
from solace.messaging.publisher.outbound_message_utility import container_add_byte_array, \
    container_add_string, container_add_int64, close_map, add_message_properties

logger = logging.getLogger('solace.messaging.publisher')


def map_cleanup(map_p):  # pylint: disable=missing-function-docstring
    if map_p:
        try:
            return_code = close_map(map_p)
            if return_code != SOLCLIENT_OK:
                logger.warning("Failed to free up the map container with status code: %d", return_code)
        except PubSubPlusClientError as exception:
            logger.warning("Failed to free up the map container with error: %s", str(exception))


class SolaceMap:  # pylint: disable=too-few-public-methods,missing-class-docstring, missing-function-docstring
    def __init__(self, solace_message=None, map_p=None):
        if map_p is not None:
            self._map_p = map_p
        else:
            self._map_p = ctypes.c_void_p()
            return_code = solace_message.message_create_user_property_map(map_p=self._map_p)
            if return_code != SOLCLIENT_OK:
                logger.warning("Unable to set User Property map. Status code: [%d]", return_code)
                raise PubSubPlusClientError(message=f"Unable to set User Property map. "
                                                        f"Status code: [{return_code}]")
        self._finalizer = weakref.finalize(self, map_cleanup, self._map_p)

    @property
    def map_p(self):
        return self._map_p

    @staticmethod
    def get_map_from_message(solace_message):
        map_p = ctypes.c_void_p()
        return_code = solace_message.message_get_user_property_map(map_p)
        if return_code == SOLCLIENT_OK:
            return SolaceMap(None, map_p)
        return None

    @staticmethod
    def add_user_props_to_container(map_p, property_key: str, property_value: Any) \
            :  # pylint: disable=no-self-use
        # """
        #  Add user properties to the container
        # Args:
        #     property_key (str): key
        #     property_value (Any):  value
        #
        # Returns:
        #
        # """
        logger.debug('Adding user property. Property key: [%s]. Property value: [%s]. '
                     'Type: [%s]', property_key, str(type(property_value)), property_value)
        if isinstance(property_value, int):
            property_value = c_int64(property_value)
            container_add_int64(map_p, property_value, property_key)
        elif isinstance(property_value, str):
            property_value = c_char_p(property_value.encode(sol_constants.ENCODING_TYPE))
            container_add_string(map_p, property_value, property_key)
        elif isinstance(property_value, bytearray):
            char_array = ctypes.c_char * len(property_value)
            property_value = char_array.from_buffer(property_value)
            container_add_byte_array(map_p, property_value, property_key)


class _OutboundMessageBuilder(OutboundMessageBuilder) \
        :  # pylint: disable=missing-class-docstring, missing-function-docstring
    # """
    # This builder is used for building outbound messages which can hold any type of messages used for publish message
    # """

    T = TypeVar('T', bytearray, str, 'OutboundMessage')

    def __init__(self):
        # """
        # message pointer initialization & allocation takes place here
        # """
        logger.debug('[%s] initialized', type(self).__name__)
        self._solace_message = _SolaceMessage()
        self.priority = None

    def from_properties(self, configuration: dict) -> 'OutboundMessageBuilder':  # pragma: no cover
        # """
        # This method takes dict and prepare message properties
        # Args:
        #     configuration (dict):
        #
        # Returns:
        #
        # """
        add_message_properties(configuration, self._solace_message)
        return self

    def with_property(self, property_key: str, property_value: str) -> 'OutboundMessageBuilder':
        # """
        #  create user property with the given key & value
        # Args:
        #     property_key (str): key
        #     property_value (str): value
        #
        # Returns:
        #     OutboundMessageBuilder
        # """
        add_message_properties({property_key: property_value}, self._solace_message)
        return self

    def with_expiration(self, timestamp: int) -> 'OutboundMessageBuilder':
        # """
        # set expiration time
        # Args:
        #     timestamp (int): timestamp in ms
        #
        # Returns:
        #     OutboundMessageBuilder
        # """
        logger.debug('Set message expiration time: [%d]', timestamp)
        return_code = self._solace_message.set_message_expiration(timestamp)

        if return_code != SOLCLIENT_OK:
            logger.warning("Unable to set expiration time. Status code: [%d]", return_code)
            raise PubSubPlusClientError(
                message=f"Unable to set expiration time. Status code: [{return_code}]")  # pragma: no cover
        return self

    def with_priority(self, priority: int) -> 'OutboundMessageBuilder':
        # """
        # Set the priority (0 to 255), where zero is the lowest  priority
        # Args:
        #     priority (OutboundMessageBuilder.Priority): integer value
        #
        # Returns:
        #     OutboundMessageBuilder
        # """
        logger.debug('Set message priority: [%d]', priority)
        return_code = self._solace_message.set_message_priority(priority)

        if return_code != SOLCLIENT_OK:
            logger.warning("Unable to set priority. Status code: [%d]", return_code)
            raise PubSubPlusClientError(message=f"Unable to set priority. "
                                                    f"Status code: [{return_code}]")  # pragma: no cover
        return self

    def with_sequence_number(self, sequence_number: int) -> 'OutboundMessageBuilder':
        # """
        # Set the sequence number for the message
        # Args:
        #     sequence_number (int):  Expecting a integer value
        #
        # Returns:
        #     OutboundMessageBuilder
        # """
        return_code = self._solace_message.set_message_sequence_number(sequence_number)

        if return_code != SOLCLIENT_OK:
            logger.warning("Unable to set sequence number: %d", return_code)
            raise PubSubPlusClientError(message=f"Unable to set sequence number: {return_code}")  # pragma: no cover
        return self

    def with_application_message_id(self, application_message_id: str) -> 'OutboundMessageBuilder':
        # """
        # Set the application message id for a message from a str, or None to delete
        # Args:
        #     application_message_id (str):  application message id
        #
        # Returns:
        #     OutboundMessageBuilder
        # """
        if application_message_id is not None:  # for this msg_p im setting an app id will i lose it?
            return_code = self._solace_message.set_message_application_message_id(application_message_id)
        else:
            return_code = self._solace_message.delete_message_application_message_id()

        if return_code != SOLCLIENT_OK:
            logger.warning("Unable to set application message id. Status code: [%d]", return_code)
            raise PubSubPlusClientError(
                message=f"Unable to set application message id. Status code: [{return_code}]")  # pragma: no cover
        return self

    def with_application_message_type(self, application_message_type: str) -> 'OutboundMessageBuilder':
        # """
        # Set the application message type for a message from a string or None to delete
        # Args:
        #     application_message_type (str): application message type
        #
        # Returns:
        #     OutboundMessageBuilder
        #
        # """
        if application_message_type is not None:
            return_code = self._solace_message.set_message_application_message_type(application_message_type)
        else:
            return_code = self._solace_message.delete_message_application_message_type()

        if return_code != SOLCLIENT_OK:
            logger.warning("Unable to set application message type. Status code: [%d]", return_code)
            raise PubSubPlusClientError(message=f"Unable to set application message type. Status code: "
                                                    f"[{return_code}]")  # pragma: no cover
        return self

    def with_http_content_header(self, content_type, content_encoding) -> 'OutboundMessageBuilder':
        # """
        # Setting the HTTP content type and encoding for a message from a string
        # Args:
        #     content_type (str):  expecting a valid content type
        #     content_encoding (str):  expecting a valid content  encoding
        # Returns:
        #
        # """
        content_type_return_code = self._solace_message.set_message_http_content_type(content_type)
        content_encoding_return_code = self._solace_message.set_message_http_content_encoding(content_encoding)
        if content_encoding_return_code != SOLCLIENT_OK or content_type_return_code != SOLCLIENT_OK:
            logger.warning("Unable to set HTTP content header: content type status code: [%d], "
                           "content_encoding status code: [%d]", content_type_return_code, content_encoding_return_code)
            raise PubSubPlusClientError(
                message=f"Unable to set HTTP content header: content type status code: [{content_type_return_code}], "
                        f"content_encoding status code: [{content_encoding_return_code}]")  # pragma: no cover
        return self

    def build(self, payload: T, additional_message_properties=None, converter=None) -> '_OutboundMessage':
        # """
        # Args:
        #     payload (T): payload
        # Kwargs:
        #     additional_message_properties (Any): properties
        #     converter (Any): converter
        # Returns:
        #
        # """

        # Here self.msg_p is a template for all the message's properties
        msg_p_dup = self._solace_message.message_duplicate()
        logger.debug('BUILD [%s]', OutboundMessage.__name__)
        return_code = SOLCLIENT_FAIL
        if not converter:
            if isinstance(payload, bytearray):
                char_array = ctypes.c_char * len(payload)
                message = char_array.from_buffer(payload)
                return_code = msg_p_dup.message_set_binary_attachment(message)

            elif isinstance(payload, str):
                return_code = msg_p_dup.message_set_binary_attachment_string(payload)

            if additional_message_properties:
                add_message_properties(additional_message_properties, msg_p_dup)
        elif converter:
            additional_properties = converter.get_message_properties()

            if additional_properties:
                add_message_properties(additional_properties, msg_p_dup)
            payload_bytes = converter.to_bytes(payload)
            char_array = ctypes.c_char * len(payload_bytes)
            message = char_array.from_buffer_copy(payload_bytes)
            return_code = msg_p_dup.message_set_binary_attachment(msg=message, msg_length=len(payload_bytes))

        if return_code != SOLCLIENT_OK:
            logger.warning("Failed to create attachment for the message. Status code: [%d]", return_code)
            raise PubSubPlusClientError(message=f"Failed to create attachment for the message. "
                                                    f"Status code: [{return_code}]")  # pragma: no cover
        return _OutboundMessage(msg_p_dup)


class _OutboundMessage(_Message, OutboundMessage):  # pylint: disable=missing-class-docstring
    # """ Implementation class for OutboundMessage abstract class """

    def __init__(self, msg_p):
        # """
        # Args: msg_p:  SolaceMessage used to publish the message
        # """

        logger.debug('[%s] initialized', type(self).__name__)
        super().__init__(msg_p)

    def __str__(self):
        return self._solace_message.get_message_dump()
