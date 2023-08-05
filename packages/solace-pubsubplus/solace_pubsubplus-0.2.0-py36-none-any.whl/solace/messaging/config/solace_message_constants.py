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


# this module contains the exception messages used through out project scope   #pylint: disable=missing-module-docstring

SOLCLIENT_LIBRARY_MISSING = "Core library unavailable"
UNABLE_TO_LOAD_SOLCLIENT_LIBRARY = "Unable to load core library"

MESSAGE_SENDING_FAILED = "Failed to send message"
SET_DESTINATION_FAILED = "Failed to set destination"
BINARY_STRING_ATTACHMENT_FAILED = "Failed to create binary string attachment"
MEMORY_ALLOCATION_FAILED = "Unable to allocate solClient message"

QUEUE_FULL_EXCEPTION_MESSAGE = "QUEUE full."

TOPIC_UNAVAILABLE = "Topic unavailable"

PUBLISHER_CANNOT_BE_STARTED_EXCEPTION_MESSAGE = "Publisher can't be started," \
                                                " before it is connected to a messaging service"
UNABLE_TO_PUBLISH_MESSAGE = "Unable to Publish message."
PUBLISHER_NOT_STARTED = f"{UNABLE_TO_PUBLISH_MESSAGE} Publisher not started."
PUBLISHER_TERMINATED = f"{UNABLE_TO_PUBLISH_MESSAGE} Publisher terminated."
PUBLISHER_TERMINATING = f"{UNABLE_TO_PUBLISH_MESSAGE} Publisher terminating"
PUBLISHER_NOT_READY = f"{UNABLE_TO_PUBLISH_MESSAGE} Publisher is not ready to publish message at this moment."
PUBLISH_FAILED_MESSAGING_SERVICE_NOT_CONNECTED = f"{UNABLE_TO_PUBLISH_MESSAGE} Messaging service not connected."
DELIVERY_LISTENER_SERVICE_DOWN_EXIT_MESSAGE = "Service down exiting the delivery listener thread"
PUBLISHER_SERVICE_DOWN_EXIT_MESSAGE = "Service down exiting the PUBLISHER thread"
RECEIVER_SERVICE_DOWN_EXIT_MESSAGE = "Service down exiting the RECEIVER thread"
PUBLISHER_TERMINATED = "Publisher terminated"
PERSISTENT_PUBLISHER_TERMINATED = f"Persistent {PUBLISHER_TERMINATED}"
STATE_CHANGE_LISTENER_SERVICE_DOWN_EXIT_MESSAGE = "Service down exiting the state change listener thread"
PUBLISHER_READINESS_SERVICE_DOWN_EXIT_MESSAGE = "Service down exiting the PUBLISHER readiness thread"
RECEIVER_CANNOT_BE_STARTED_EXCEPTION_MESSAGE = "Receiver can't be started before it is connected to a messaging service"
UNABLE_TO_RECEIVE_MESSAGE = "Unable to Receive message."
RECEIVER_NOT_STARTED = f"{UNABLE_TO_RECEIVE_MESSAGE} Receiver not started."
RECEIVER_TERMINATED = f"{UNABLE_TO_RECEIVE_MESSAGE} Receiver terminated."
CANNOT_START_RECEIVER = "Receiver can't be started before it is connected to a messaging service"

INCOMPATIBLE_MESSAGE = "Incompatible message, provided converter can't be used"
INVALID_PROPERTY_KEY = "The property key can not be None or empty"
INVALID_PROPERTY_VALUE = "The property value can not be None"
EMPTY_PROPERTY_VALUE = "The property value can not be empty"

UNABLE_TO_SUBSCRIBE_TO_TOPIC = "Unable to subscribe Topic"
UNABLE_TO_UNSUBSCRIBE_TO_TOPIC = "Unable to unsubscribe Topic"
TOPIC_NAME_TOO_LONG = "Invalid topic: Too long (encoding must be <= 250 bytes)"
QUEUE_NAME_TOO_LONG = "Invalid queue: Too long Queue Name, it cannot be longer than 200 characters"
TOPIC_NAME_CANNOT_BE_EMPTY = "Topic cannot be empty string"
TOPICSUBSCRIPTION_NAME_CANNOT_BE_EMPTY = "TopicSubscription cannot be empty string"
MAX_QUEUE_LIMIT_REACHED = "Queue maximum limit is reached"
FAILED_TO_SHUTDOWN_GRACEFULLY = "Failed to shutdown gracefully"

ESTABLISH_SESSION_ON_HOST = 'ESTABLISH SESSION ON HOST'
SESSION_CREATION_FAILED = "SESSION CREATION UNSUCCESSFUL."
TCP_CONNECTION_FAILURE = f"{SESSION_CREATION_FAILED} TCP connection failure, Connection refused."
FAILED_TO_LOAD_TRUST_STORE = f"{SESSION_CREATION_FAILED} Failed to load trust store."
FAILED_TO_LOADING_CERTIFICATE_AND_KEY = f"{SESSION_CREATION_FAILED} Failed to load certificate."
UNTRUSTED_CERTIFICATE_MESSAGE = f"{SESSION_CREATION_FAILED} Untrusted certificate."
WOULD_BLOCK_EXCEPTION_MESSAGE = f"{UNABLE_TO_PUBLISH_MESSAGE}. Would block exception occurred"

RECONNECTION_LISTENER_SHOULD_BE_TYPE_OF = "Reconnection listener should be an instance of "
RECONNECTION_ATTEMPT_LISTENER_SHOULD_BE_TYPE_OF = "Reconnection attempt listener should be an instance of "

