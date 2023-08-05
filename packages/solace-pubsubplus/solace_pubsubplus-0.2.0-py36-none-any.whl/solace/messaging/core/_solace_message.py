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


# module containing the class and methods/functions which represent a C-API opaqueMsg
# #pylint:disable=missing-module-docstring, missing-function-docstring, too-many-public-methods
import ctypes
import logging
import weakref
from ctypes import c_uint32, sizeof, c_int64, c_int32, c_uint64, byref

import solace
from solace.messaging.config import sol_constants
from solace.messaging.config.sol_constants import SOLCLIENT_OK, \
    SOLCLIENT_MSGDUMP_FULL, DEFAULT_BUFFER_SIZE, DEFAULT_BUFFER_MULTIPLIER
from solace.messaging.config.solace_properties.message_properties import APPLICATION_MESSAGE_TYPE, PRIORITY, \
    HTTP_CONTENT_TYPE, \
    ELIDING_ELIGIBLE, PERSISTENT_TIME_TO_LIVE, PERSISTENT_DMQ_ELIGIBLE, HTTP_CONTENT_ENCODING, CORRELATION_ID, \
    PERSISTENT_EXPIRATION, PERSISTENT_ACK_IMMEDIATELY, APPLICATION_MESSAGE_ID, SEQUENCE_NUMBER
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError
from solace.messaging.solace_logging.core_api_log import last_error_info

logger = logging.getLogger('solace.messaging.core.api')


def message_cleanup(msg_p, caller):
    """Clean up or free the resources used for the message."""
    try:
        if msg_p is None:  # pylint: disable=no-else-return
            return
        elif isinstance(msg_p, ctypes.c_int):
            msg_p = ctypes.c_void_p(int(msg_p))
            solace.CORE_LIB.solClient_msg_free(byref(msg_p))
        elif isinstance(msg_p, ctypes.c_void_p):
            solace.CORE_LIB.solClient_msg_free(byref(msg_p))
        else:
            logger.error("%s msg_p not a valid type", caller)
    except PubSubPlusClientError as exception:
        logger.error(exception)