INTERRUPTION_LISTENER_SHOULD_BE_TYPE_OF = "Service Interruption listener should be an instance of"

BAD_CREDENTIALS = "The username or password is incorrect"
UNRESOLVED_SESSION = 'Could not be resolved from session'
BAD_HOST_OR_PORT = "Service can't be reached using provided host and port"
NO_VALID_SMF_HEADER_MAPPING = "Could not read valid SMF Header from network"
NOT_BYTES_TO_READ_MAPPING = "Unable to read enough bytes from stream!"
EXCEPTION_NULL = "Exception can't be null"
SESSION_FORCE_DISCONNECT = "Session is being forcefully disconnected"

CCSMP_CALLER_DESC = 'caller_description'
CCSMP_RETURN_CODE = 'return_code'
CCSMP_SUB_CODE = 'sub_code'
CCSMP_INFO_SUB_CODE = 'error_info_sub_code'
CCSMP_INFO_CONTENTS = 'error_info_contents'

CCSMP_CERTIFICATE_ERROR = "certificate verify failed"
CCSMP_TCP_CONNECTION_FAILURE = "TCP connection failure"

CCSMP_SUB_CODE_UNRESOLVED_HOST = "SOLCLIENT_SUBCODE_UNRESOLVED_HOST"
CCSMP_SUB_CODE_INTERNAL_ERROR = "SOLCLIENT_SUBCODE_INTERNAL_ERROR"
CCSMP_SUB_CODE_UNTRUSTED_COMMONNAME = "SOLCLIENT_SUBCODE_UNTRUSTED_COMMONNAME"
CCSMP_SUB_CODE_LOGIN_FAILURE = "SOLCLIENT_SUBCODE_LOGIN_FAILURE"
CCSMP_SUB_CODE_FAILED_TO_LOAD_TRUST_STORE = "SOLCLIENT_SUBCODE_FAILED_LOADING_TRUSTSTORE"
CCSMP_SUB_CODE_FAILED_LOADING_CERTIFICATE_AND_KEY = "SOLCLIENT_SUBCODE_FAILED_LOADING_CERTIFICATE_AND_KEY"
CCSMP_SUBCODE_UNTRUSTED_CERTIFICATE = "SOLCLIENT_SUBCODE_UNTRUSTED_CERTIFICATE"
CCSMP_SUB_CODE_OK = "SOLCLIENT_SUBCODE_OK"
CCSMP_SUBCODE_COMMUNICATION_ERROR = 'SOLCLIENT_SUBCODE_COMMUNICATION_ERROR'
CCSMP_SUBCODE_SUBCODE_UNKNOWN_QUEUE_NAME = 'SOLCLIENT_SUBCODE_UNKNOWN_QUEUE_NAME'
CCSMP_SUBCODE_PARAM_OUT_OF_RANGE = 'SOLCLIENT_SUBCODE_PARAM_OUT_OF_RANGE'
CCSMP_SUBCODE_DATA_OTHER = 'SOLCLIENT_SUBCODE_DATA_OTHER'

STATS_ERROR = "FAILED TO RETRIEVE THE STATISTICS"

VALUE_CANNOT_BE_NEGATIVE = "Value cannot be negative "
VALUE_OUT_OF_RANGE = 'Value is out of range '

SHARE_NAME_CANT_BE_NONE = "ShareName can't be none"
SHARE_NAME_ILLEGAL_CHAR_ERROR_MESSAGE = "Literals '>' and '*' are not permitted in a ShareName"

NOT_FOUND_MESSAGE = "Not Found"
FAILED_TO_RETRIEVE = "Failed to retrieve"
FAILED_TO_GET_APPLICATION_TYPE = 'Unable to get application message type.'

UNSUPPORTED_METRIC_TYPE = "Unsupported metric value type."
ERROR_WHILE_RETRIEVING_METRIC = "Error while retrieving API metric."
INVALID_DATATYPE = "Invalid datatype"
BROKER_MANDATORY_KEY_MISSING_ERROR_MESSAGE = "Mandatory broker properties are missing. Try adding these missing keys :"

MISSING_BUFFER_CAPACITY = "Missing buffer capacity"
ILLEGAL_BUFFER_CAPACITY = "Illegal buffer capacity"
MISSING_BUFFER_TIMEOUT = "Missing buffer timeout"
ILLEGAL_BUFFER_TIMEOUT = "Illegal buffer timeout"
ILLEGAL_CONNECTION_RETRIES = "Illegal connection retries"
ILLEGAL_CONNECTION_ATTEMPTS_TIMEOUT = "Illegal connection attempts timeout"
ILLEGAL_RECONNECTION_RETRIES = "Illegal reconnection retries"
ILLEGAL_RECONNECTION_ATTEMPTS_WAIT_INTERVAL = "Illegal reconnection attempt wait interval"
ILLEGAL_COMPRESSION_LEVEL = "Illegal compression level"
DISPATCH_FAILED = "Failed to dispatch the callback"
HOSTNAME_MISMATCH = "Hostname mismatch"
IP_ADDRESS_MISMATCH = "IP address mismatch"
UNKNOWN_QUEUE = 'Unknown Queue'

UNCLEANED_TERMINATION_EXCEPTION_MESSAGE = "Failed to publish messages, publisher terminated"
DISCARD_INDICATION_FALSE = "Has discard indication!: [0]"

FLOW_PAUSE = "Flow paused after reaching internal threshold upper limit"

FLOW_RESUME = "Flow resumed after reaching internal threshold lower limit"

NO_INCOMING_MESSAGE = "No incoming message"