class _SolaceMessage:
    # """The class handles PubSub+ messaging. """
    def __init__(self, msg_p=None):
        self._msg_p = ctypes.c_void_p(None)
        self._message_properties_mapping = {APPLICATION_MESSAGE_TYPE: self.set_message_application_message_type,
                                            ELIDING_ELIGIBLE: self.set_eliding_eligible,
                                            PRIORITY: self.set_message_priority,
                                            HTTP_CONTENT_TYPE: self.set_message_http_content_type,
                                            HTTP_CONTENT_ENCODING: self.set_message_http_content_encoding,
                                            CORRELATION_ID: self.message_set_correlation_id,
                                            PERSISTENT_TIME_TO_LIVE: self.set_ttl,
                                            PERSISTENT_EXPIRATION: self.set_message_expiration,
                                            PERSISTENT_DMQ_ELIGIBLE: self.set_persistent_dmq_eligible,
                                            PERSISTENT_ACK_IMMEDIATELY: self.set_ack_immediately,
                                            SEQUENCE_NUMBER: self.set_message_sequence_number,
                                            APPLICATION_MESSAGE_ID: self.set_message_application_message_id}

        if msg_p is None:
            return_code = solace.CORE_LIB.solClient_msg_alloc(ctypes.byref(self._msg_p))
            if return_code != SOLCLIENT_OK:
                raise PubSubPlusClientError(message=f"Unable to allocate SolaceMessage. "
                                                        f"Status code: [{return_code}]")
        else:
            self._msg_p = msg_p
        self._finalizer = weakref.finalize(self, message_cleanup, self._msg_p, "Solace message cleanup")

    @property
    def msg_p(self):
        return self._msg_p

    @property
    def message_properties_mapping(self):
        return self._message_properties_mapping

    def handle_message_properties(self, message_properties: dict):
        # """
        #
        # Args:
        #     message_properties ():
        # """
        if message_properties:
            for key, value in message_properties.items():
                if key in self._message_properties_mapping:
                    return_code = self._message_properties_mapping[key](value)  # call the respective property setter
                    if return_code != SOLCLIENT_OK:
                        logger.warning(last_error_info(return_code, key))

    def set_persistent_dmq_eligible(self, dmqe):
        # """
        # Given a msg_p, set the Dead Message Queue (DMQ) eligible property on a message. When this
        #   option is set, messages that expire in the network, are saved on a appliance dead message
        #   queue. Otherwise expired messages are discarded.
        # Args:
        #     msg_p (): solClient_opaqueMsg_pt that is returned from a previous call
        #                   to solClient_msg_alloc() or received in a receive
        #                   message callback
        #     dmqe ():0 - clear, 1 - set
        #
        # Returns::SOLCLIENT_OK on success, ::SOLCLIENT_FAIL if
        #                         msg_p is invalid
        #
        # """
        # self.persistent_dmq_eligible = dmqe
        return solace.CORE_LIB.solClient_msg_setDMQEligible(self._msg_p, ctypes.c_int(int(dmqe)))

    def set_ttl(self, ttl):
        #  Given a msg_p, set the Time To Live (TTL) for a message. Setting the Time To Live to
        #  zero disables TTL for the message   This property is only valid for Guaranteed messages
        #  (Persistent and Non-Persistent).
        #   It has no effect when used in conjunction with other message types unless the message
        #   is promoted by the appliance to a Guaranteed message..
        # """
        #
        # Args:
        #     msg_p (): solClient_opaqueMsg_pt that is returned from a previous call
        #                   to solClient_msg_alloc() or received in a receive
        #                   message callback
        #     ttl (int): 64-bit value in ms to use for message time to live.
        #
        # Returns:SOLCLIENT_OK on success, ::SOLCLIENT_FAIL if msg_p is invalid
        #
        # """"""
        return solace.CORE_LIB.solClient_msg_setTimeToLive(self._msg_p, ctypes.c_int64(ttl))

    def set_dmq_eligible(self, dmqe):
        # """
        # Given a msg_p, set the Dead Message Queue (DMQ) eligible property on a message. When this
        #   option is set, messages that expire in the network, are saved on a appliance dead message
        #   queue. Otherwise expired messages are discarded.
        # Args:
        #     dmqe ():0 - clear, 1 - set
        #
        # Returns::SOLCLIENT_OK on success, ::SOLCLIENT_FAIL if
        #                         msg_p is invalid
        #
        # """
        return solace.CORE_LIB.solClient_msg_setDMQEligible(self._msg_p, ctypes.c_int(int(dmqe)))

    def set_eliding_eligible(self, elide):
        # """
        #  Given a msg_p, set the ElidingEligible property on a message. Setting this property
        #  to true indicates that this message should be eligible for eliding. Message eliding
        #  enables filtering of data to avoid transmitting every single update to a subscribing
        #  client. It can be used to overcome slow consumers or any situation where a slower
        #  message rate is desired.
        #
        #  Time-based eliding (supported in SolOS-TR) ensures that subscriber applications
        #  always receive only the most current update of a published topic at a rate that
        #  they can manage. By limiting the incoming message rate, a subscriber application
        #  is able to avoid a message backlog filled with outdated messages.
        #
        #  This property does not indicate whether the message was elided or even provide
        #  information about the subscriber's configuration (with regards to Message Eliding)
        # Args:
        #     elide ():A Boolean that indicates whether to set or reset the Eliding Eligible
        #                   attribute
        #
        # Returns:SOLCLIENT_OK on success, ::SOLCLIENT_FAIL if msg_p is invalid.
        #
        # """
        return solace.CORE_LIB.solClient_msg_setElidingEligible(self._msg_p, ctypes.c_int(int(elide)))

    def set_ack_immediately(self, val):
        # """
        #  Given a msg_p, set the optional ACK Immediately message property.
        #  When the ACK Immediately property is set to true on an outgoing Guaranteed Delivery message,
        #  it indicates that the appliance should ACK this message immediately upon receipt.
        #  By default the property is set to false on newly created messages.
        #
        #  This property, when set by a publisher, may or may not be removed by the appliance prior to delivery
        #  to a consumer, so message consumers must not expect the property value indicates how the message was
        #  originally published. Therefore if a received message
        #  is forwarded by the application, the ACK immediately property should be explicitly set to the desired
        #  value (true or false).
        #
        #  Setting this property on an outgoing direct message has no effect
        # Args:
        #     val (): A Boolean that indicates whether to set or clear the ACK Immediately message property.
        #
        # Returns:SOLCLIENT_OK on success, ::SOLCLIENT_FAIL if msg is invalid.
        #
        # """
        return solace.CORE_LIB.solClient_msg_setAckImmediately(self._msg_p, ctypes.c_int(int(val)))

    def message_duplicate(self):
        """method for duplicating the message

        Args:
            msg_p: message pointer
        """
        new_msg_p = ctypes.c_void_p(None)
        return_code = solace.CORE_LIB.solClient_msg_dup(self._msg_p, byref(new_msg_p))
        if return_code == SOLCLIENT_OK:
            return _SolaceMessage(new_msg_p)
        raise PubSubPlusClientError("Failed to get a duplicate message")

    def message_set_destination(self, destination):
        """method to set the message destination
        Args:
            destination: topic destination
        """
        return solace.CORE_LIB.solClient_msg_setDestination(self._msg_p,
                                                            byref(destination), sizeof(destination))

    def set_message_expiration(self, timestamp_ms):
        # """method to set the message expiration"""
        return solace.CORE_LIB.solClient_msg_setExpiration(self._msg_p, c_int64(timestamp_ms))

    def set_message_priority(self, priority):
        # """method to set the message priority"""
        return solace.CORE_LIB.solClient_msg_setPriority(self._msg_p, c_int32(priority))

    def set_message_sequence_number(self, sequence_number):
        # """method to set the message sequence number"""
        return solace.CORE_LIB.solClient_msg_setSequenceNumber(self._msg_p, c_uint64(sequence_number))

    def set_message_http_content_type(self, content_type):
        # """method to set message http content type"""
        return solace.CORE_LIB.solClient_msg_setHttpContentType(self._msg_p, ctypes.c_char_p(content_type.encode()))

    def set_message_http_content_encoding(self, content_encoding):
        # """method to set the message http content encoding
        # Args:
        #     msg_p: message pointer
        #     content_encoding: content encoding
        # """
        return solace.CORE_LIB.solClient_msg_setHttpContentEncoding(self._msg_p,
                                                                    ctypes.c_char_p(content_encoding.encode()))

    def message_create_user_property_map(self, map_p, size=0):
        # """method to crete  user property map"""
        return solace.CORE_LIB.solClient_msg_createUserPropertyMap(self._msg_p, ctypes.byref(map_p), size)

    def message_set_binary_attachment(self, msg, msg_length=None):
        # """method to set the binary attachment
        # Args:
        #     msg_p: message pointer
        #     msg: message
        #     msg_length: the message length
        # """
        if msg_length is None:
            msg_length = len(msg)
        return solace.CORE_LIB.solClient_msg_setBinaryAttachment(self._msg_p, msg, c_uint32(msg_length))

    def message_get_binary_attachment_ptr(self, binary_p, binary_len):
        # """method to get the binary attachment pointer"""
        return solace.CORE_LIB.solClient_msg_getBinaryAttachmentPtr(self._msg_p, ctypes.byref(binary_p),
                                                                    ctypes.byref(binary_len))

    def message_set_binary_attachment_string(self, msg):
        # """method to set the binary attachment string"""
        return solace.CORE_LIB.solClient_msg_setBinaryAttachmentString(self._msg_p,
                                                                       msg.encode(sol_constants.ENCODING_TYPE))

    def set_message_application_message_id(self, application_message_id):
        # """method to set message application message id"""
        return solace.CORE_LIB.solClient_msg_setApplicationMessageId(self._msg_p,
                                                                     ctypes.c_char_p(application_message_id.encode()))

    def set_message_application_message_type(self, application_message_type):
        # """method to set the message application message type"""
        return solace.CORE_LIB.solClient_msg_setApplicationMsgType(self._msg_p,
                                                                   ctypes.c_char_p(application_message_type.encode()))

    def delete_message_application_message_type(self):
        # """method to delete the message application message type"""
        return solace.CORE_LIB.solClient_msg_deleteApplicationMsgType(self._msg_p)

    def delete_message_application_message_id(self):
        # """method to delete the message application message id"""
        return solace.CORE_LIB.solClient_msg_deleteApplicationMessageId(self._msg_p)

    def get_buffer_details(self):
        buffer_p = ctypes.c_void_p(None)
        buffer_size = ctypes.c_uint32(0)
        return_code = self.message_get_binary_attachment_ptr(buffer_p, buffer_size)
        if return_code != SOLCLIENT_OK:
            logger.warning("Unable to get payload for the message. Status code: %d", return_code)
            raise PubSubPlusClientError(f"Unable to get payload for the message. "
                                            f"Status code: {return_code}")  # pragma: no cover
        return buffer_size.value, buffer_p.value

    def get_message_dump(self):
        buffer_size, _ = self.get_buffer_details()
        buffer = ctypes.create_string_buffer(DEFAULT_BUFFER_SIZE + buffer_size * DEFAULT_BUFFER_MULTIPLIER)
        return_code = solace.CORE_LIB.solClient_msg_dumpExt(self._msg_p, ctypes.byref(buffer),
                                                            DEFAULT_BUFFER_SIZE +
                                                            (DEFAULT_BUFFER_MULTIPLIER * buffer_size),
                                                            SOLCLIENT_MSGDUMP_FULL)
        if return_code == SOLCLIENT_OK:
            return buffer.value.decode()

        raise PubSubPlusClientError("Failed to retrieve the message dump")

    def get_message_expiration(self, timestamp_p):
        # """method to get the message expiration"""
        return solace.CORE_LIB.solClient_msg_getExpiration(self._msg_p, ctypes.byref(timestamp_p))

    def get_message_priority(self, priority: int):
        # """method to get the message priority"""
        return solace.CORE_LIB.solClient_msg_getPriority(self._msg_p, ctypes.byref(priority))

    def get_message_sequence_number(self, sequence_number):
        # """method to get the message sequence number"""
        return solace.CORE_LIB.solClient_msg_getSequenceNumber(self._msg_p, ctypes.byref(sequence_number))

    def get_destination(self, destination):
        # """method to get the destination name"""
        return solace.CORE_LIB.solClient_msg_getDestination(self._msg_p, ctypes.byref(destination),
                                                            ctypes.sizeof(destination))

    def get_message_timestamp(self, timestamp_p):
        # """method to get the message  timestamp"""
        return solace.CORE_LIB.solClient_msg_getRcvTimestamp(self._msg_p, ctypes.byref(timestamp_p))

    def get_message_sender_timestamp(self, timestamp_p):
        # """method to get the message sender timestamp"""
        return solace.CORE_LIB.solClient_msg_getSenderTimestamp(self._msg_p, ctypes.byref(timestamp_p))

    def get_message_http_content_type(self, type_p):
        # """method to get the http content type
        # Args:
        #     msg_p: message pointer
        #     type_p: type pointer
        # """
        return solace.CORE_LIB.solClient_msg_getHttpContentType(self._msg_p, ctypes.byref(type_p))

    def get_message_http_content_encoding(self, encoding_p):
        # """method to get the message http content encoding
        # Args:
        #     msg_p: message pointer
        #     encoding_p: encoding pointer
        # """
        return solace.CORE_LIB.solClient_msg_getHttpContentEncoding(self._msg_p, ctypes.byref(encoding_p))

    def message_get_user_property_map(self, map_p):
        # """method to get the user property map"""
        return solace.CORE_LIB.solClient_msg_getUserPropertyMap(self._msg_p, ctypes.byref(map_p))

    def message_get_correlation_id(self, correlation_p):
        # """method to get the correlation id
        # Args:
        #     msg_p:  message pointer
        #     correlation_p: A pointer to string pointer to receive correlation_id pointer
        # """
        return solace.CORE_LIB.solClient_msg_getCorrelationId(self._msg_p, ctypes.byref(correlation_p))

    def message_set_correlation_id(self, correlation_id):
        # """method to set the correlation id
        # Args:
        #     msg_p:  message pointer
        #     correlation_p: A pointer to string to copy into correlation_id
        # """
        return solace.CORE_LIB.solClient_msg_setCorrelationId(self._msg_p, ctypes.c_char_p(correlation_id.encode()))

    def message_get_binary_attachment_string(self, binary_p):
        # """method to get the message binary attachment string"""
        return solace.CORE_LIB.solClient_msg_getBinaryAttachmentString(self._msg_p, ctypes.byref(binary_p))

    def get_application_message_id(self, msg_id):
        # """method to get the application message id
        # Args:
        #     msg_p: message pointer
        #     msg_id: message id
        # """
        return solace.CORE_LIB.solClient_msg_getApplicationMessageId(self._msg_p, ctypes.byref(msg_id))

    def get_application_msg_type(self, app_msg_type):
        # """method to get the application message type"""
        return solace.CORE_LIB.solClient_msg_getApplicationMsgType(self._msg_p, ctypes.byref(app_msg_type))

    def get_message_id(self, msg_id):
        # """method to get the message id"""
        return solace.CORE_LIB.solClient_msg_getMsgId(self._msg_p, ctypes.byref(msg_id))

    def has_discard_indication(self):
        # """method to get discard indication status"""
        return solace.CORE_LIB.solClient_msg_isDiscardIndication(self._msg_p)

    def get_delivery_mode(self):
        mode = ctypes.c_uint32()
        solace.CORE_LIB.solClient_msg_getDeliveryMode(self._msg_p, ctypes.byref(mode))
        return mode.value

    def set_delivery_mode(self, mode):
        return solace.CORE_LIB.solClient_msg_setDeliveryMode(self._msg_p, c_uint32(mode))
