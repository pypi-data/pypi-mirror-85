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


# contains return codes for underlying c api   # pylint: disable=missing-module-docstring, trailing-whitespace

import enum

SOLCLIENT_NOT_SET_PRIORITY_VALUE = -1
# The default log filter
SOLCLIENT_LOG_DEFAULT_FILTER = 5

# Normal return - the message is destroyed by the API upon return.
SOLCLIENT_CALLBACK_OK = 0

# The API call was successful.
SOLCLIENT_OK = 0

# The API call would block but non-blocking was requested.
SOLCLIENT_WOULD_BLOCK = 1

# An API call is in progress (non-blocking mode).
SOLCLIENT_IN_PROGRESS = 2

# The API could not complete as an object is not ready
SOLCLIENT_NOT_READY = 3

# (for example the Session is not connected).
# A getNext on a structured container returned End-of-Stream.
SOLCLIENT_EOS = 4

# A get for a named field in a MAP was not found in the MAP.
SOLCLIENT_NOT_FOUND = 5

# solClient_context_processEventsWait returns this if wait
SOLCLIENT_NOEVENT = 6

# The API call completed some but not all of the requested function.
SOLCLIENT_INCOMPLETE = 7

# solClient_transactedSession_commit returns this when the
SOLCLIENT_ROLLBACK = 8

# The API call failed.
SOLCLIENT_FAIL = -1

# Delivery Mode Types
SOLCLIENT_DELIVERY_MODE_DIRECT = 0  # Send a Direct message (0x00).
SOLCLIENT_DELIVERY_MODE_PERSISTENT = 16  # Send a Persistent message (0x10).
SOLCLIENT_DELIVERY_MODE_NONPERSISTENT = 32  # Send a Non-Persistent message (0x20).

SOLCLIENT_NULL_DESTINATION = -1
SOLCLIENT_TOPIC_DESTINATION = 0
SOLCLIENT_QUEUE_DESTINATION = 1
SOLCLIENT_TOPIC_TEMP_DESTINATION = 2
SOLCLIENT_QUEUE_TEMP_DESTINATION = 3

# Callback on the dispatch function immediately when a message arrives
SOLCLIENT_DISPATCH_TYPE_CALLBACK = 1

# The subscribe/unsubscribe call blocks until a confirmation is received.
SOLCLIENT_SUBSCRIBE_FLAGS_WAITFORCONFIRM = 0x02

# This flag indicates the subscription should only be added to
SOLCLIENT_SUBSCRIBE_FLAGS_LOCAL_DISPATCH_ONLY = 0x08

# Requests a confirmation for the subscribe/unsubscribe operation.
SOLCLIENT_SUBSCRIBE_FLAGS_REQUEST_CONFIRM = 0x10

# The application is keeping the rxMsg and it must not be released or reused by the API
SOLCLIENT_CALLBACK_TAKE_MSG = 1

MAX_SESSION_PROPS = 60
MAX_RETRY_INTERVAL_MS = 60000
DEFAULT_RECONNECT_RETRY_INTERVAL_TIMER_MS = 3000
SOLCLIENT_SESSION_PROP_AUTHENTICATION_SCHEME_CLIENT_CERTIFICATE = "AUTHENTICATION_SCHEME_CLIENT_CERTIFICATE"
SOLCLIENT_SESSION_PROP_AUTHENTICATION_SCHEME_BASIC = "AUTHENTICATION_SCHEME_BASIC"
SOLCLIENT_SESSION_PROP_DEFAULT_COMPRESSION_LEVEL = 0  # The default compression level (no compression)

# The value used to enable the property
SOLCLIENT_PROP_ENABLE_VAL = "1"

# The value used to disable the property
SOLCLIENT_PROP_DISABLE_VAL = "0"
ENCODING_TYPE = "utf-8"

# The Session is established.
SOLCLIENT_SESSION_EVENT_UP_NOTICE = 0

# The Session was established and then went down.
SOLCLIENT_SESSION_EVENT_DOWN_ERROR = 1

# The Session attempted to connect but was unsuccessful.
SOLCLIENT_SESSION_EVENT_CONNECT_FAILED_ERROR = 2

# The appliance rejected a published message.
SOLCLIENT_SESSION_EVENT_REJECTED_MSG_ERROR = 3

# The appliance rejected a subscription (add or remove).
SOLCLIENT_SESSION_EVENT_SUBSCRIPTION_ERROR = 4

# The API discarded a received message that exceeded the Session buffer size.
SOLCLIENT_SESSION_EVENT_RX_MSG_TOO_BIG_ERROR = 5

# The oldest transmitted Persistent/Non-Persistent message that has been acknowledged.
SOLCLIENT_SESSION_EVENT_ACKNOWLEDGEMENT = 6

# Deprecated
# solClient_session_startAssuredPublishing. The AD Handshake (that is Guaranteed Delivery handshake) has completed
# for the publisher and Guaranteed messages can be sent.
SOLCLIENT_SESSION_EVENT_ASSURED_PUBLISHING_UP = 7

# Deprecated
# solClient_session_startAssuredPublishing. The appliance rejected the AD Handshake to start Guaranteed publishing.
# Use ::SOLCLIENT_SESSION_EVENT_ASSURED_DELIVERY_DOWN instead.
SOLCLIENT_SESSION_EVENT_ASSURED_CONNECT_FAILED = 8

# Guaranteed Delivery publishing is not available.
# The guaranteed delivery capability on the session has been disabled by some action on the appliance.
SOLCLIENT_SESSION_EVENT_ASSURED_DELIVERY_DOWN = 8

# The Topic Endpoint unsubscribe command failed.
SOLCLIENT_SESSION_EVENT_TE_UNSUBSCRIBE_ERROR = 9

# Deprecated name: SOLCLIENT_SESSION_EVENT_TE_UNSUBSCRIBE_ERROR is preferred
SOLCLIENT_SESSION_EVENT_DTE_UNSUBSCRIBE_ERROR = SOLCLIENT_SESSION_EVENT_TE_UNSUBSCRIBE_ERROR

# The Topic Endpoint unsubscribe completed.
SOLCLIENT_SESSION_EVENT_TE_UNSUBSCRIBE_OK = 10

# Deprecated name: SOLCLIENT_SESSION_EVENT_TE_UNSUBSCRIBE_OK is preferred
SOLCLIENT_SESSION_EVENT_DTE_UNSUBSCRIBE_OK = SOLCLIENT_SESSION_EVENT_TE_UNSUBSCRIBE_OK

# The send is no longer blocked.
SOLCLIENT_SESSION_EVENT_CAN_SEND = 11

# The Session has gone down and an automatic reconnect attempt is in progress.
SOLCLIENT_SESSION_EVENT_RECONNECTING_NOTICE = 12

# The automatic reconnect of the Session was successful and the Session was established again.
SOLCLIENT_SESSION_EVENT_RECONNECTED_NOTICE = 13

# The endpoint create/delete command failed.
SOLCLIENT_SESSION_EVENT_PROVISION_ERROR = 14

# The endpoint create/delete command completed.
SOLCLIENT_SESSION_EVENT_PROVISION_OK = 15

# The subscribe or unsubscribe operation has succeeded.
SOLCLIENT_SESSION_EVENT_SUBSCRIPTION_OK = 16

# The appliance's Virtual Router Name changed during a reconnect operation.
# This could render existing queues or temporary topics invalid.
SOLCLIENT_SESSION_EVENT_VIRTUAL_ROUTER_NAME_CHANGED = 17

# The session property modification completed.
SOLCLIENT_SESSION_EVENT_MODIFYPROP_OK = 18

# The session property modification failed.
SOLCLIENT_SESSION_EVENT_MODIFYPROP_FAIL = 19

# After successfully reconnecting a disconnected
# session the SDK received an unknown publisher flow name response when reconnecting the GD publisher flow.
# If configured to auto-retry (See ::SOLCLIENT_SESSION_PROP_GD_RECONNECT_FAIL_ACTION.) this event is generated
# to indicate how many unacknowledged messages are retransmitted on success. As the publisher state has been lost
# on failover receiving this event may indicate that some messages have been duplicated in the system.
SOLCLIENT_SESSION_EVENT_REPUBLISH_UNACKED_MESSAGES = 20

SOLCLIENT_SENT_STATS = 'SOLCLIENT_STATS_TX_NUM_STATS'
SOLCLIENT_RECEIVED_STATS = 'SOLCLIENT_STATS_RX_NUM_STATS'

# solClient_msg_dumpExt mode flags
SOLCLIENT_MSGDUMP_FULL = 1  # Display the entire message
SOLCLIENT_MSGDUMP_BRIEF = 0  # Display only the length of the binary attachment, XML attachment, and user property map

DEFAULT_BUFFER_SIZE = 1000
DEFAULT_BUFFER_MULTIPLIER = 3

PUBLISHER_BACK_PRESSURE_STRATEGY_ELASTIC = "ELASTIC"
PUBLISHER_BACK_PRESSURE_STRATEGY_BUFFER_REJECT_WHEN_FULL = "BUFFER_REJECT_WHEN_FULL"
PUBLISHER_BACK_PRESSURE_STRATEGY_BUFFER_WAIT_WHEN_FULL = "BUFFER_WAIT_WHEN_FULL"


class SOLCLIENTSTATSTX(enum.Enum):
    """
    #  Transmit statistics (64-bit counters). Index into array of transmit statistics equivalent to solClient_stats_tx.
    """
    SOLCLIENT_STATS_TX_TOTAL_DATA_BYTES = 0  # The number of data bytes transmitted in total.
    SOLCLIENT_STATS_TX_BYTES = SOLCLIENT_STATS_TX_TOTAL_DATA_BYTES  # Deprecated name; ::
    # SOLCLIENT_STATS_TX_TOTAL_DATA_BYTES is preferred
    SOLCLIENT_STATS_TX_TOTAL_DATA_MSGS = 1  # The number of data messages transmitted in total.
    SOLCLIENT_STATS_TX_MSGS = SOLCLIENT_STATS_TX_TOTAL_DATA_MSGS  # Deprecated name; ::SOLCLIENT_
    # STATS_TX_TOTAL_DATA_MSGS is preferred
    SOLCLIENT_STATS_TX_WOULD_BLOCK = 2  # The number of messages not accepted due to would block (non-blocking only).
    SOLCLIENT_STATS_TX_SOCKET_FULL = 3  # The number of times the socket was full when send done (data buffered).
    SOLCLIENT_STATS_TX_DIRECT_BYTES = 4  # The number of bytes transmitted in Direct messages.
    SOLCLIENT_STATS_TX_DIRECT_MSGS = 5  # The number of Direct messages transmitted.
    SOLCLIENT_STATS_TX_PERSISTENT_BYTES = 6  # The number of bytes transmitted in Persistent messages.
    SOLCLIENT_STATS_TX_NONPERSISTENT_BYTES = 7  # The number of bytes transmitted in Non-Persistent messages.
    SOLCLIENT_STATS_TX_PERSISTENT_MSGS = 8  # The number of Persistent messages transmitted.
    SOLCLIENT_STATS_TX_NONPERSISTENT_MSGS = 9  # The number of Non-Persistent messages transmitted.
    SOLCLIENT_STATS_TX_PERSISTENT_REDELIVERED = 10  # The number of Persistent messages redelivered.
    SOLCLIENT_STATS_TX_NONPERSISTENT_REDELIVERED = 11  # The number of Non-Persistent messages redelivered.
    SOLCLIENT_STATS_TX_PERSISTENT_BYTES_REDELIVERED = 12  # The number of bytes redelivered in Persistent messages.
    SOLCLIENT_STATS_TX_NONPERSISTENT_BYTES_REDELIVERED = 13  # The number of bytes redelivered in
    # Non-Persistent messages.
    SOLCLIENT_STATS_TX_ACKS_RXED = 14  # The number of acknowledgments received.
    SOLCLIENT_STATS_TX_WINDOW_CLOSE = 15  # The number of times the transmit window closed.
    SOLCLIENT_STATS_TX_ACK_TIMEOUT = 16  # The number of times the acknowledgment timer expired.
    SOLCLIENT_STATS_TX_CTL_MSGS = 17  # The number of control (non-data) messages transmitted.
    SOLCLIENT_STATS_TX_CTL_BYTES = 18  # The number of bytes transmitted in control (non-data) messages.
    SOLCLIENT_STATS_TX_COMPRESSED_BYTES = 19  # The number of bytes transmitted after compression.
    SOLCLIENT_STATS_TX_TOTAL_CONNECTION_ATTEMPTS = 20  # The total number of TCP connections attempted by
    # this Session.
    SOLCLIENT_STATS_TX_REQUEST_SENT = 21  # The request messages sent.
    SOLCLIENT_STATS_TX_REQUEST_TIMEOUT = 22  # The request messages sent that did not receive a reply due to timeout.
    SOLCLIENT_STATS_TX_CACHEREQUEST_SENT = 23  # The cache requests sent.
    SOLCLIENT_STATS_TX_GUARANTEED_MSGS_SENT_CONFIRMED = 24  # Guaranteed messages (Persistent/Non-Persistent)
    # published that have been acknowledged.
    SOLCLIENT_STATS_TX_DISCARD_NO_MATCH = 25  # When the IPC add-on is in use  the counter of messages
    # discarded due to no subscription match with connected peers
    SOLCLIENT_STATS_TX_DISCARD_CHANNEL_ERROR = 26  # Messages discarded due to channel failure
    SOLCLIENT_STATS_TX_BLOCKED_ON_SEND = 27  # The number of times Session blocked on socket
    # full (blocking only) occurred.
    SOLCLIENT_STATS_TX_NUM_STATS = 28  # The size of transmit stats array.


class SOLCLIENTSTATSRX(enum.Enum):
    """
    Receive statistics (64-bit counters). Index into array of receive statistics equivalent of solClient_stats_rx
    """
    SOLCLIENT_STATS_RX_DIRECT_BYTES = 0  # The number of bytes received.
    SOLCLIENT_STATS_RX_BYTES = SOLCLIENT_STATS_RX_DIRECT_BYTES  # Deprecated name
    # ::SOLCLIENT_STATS_RX_DIRECT_BYTES is preferred
    SOLCLIENT_STATS_RX_DIRECT_MSGS = 1  # The number of messages received.
    SOLCLIENT_STATS_RX_MSGS = SOLCLIENT_STATS_RX_DIRECT_MSGS  # Deprecated name
    # ::SOLCLIENT_STATS_RX_DIRECT_MSGS is preferred.
    SOLCLIENT_STATS_RX_READS = 2  # The number of non-empty reads.
    SOLCLIENT_STATS_RX_DISCARD_IND = 3  # The number of receive messages with discard indication set.
    SOLCLIENT_STATS_RX_DISCARD_SMF_UNKNOWN_ELEMENT = 4  # The number of messages discarded due to the presence of
    # an unknown element or unknown protocol in the Solace Message Format (SMF) header.
    SOLCLIENT_STATS_RX_DISCARD_MSG_HDR_ERROR = SOLCLIENT_STATS_RX_DISCARD_SMF_UNKNOWN_ELEMENT  # Deprecated  use
    # the more accurately named SOLCLIENT_STATS_RX_DISCARD_SMF_UNKNOWN_ELEMENT instead.
    SOLCLIENT_STATS_RX_DISCARD_MSG_TOO_BIG = 5  # The number of messages discarded due to msg too large.
    SOLCLIENT_STATS_RX_ACKED = 6  # The number of acknowledgments sent for Guaranteed messages.
    SOLCLIENT_STATS_RX_DISCARD_DUPLICATE = 7  # The number of Guaranteed messages dropped for being duplicates.
    SOLCLIENT_STATS_RX_DISCARD_NO_MATCHING_FLOW = 8  # The number of Guaranteed messages discarded due to no match on
    # the flowId.
    SOLCLIENT_STATS_RX_DISCARD_OUTOFORDER = 9  # The number of Guaranteed messages discarded for
    # being received out of order.
    SOLCLIENT_STATS_RX_PERSISTENT_BYTES = 10  # The number of Persistent bytes received on the Flow. On the Session
    # it is the total number of Persistent bytes received across all Flows.
    SOLCLIENT_STATS_RX_PERSISTENT_MSGS = 11  # The number of Persistent messages received on the Flow.
    # On the Session  it is the total number of Persistent messages received across all Flows.
    SOLCLIENT_STATS_RX_NONPERSISTENT_BYTES = 12  # The number of Persistent bytes received on the Flow.
    # On the Session  it is the total number of Persistent bytes received across all Flows.
    SOLCLIENT_STATS_RX_NONPERSISTENT_MSGS = 13  # The number of Persistent messages received on the Flow.
    # On the Session  it is the total number of Persistent messages received across all Flows.
    SOLCLIENT_STATS_RX_CTL_MSGS = 14  # The number of control (non-data) messages received.
    SOLCLIENT_STATS_RX_CTL_BYTES = 15  # The number of bytes received in control (non-data) messages.
    SOLCLIENT_STATS_RX_TOTAL_DATA_BYTES = 16  # The total number of data bytes received.
    SOLCLIENT_STATS_RX_TOTAL_DATA_MSGS = 17  # The total number of data messages received.
    SOLCLIENT_STATS_RX_COMPRESSED_BYTES = 18  # The number of bytes received before decompression.
    SOLCLIENT_STATS_RX_REPLY_MSG = 19  # The reply messages received.
    SOLCLIENT_STATS_RX_REPLY_MSG_DISCARD = 20  # The reply messages (including cache request response) discarded due
    # to errors in response format or no outstanding request.
    SOLCLIENT_STATS_RX_CACHEREQUEST_OK_RESPONSE = 21  # Cache requests completed OK.
    SOLCLIENT_STATS_RX_CACHEREQUEST_FULFILL_DATA = 22  # Cache requests fulfilled by live data.
    SOLCLIENT_STATS_RX_CACHEREQUEST_ERROR_RESPONSE = 23  # Cache requests failed due to solCache error response.
    SOLCLIENT_STATS_RX_CACHEREQUEST_DISCARD_RESPONSE = 24  # Cache request response discarded due to errors in
    # response format or no outstanding cache request.
    SOLCLIENT_STATS_RX_CACHEMSG = 25  # Cached messages delivered to application.
    SOLCLIENT_STATS_RX_FOUND_CTSYNC = 26  # On a cut-through Flow  the number of times the Flow entered
    # cut-through delivery mode.
    SOLCLIENT_STATS_RX_LOST_CTSYNC = 27  # On a cut-through Flow  the number of times the Flow left cut-through
    # delivery mode to resynchronize with the Guaranteed message storage on the appliance
    SOLCLIENT_STATS_RX_LOST_CTSYNC_GM = 28  # On a cut-through Flow  the number of times the Flow left
    # cut-through delivery mode to resynchronize with the Guaranteed message storage due to receiving a
    # Guaranteed message that was not previously received as Direct.
    SOLCLIENT_STATS_RX_OVERFLOW_CTSYNC_BUFFER = 29  # On a cut-through Flow  the number of times the
    # synchronization buffer overflowed  delaying synchronization.
    SOLCLIENT_STATS_RX_ALREADY_CUT_THROUGH = 30  # On a cut-through Flow  the number of Guaranteed messages
    # discarded because they had already been received on the cut-through Flow.
    SOLCLIENT_STATS_RX_DISCARD_FROM_CTSYNC = 31  # On a cut-through Flow  the number of messages discarded
    # from the synchronization list other than those discarded due to overflow.
    SOLCLIENT_STATS_RX_DISCARD_MSG_FLOW_UNBOUND_PENDING = 32  # On a transacted flow  the number of messages
    # discarded because the flow is in a UNBOUND pending state.
    SOLCLIENT_STATS_RX_DISCARD_MSG_TRANSACTION_ROLLBACK = 33  # On a transacted flow  the number of messages
    # discarded after a transaction rollback and becomes a message comes in with prevMsgId=0.
    SOLCLIENT_STATS_RX_DISCARD_TRANSACTION_RESPONSE = 34  # On a transacted session  the number of transaction
    # responses discarded due to reconnection.
    SOLCLIENT_STATS_RX_SSL_READ_EVENTS = 35
    SOLCLIENT_STATS_RX_SSL_READ_CALLS = 36
    SOLCLIENT_STATS_RX_NUM_STATS = 37  # The size of receive stats array.


SOLCLIENT_FLOW_PROP_DEFAULT_ACTIVE_FLOW_IND = SOLCLIENT_PROP_DISABLE_VAL  # The default value for the
# ::SOLCLIENT_FLOW_PROP_ACTIVE_FLOW_IND property.

# Flow Bind Entities

SOLCLIENT_FLOW_PROP_BIND_ENTITY_SUB = "1"  # A bind target of subscriber
SOLCLIENT_FLOW_PROP_BIND_ENTITY_QUEUE = "2"  # A bind target of Queue
SOLCLIENT_FLOW_PROP_BIND_ENTITY_TE = "3"  # A bind target of Topic Endpoint
SOLCLIENT_FLOW_PROP_BIND_ENTITY_DTE = SOLCLIENT_FLOW_PROP_BIND_ENTITY_TE  # Deprecated name
# ; ::SOLCLIENT_FLOW_PROP_BIND_ENTITY_TE is preferred 

# Flow Acknowledgment Modes

SOLCLIENT_FLOW_PROP_ACKMODE_AUTO = "1"  # Automatic application acknowledgment of all received messages.
# If application calls ::solClient_flow_sendAck() in the ::SOLCLIENT_FLOW_PROP_ACKMODE_AUTO mode,
# a warning is generated.
SOLCLIENT_FLOW_PROP_ACKMODE_CLIENT = "2"  # Client must call solClient_flow_sendAck() to
# acknowledge the msgId specified.


# Flow Configuration Properties
SOLCLIENT_FLOW_PROP_BIND_ENTITY_ID = "FLOW_BIND_ENTITY_ID"  # The type of object to which this
# Flow is bound. The valid values are ::SOLCLIENT_FLOW_PROP_BIND_ENTITY_SUB, ::SOLCLIENT_FLOW_PROP_BIND_ENTITY_QUEUE,
# and ::SOLCLIENT_FLOW_PROP_BIND_ENTITY_TE. Default: ::SOLCLIENT_FLOW_PROP_DEFAULT_BIND_ENTITY_ID 

SOLCLIENT_FLOW_PROP_BIND_ENTITY_DURABLE = "FLOW_BIND_ENTITY_DURABLE"  # The durability of the
# object to which this Flow is bound. Default: ::SOLCLIENT_PROP_ENABLE_VAL, which means the endpoint is durable. 
# When set to SOLCLIENT_PROP_DISABLE_VAL, a temporary endpoint is created. 

SOLCLIENT_FLOW_PROP_BIND_NAME = "FLOW_BIND_NAME"  # The name of the Queue or Topic Endpoint that is the target
# of the bind. This property is ignored when the BIND_ENTITY_ID is ::SOLCLIENT_FLOW_PROP_BIND_ENTITY_SUB. 
# The maximum length (not including NULL terminator) is ::SOLCLIENT_BUFINFO_MAX_QUEUENAME_SIZE except for 
# durable queues, which has a limit of ::SOLCLIENT_BUFINFO_MAX_DURABLE_QUEUENAME_SIZE
# . Default: ::SOLCLIENT_FLOW_PROP_DEFAULT_BIND_NAME 

SOLCLIENT_FLOW_PROP_ACKMODE = "FLOW_ACKMODE"  # Controls how acknowledgments are generated
# for received Guaranteed messages. Possible values are ::SOLCLIENT_FLOW_PROP_ACKMODE_AUTO
# and ::SOLCLIENT_FLOW_PROP_ACKMODE_CLIENT. Default ::SOLCLIENT_FLOW_PROP_ACKMODE_AUTO 

SOLCLIENT_FLOW_PROP_ACTIVE_FLOW_IND = "FLOW_ACTIVE_FLOW_IND"  # When a Flow has the Active
# Flow Indication property enabled, the application will receive flow events when the flow becomes
# active, or inactive.  If the underlying session capabilities indicate that the appliance does not
# support active flow indications, then solClient_session_createFlow() will fail immediately (SOLCLIENT_FAIL)
# and set the subCode SOLCLIENT_SUBCODE_FLOW_ACTIVE_FLOW_INDICATION_UNSUPPORTED.
# Default: ::SOLCLIENT_FLOW_PROP_DEFAULT_ACTIVE_FLOW_IND 


SOLCLIENT_ENDPOINT_PROP_ACCESSTYPE_NONEXCLUSIVE = "0"  # A non-exclusive (shared) Queue. Each client to bind
# receives messages in a round robin fashion.
SOLCLIENT_ENDPOINT_PROP_ACCESSTYPE_EXCLUSIVE = "1"  # An exclusive Queue. The first client to bind receives
# the stored messages on the Endpoint.

# Endpoint Naming Entities, used as values for ENDPOINT properties in 
# solClient_session_endpointProvision()/solClient_session_endpointDeprovision(), in solClient_session_createFlow(), and
# in solClient_session_endpointTopicSubscribe() / solClient_session_endpointTopicUnsubscribe().

SOLCLIENT_ENDPOINT_PROP_QUEUE = "2"  # Request is for a Queue.
SOLCLIENT_ENDPOINT_PROP_TE = "3"  # Request is for a Topic Endpoint.
SOLCLIENT_ENDPOINT_PROP_CLIENT_NAME = "4"  # Request is for a Client name

#  Items that can be configured for a create endpoint operation.
SOLCLIENT_ENDPOINT_PROP_ID = "ENDPOINT_ID"  # The type of endpoint, the valid
# values are ::SOLCLIENT_ENDPOINT_PROP_QUEUE, ::SOLCLIENT_ENDPOINT_PROP_TE,
# and ::SOLCLIENT_ENDPOINT_PROP_CLIENT_NAME. Default: ::SOLCLIENT_ENDPOINT_PROP_TE 
SOLCLIENT_ENDPOINT_PROP_NAME = "ENDPOINT_NAME"  # The name of the Queue or Topic endpoint
# as a NULL-terminated UTF-8 encoded string. 
SOLCLIENT_ENDPOINT_PROP_DURABLE = "ENDPOINT_DURABLE"  # The durability of the endpoint to name.
# Default: ::SOLCLIENT_PROP_ENABLE_VAL, which means the endpoint is durable.
# Only ::SOLCLIENT_PROP_ENABLE_VAL is supported in solClient_session_endpointProvision().
# This property is ignored in solClient_session_creatFlow(). 
SOLCLIENT_ENDPOINT_PROP_PERMISSION = "ENDPOINT_PERMISSION"
SOLCLIENT_ENDPOINT_PROP_ACCESSTYPE = "ENDPOINT_ACCESSTYPE"  # Sets the access type for the endpoint.
# This applies to durable Queues only. 
# Provision Flags
# The provision operation may be modified by the use of one or more of the following flags:
SOLCLIENT_PROVISION_FLAGS_WAITFORCONFIRM = (0x01)  # The provision operation blocks until it has completed
# successfully on the appliance or failed.
SOLCLIENT_PROVISION_FLAGS_IGNORE_EXIST_ERRORS = (0x02)  # When set, it is not considered an error

# Endpoint Permissions

SOLCLIENT_ENDPOINT_PERM_NONE = "n"  # No permissions for other clients
SOLCLIENT_ENDPOINT_PERM_READ_ONLY = "r"  # Read-only permission  other clients may not consume messages.
SOLCLIENT_ENDPOINT_PERM_CONSUME = "c"  # Consumer permission  other clients may read and consume messages.
SOLCLIENT_ENDPOINT_PERM_MODIFY_TOPIC = "m"  # Modify Topic permission  other clients may read and
# consume messages, and modify Topic on a Topic Endpoint.
SOLCLIENT_ENDPOINT_PERM_DELETE = "d"  # Delete permission  other clients may read and consume


# messages, modify the Topic on a Topic Endpoint, and delete the endpoint.

# solClient_flow_event
# Flow events that can be given to the Flow event callback routine registered for
#  a Flow. The Flow event callback is registered when a Flow is created through 
# solClient_session_createFlow() and has the prototype ::solClient_flow_eventCallbackFunc_t.
# A Flow event can be converted to a string value through solClient_flow_eventToString().
class SolClientFlowEvent(enum.Enum):
    """SolClient Flow event enums"""
    SOLCLIENT_FLOW_EVENT_UP_NOTICE = 0  # The Flow is established
    SOLCLIENT_FLOW_EVENT_DOWN_ERROR = 1  # The Flow was established and then disconnected by the appliance,
    # likely due to operator intervention. The Flow must be destroyed
    SOLCLIENT_FLOW_EVENT_BIND_FAILED_ERROR = 2  # The Flow attempted to connect but was unsuccessful
    SOLCLIENT_FLOW_EVENT_REJECTED_MSG_ERROR = 3  # This event is deprecated and will never be raised
    SOLCLIENT_FLOW_EVENT_SESSION_DOWN = 4  # The Session for the Flow was disconnected. The Flow will
    # rebound automatically when the Session is reconnected.
    SOLCLIENT_FLOW_EVENT_ACTIVE = 5  # The flow has become active
    SOLCLIENT_FLOW_EVENT_INACTIVE = 6  # The flow has become inactive
    SOLCLIENT_FLOW_EVENT_RECONNECTING = 7  # The Flow was established and then disconnected by the broker,
    # due to operator action, either 'Replay Started' or 'shutdown' on the queue, topic endpoint, or message spool.
    # The API is attempting to reconnect the flow automatically
    SOLCLIENT_FLOW_EVENT_RECONNECTED = 8  # The Flow was successfully reconnected to the broker


class SolClientSubCode(enum.Enum):
    """SolClient sub code enums"""
    SOLCLIENT_SUBCODE_OK = 0  # No error.
    SOLCLIENT_SUBCODE_PARAM_OUT_OF_RANGE = 1  # An API call was made with an out-of-range parameter.
    SOLCLIENT_SUBCODE_PARAM_NULL_PTR = 2  # An API call was made with a null or invalid pointer parameter.
    SOLCLIENT_SUBCODE_PARAM_CONFLICT = 3  # An API call was made with a parameter combination that is not valid.
    SOLCLIENT_SUBCODE_INSUFFICIENT_SPACE = 4  # An API call failed due to insufficient space to accept more data.
    SOLCLIENT_SUBCODE_OUT_OF_RESOURCES = 5  # An API call failed due to lack of resources (for example, starting a
    # timer when all timers are in use).
    SOLCLIENT_SUBCODE_INTERNAL_ERROR = 6  # An API call had an internal error (not an application fault).
    SOLCLIENT_SUBCODE_OUT_OF_MEMORY = 7  # An API call failed due to inability to allocate memory.
    SOLCLIENT_SUBCODE_PROTOCOL_ERROR = 8  # An API call failed due to a protocol error with the appliance (not an
    # application fault).
    SOLCLIENT_SUBCODE_INIT_NOT_CALLED = 9  # An API call failed due to solClient_initialize() not being called first.
    SOLCLIENT_SUBCODE_TIMEOUT = 10  # An API call failed due to a timeout.
    SOLCLIENT_SUBCODE_KEEP_ALIVE_FAILURE = 11  # The Session Keep-Alive detected a failed Session.
    SOLCLIENT_SUBCODE_SESSION_NOT_ESTABLISHED = 12  # An API call failed due to the Session not being established.
    SOLCLIENT_SUBCODE_OS_ERROR = 13  # An API call failed due to a failed operating system call; an error string can
    # be retrieved with solClient_getLastErrorInfo().
    SOLCLIENT_SUBCODE_COMMUNICATION_ERROR = 14  # An API call failed due to a communication error. An error string
    # can be retrieved with solClient_getLastErrorInfo().
    SOLCLIENT_SUBCODE_USER_DATA_TOO_LARGE = 15  # An attempt was made to send a message with user data larger than
    # the maximum that is supported.
    SOLCLIENT_SUBCODE_TOPIC_TOO_LARGE = 16  # An attempt was made to use a Topic that is longer than the maximum that
    # is supported.
    SOLCLIENT_SUBCODE_INVALID_TOPIC_SYNTAX = 17  # An attempt was made to use a Topic that has a syntax which is not
    # supported.
    SOLCLIENT_SUBCODE_XML_PARSE_ERROR = 18  # The appliance could not parse an XML message.
    SOLCLIENT_SUBCODE_LOGIN_FAILURE = 19  # The client could not log into the appliance (bad username or password).
    SOLCLIENT_SUBCODE_INVALID_VIRTUAL_ADDRESS = 20  # An attempt was made to connect to the wrong IP address on the
    # appliance (must use CVRID if configured) or the appliance CVRID has changed and this was detected on reconnect.
    SOLCLIENT_SUBCODE_CLIENT_DELETE_IN_PROGRESS = 21  # The client login not currently possible as previous
    # instance of same client still being deleted.
    SOLCLIENT_SUBCODE_TOO_MANY_CLIENTS = 22  # The client login not currently possible because the maximum
    # number of active clients on appliance has already been reached.
    SOLCLIENT_SUBCODE_SUBSCRIPTION_ALREADY_PRESENT = 23  # The client attempted to add a subscription
    # which already exists. This subcode is only returned if the Session property
    # SOLCLIENT_SESSION_PROP_IGNORE_DUP_SUBSCRIPTION_ERROR is not enabled.
    SOLCLIENT_SUBCODE_SUBSCRIPTION_NOT_FOUND = 24  # The client attempted to remove a subscription
    # which did not exist. This subcode is only returned if the Session property
    # SOLCLIENT_SESSION_PROP_IGNORE_DUP_SUBSCRIPTION_ERROR is not enabled.
    SOLCLIENT_SUBCODE_SUBSCRIPTION_INVALID = 25  # The client attempted to add/remove a subscription that is not valid.
    SOLCLIENT_SUBCODE_SUBSCRIPTION_OTHER = 26  # The appliance rejected a subscription add or
    # remove request for a reason not separately enumerated.
    SOLCLIENT_SUBCODE_CONTROL_OTHER = 27  # The appliance rejected a control message for another
    # reason not separately enumerated.
    SOLCLIENT_SUBCODE_DATA_OTHER = 28  # The appliance rejected a data message for another reason
    # not separately enumerated.
    SOLCLIENT_SUBCODE_LOG_FILE_ERROR = 29  # Could not open the log file name specified by the application
    # for writing (Deprecated - ::SOLCLIENT_SUBCODE_OS_ERROR is used).
    SOLCLIENT_SUBCODE_MESSAGE_TOO_LARGE = 30  # The client attempted to send a message larger than that
    # supported by the appliance.
    SOLCLIENT_SUBCODE_SUBSCRIPTION_TOO_MANY = 31  # The client attempted to add a subscription
    # that exceeded the maximum number allowed.
    SOLCLIENT_SUBCODE_INVALID_SESSION_OPERATION = 32  # An API call failed due to the attempted
    # operation not being valid for the Session.
    SOLCLIENT_SUBCODE_TOPIC_MISSING = 33  # A send call was made that did not have a Topic in a
    # mode where one is required (for example, client mode).
    SOLCLIENT_SUBCODE_ASSURED_MESSAGING_NOT_ESTABLISHED = 34  # A send call was made to send a
    # Guaranteed message before Guaranteed Delivery is established (Deprecated).
    SOLCLIENT_SUBCODE_ASSURED_MESSAGING_STATE_ERROR = 35  # An attempt was made to start
    # Guaranteed Delivery when it is already started.
    SOLCLIENT_SUBCODE_QUEUENAME_TOPIC_CONFLICT = 36  # Both Queue Name and Topic are
    # specified in solClient_session_send.
    SOLCLIENT_SUBCODE_QUEUENAME_TOO_LARGE = 37  # An attempt was made to use a Queue
    # name which is longer than the maximum supported length.
    SOLCLIENT_SUBCODE_QUEUENAME_INVALID_MODE = 38  # An attempt was made to use a Queue
    # name on a non-Guaranteed message.
    SOLCLIENT_SUBCODE_MAX_TOTAL_MSGSIZE_EXCEEDED = 39  # An attempt was made to send a message
    # with a total size greater than that supported by the protocol.
    SOLCLIENT_SUBCODE_DBLOCK_ALREADY_EXISTS = 40  # An attempt was made to allocate a datablock
    # for a msg element when one already exists.
    SOLCLIENT_SUBCODE_NO_STRUCTURED_DATA = 41  # An attempt was made to create a container to
    # read structured data where none exists.
    SOLCLIENT_SUBCODE_CONTAINER_BUSY = 42  # An attempt was made to add a field to a map or stream
    # while a sub map or stream is being built.
    SOLCLIENT_SUBCODE_INVALID_DATA_CONVERSION = 43  # An attempt was made to retrieve structured data with wrong type.
    SOLCLIENT_SUBCODE_CANNOT_MODIFY_WHILE_NOT_IDLE = 44  # An attempt was made to modify a property
    # that cannot be modified while Session is not idle.
    SOLCLIENT_SUBCODE_MSG_VPN_NOT_ALLOWED = 45  # The Message VPN name set for the Session is not
    # allowed for the Session's username.
    SOLCLIENT_SUBCODE_CLIENT_NAME_INVALID = 46  # The client name chosen has been rejected as invalid by the appliance.
    SOLCLIENT_SUBCODE_MSG_VPN_UNAVAILABLE = 47  # The Message VPN name set for the Session
    # (or the default Message VPN, if none was set) is currently shutdown on the appliance.
    SOLCLIENT_SUBCODE_CLIENT_USERNAME_IS_SHUTDOWN = 48  # The username for the client is administratively
    # shutdown on the appliance.
    SOLCLIENT_SUBCODE_DYNAMIC_CLIENTS_NOT_ALLOWED = 49  # The username for the Session has not been set
    # and dynamic clients are not allowed.
    SOLCLIENT_SUBCODE_CLIENT_NAME_ALREADY_IN_USE = 50  # The Session is attempting to use a client,
    # publisher name, or subscriber name that is in use by another client, publisher, or subscriber,
    # and the appliance is configured to reject the new Session. When Message VPNs are in use, the conflicting
    # client name must be in the same Message VPN.
    SOLCLIENT_SUBCODE_CACHE_NO_DATA = 51  # When the cache request returns ::SOLCLIENT_INCOMPLETE,
    # this subcode indicates there is no cached data in the designated cache.
    SOLCLIENT_SUBCODE_CACHE_SUSPECT_DATA = 52  # When the designated cache responds to a cache request with
    # suspect data the API returns ::SOLCLIENT_INCOMPLETE with this subcode.
    SOLCLIENT_SUBCODE_CACHE_ERROR_RESPONSE = 53  # The cache instance has returned an error response to the request.
    SOLCLIENT_SUBCODE_CACHE_INVALID_SESSION = 54  # The cache session operation failed because the Session
    # has been destroyed.
    SOLCLIENT_SUBCODE_CACHE_TIMEOUT = 55  # The cache session operation failed because the request timeout expired.
    SOLCLIENT_SUBCODE_CACHE_LIVEDATA_FULFILL = 56  # The cache session operation completed when live data
    # arrived on the Topic requested.
    SOLCLIENT_SUBCODE_CACHE_ALREADY_IN_PROGRESS = 57  # A cache request has been made when there is already
    # a cache request outstanding on the same Topic and SOLCLIENT_CACHEREQUEST_FLAGS_LIVEDATA_FLOWTHRU was not set.
    SOLCLIENT_SUBCODE_MISSING_REPLY_TO = 58  # A message does not have the required reply-to field.
    SOLCLIENT_SUBCODE_CANNOT_BIND_TO_QUEUE = 59  # Already bound to the queue, or not authorized to bind to the queue.
    SOLCLIENT_SUBCODE_INVALID_TOPIC_NAME_FOR_TE = 60  # An attempt was made to bind to a Topic
    # Endpoint with an invalid topic.
    SOLCLIENT_SUBCODE_INVALID_TOPIC_NAME_FOR_DTE = SOLCLIENT_SUBCODE_INVALID_TOPIC_NAME_FOR_TE
    # Deprecated name; ::SOLCLIENT_SUBCODE_INVALID_TOPIC_NAME_FOR_TE is preferred.
    SOLCLIENT_SUBCODE_UNKNOWN_QUEUE_NAME = 61  # An attempt was made to bind to an unknown Queue name
    # (for example, not configured on appliance).
    SOLCLIENT_SUBCODE_UNKNOWN_TE_NAME = 62  # An attempt was made to bind to an unknown Topic Endpoint
    # name (for example, not configured on appliance).
    SOLCLIENT_SUBCODE_UNKNOWN_DTE_NAME = SOLCLIENT_SUBCODE_UNKNOWN_TE_NAME  # Deprecated name;
    # ::SOLCLIENT_SUBCODE_UNKNOWN_TE_NAME is preferred.
    SOLCLIENT_SUBCODE_MAX_CLIENTS_FOR_QUEUE = 63  # An attempt was made to bind to a Queue that
    # already has a maximum number of clients.
    SOLCLIENT_SUBCODE_MAX_CLIENTS_FOR_TE = 64  # An attempt was made to bind to a Topic Endpoint
    # that already has a maximum number of clients.
    SOLCLIENT_SUBCODE_MAX_CLIENTS_FOR_DTE = SOLCLIENT_SUBCODE_MAX_CLIENTS_FOR_TE  # Deprecated name,
    # ::SOLCLIENT_SUBCODE_MAX_CLIENTS_FOR_TE is preferred.
    SOLCLIENT_SUBCODE_UNEXPECTED_UNBIND = 65  # An unexpected unbind response was received for a Queue
    # or Topic Endpoint (for example, the Queue or Topic Endpoint was deleted from the appliance).
    SOLCLIENT_SUBCODE_QUEUE_NOT_FOUND = 66  # The specified Queue was not found when publishing a message.
    SOLCLIENT_SUBCODE_CLIENT_ACL_DENIED = 67  # The client login to the appliance was denied because the
    # IP address/netmask combination used for the client is designated in the ACL (Access Control List)
    # as a deny connection for the given Message VPN and username.
    SOLCLIENT_SUBCODE_SUBSCRIPTION_ACL_DENIED = 68  # Adding a subscription was denied because it matched
    # a subscription that was defined on the ACL (Access Control List).
    SOLCLIENT_SUBCODE_PUBLISH_ACL_DENIED = 69  # A message could not be published because its Topic matched
    # a Topic defined on the ACL (Access Control List).
    SOLCLIENT_SUBCODE_DELIVER_TO_ONE_INVALID = 70  # An attempt was made to set both Deliver-To-One (DTO)
    # and Guaranteed Delivery in the same message. (Deprecated:  DTO will be applied to the corresponding
    # demoted direct message)
    SOLCLIENT_SUBCODE_SPOOL_OVER_QUOTA = 71  # Message was not delivered because the Guaranteed message
    # spool is over its allotted space quota.
    SOLCLIENT_SUBCODE_QUEUE_SHUTDOWN = 72  # An attempt was made to operate on a shutdown queue.
    SOLCLIENT_SUBCODE_TE_SHUTDOWN = 73  # An attempt was made to bind to a shutdown Topic Endpoint.
    SOLCLIENT_SUBCODE_NO_MORE_NON_DURABLE_QUEUE_OR_TE = 74  # An attempt was made to bind to a
    # non-durable Queue or Topic Endpoint, and the appliance is out of resources.
    SOLCLIENT_SUBCODE_ENDPOINT_ALREADY_EXISTS = 75  # An attempt was made to create a Queue or
    # Topic Endpoint that already exists. This subcode is only returned if the provision flag
    # SOLCLIENT_PROVISION_FLAGS_IGNORE_EXIST_ERRORS is not set.
    SOLCLIENT_SUBCODE_PERMISSION_NOT_ALLOWED = 76  # An attempt was made to delete or create a
    # Queue or Topic Endpoint when the Session does not have authorization for the action.
    # This subcode is also returned when an attempt is made to remove a message from an endpoint when the
    # Session does not have 'consume' authorization, or when an attempt is made to add or remove a Topic
    # subscription from a Queue when the Session does not have 'modify-topic' authorization.
    SOLCLIENT_SUBCODE_INVALID_SELECTOR = 77  # An attempt was made to bind to a Queue or Topic
    # Endpoint with an invalid selector.
    SOLCLIENT_SUBCODE_MAX_MESSAGE_USAGE_EXCEEDED = 78  # Publishing of message denied because the
    # maximum spooled message count was exceeded.
    SOLCLIENT_SUBCODE_ENDPOINT_PROPERTY_MISMATCH = 79  # An attempt was made to create a dynamic durable
    # endpoint and it was found to exist with different properties.
    SOLCLIENT_SUBCODE_SUBSCRIPTION_MANAGER_DENIED = 80  # An attempt was made to add a subscription to
    # another client when Session does not have subscription manager privileges.
    SOLCLIENT_SUBCODE_UNKNOWN_CLIENT_NAME = 81  # An attempt was made to add a subscription to another
    # client that is unknown on the appliance.
    SOLCLIENT_SUBCODE_QUOTA_OUT_OF_RANGE = 82  # An attempt was made to provision an endpoint with a
    # quota that is out of range.
    SOLCLIENT_SUBCODE_SUBSCRIPTION_ATTRIBUTES_CONFLICT = 83  # The client attempted to add a subscription
    # which already exists but it has different properties
    SOLCLIENT_SUBCODE_INVALID_SMF_MESSAGE = 84  # The client attempted to send a Solace Message Format (SMF) message
    # using solClient_session_sendSmf() or solClient_session_sendMultipleSmf(), but the buffer did not
    # contain a Direct message.
    SOLCLIENT_SUBCODE_NO_LOCAL_NOT_SUPPORTED = 85  # The client attempted to establish a Session or
    # Flow with No Local enabled and the capability is not supported by the appliance.
    SOLCLIENT_SUBCODE_UNSUBSCRIBE_NOT_ALLOWED_CLIENTS_BOUND = 86  # The client attempted to unsubscribe
    # a Topic from a Topic Endpoint while there were still Flows bound to the endpoint.
    SOLCLIENT_SUBCODE_CANNOT_BLOCK_IN_CONTEXT = 87  # An API function was invoked in the
    # Context thread that would have blocked otherwise. For an example, a call may have been made to send a message
    # when the Session is configured with ::SOLCLIENT_SESSION_PROP_SEND_BLOCKING enabled and the
    # transport (socket or IPC) channel is full. All application callback functions are executed in the Context thread.
    SOLCLIENT_SUBCODE_FLOW_ACTIVE_FLOW_INDICATION_UNSUPPORTED = 88  # The client attempted
    # to establish a Flow with Active Flow Indication (SOLCLIENT_FLOW_PROP_ACTIVE_FLOW_IND) enabled and the
    # capability is not supported by the appliance
    SOLCLIENT_SUBCODE_UNRESOLVED_HOST = 89  # The client failed to connect because the host name could not be resolved.
    SOLCLIENT_SUBCODE_CUT_THROUGH_UNSUPPORTED = 90  # An attempt was made to create
    # a 'cut-through' Flow on a Session that does not support this capability
    SOLCLIENT_SUBCODE_CUT_THROUGH_ALREADY_BOUND = 91  # An attempt was made to create
    # a 'cut-through' Flow on a Session that already has one 'cut-through' Flow
    SOLCLIENT_SUBCODE_CUT_THROUGH_INCOMPATIBLE_WITH_SESSION = 92  # An attempt was made to
    # create a 'cut-through' Flow on a Session with incompatible Session properties. Cut-through may not
    # be enabled on Sessions with SOLCLIENT_SESSION_PROP_TOPIC_DISPATCH enabled.
    SOLCLIENT_SUBCODE_INVALID_FLOW_OPERATION = 93  # An API call failed due to the attempted
    # operation not being valid for the Flow.
    SOLCLIENT_SUBCODE_UNKNOWN_FLOW_NAME = 94  # The session was disconnected due to loss of
    # the publisher flow state. All (unacked and unsent) messages held by the API were deleted. To connect
    # the session, applications need to call ::solClient_session_connect again.
    SOLCLIENT_SUBCODE_REPLICATION_IS_STANDBY = 95  # An attempt to perform an operation using
    # a VPN that is configured to be STANDBY for replication.
    SOLCLIENT_SUBCODE_LOW_PRIORITY_MSG_CONGESTION = 96  # The message was rejected by
    # the appliance as one or more matching endpoints exceeded the reject-low-priority-msg-limit.
    SOLCLIENT_SUBCODE_LIBRARY_NOT_LOADED = 97  # The client failed to find the library or symbol.
    SOLCLIENT_SUBCODE_FAILED_LOADING_TRUSTSTORE = 98  # The client failed to load the trust store.
    SOLCLIENT_SUBCODE_UNTRUSTED_CERTIFICATE = 99  # The client attempted to connect to
    # an appliance that has a suspect certificate.
    SOLCLIENT_SUBCODE_UNTRUSTED_COMMONNAME = 100  # The client attempted to connect to
    # an appliance that has a suspect common name.
    SOLCLIENT_SUBCODE_CERTIFICATE_DATE_INVALID = 101  # The client attempted to connect to
    # an appliance that does not have a valid certificate date.
    SOLCLIENT_SUBCODE_FAILED_LOADING_CERTIFICATE_AND_KEY = 102  # The client failed to
    # load certificate and/or private key files.
    SOLCLIENT_SUBCODE_BASIC_AUTHENTICATION_IS_SHUTDOWN = 103  # The client attempted to connect
    # to an appliance that has the basic authentication shutdown.
    SOLCLIENT_SUBCODE_CLIENT_CERTIFICATE_AUTHENTICATION_IS_SHUTDOWN = 104  # The client attempted to connect
    # to an appliance that has the client certificate authentication shutdown.
    SOLCLIENT_SUBCODE_UNTRUSTED_CLIENT_CERTIFICATE = 105  # The client failed to connect to an appliance
    # as it has a suspect client certificate.
    SOLCLIENT_SUBCODE_CLIENT_CERTIFICATE_DATE_INVALID = 106  # The client failed to connect to an appliance
    # as it does not have a valid client certificate date.
    SOLCLIENT_SUBCODE_CACHE_REQUEST_CANCELLED = 107  # The cache request has been cancelled by the client.
    SOLCLIENT_SUBCODE_DELIVERY_MODE_UNSUPPORTED = 108  # Attempt was made from a Transacted Session to
    # send a message with the delivery mode SOLCLIENT_DELIVERY_MODE_DIRECT.
    SOLCLIENT_SUBCODE_PUBLISHER_NOT_CREATED = 109  # Client attempted to send a message from
    # a Transacted Session without creating a default publisher flow.
    SOLCLIENT_SUBCODE_FLOW_UNBOUND = 110  # The client attempted to receive message from an UNBOUND Flow
    # with no queued messages in memory.
    SOLCLIENT_SUBCODE_INVALID_TRANSACTED_SESSION_ID = 111  # The client attempted to commit or rollback
    # a transaction with an invalid Transacted Session Id.
    SOLCLIENT_SUBCODE_INVALID_TRANSACTION_ID = 112  # The client attempted to commit or rollback a transaction
    # with an invalid transaction Id.
    SOLCLIENT_SUBCODE_MAX_TRANSACTED_SESSIONS_EXCEEDED = 113  # The client failed to open a Transacted Session
    # as it exceeded the max Transacted Sessions.
    SOLCLIENT_SUBCODE_TRANSACTED_SESSION_NAME_IN_USE = 114  # The client failed to open a Transacted Session as
    # the Transacted Session name provided is being used by another opened session.
    SOLCLIENT_SUBCODE_SERVICE_UNAVAILABLE = 115  # Guaranteed Delivery services are not enabled on the appliance.
    SOLCLIENT_SUBCODE_NO_TRANSACTION_STARTED = 116  # The client attempted to commit an unknown transaction.
    SOLCLIENT_SUBCODE_PUBLISHER_NOT_ESTABLISHED = 117  # A send call was made on a transacted session
    # before its publisher is established.
    SOLCLIENT_SUBCODE_MESSAGE_PUBLISH_FAILURE = 118  # The client attempted to commit a transaction
    # with a GD publish failure encountered.
    SOLCLIENT_SUBCODE_TRANSACTION_FAILURE = 119  # The client attempted to commit a transaction with
    # too many transaction steps.
    SOLCLIENT_SUBCODE_MESSAGE_CONSUME_FAILURE = 120  # The client attempted to commit a transaction
    # with a consume failure encountered.
    SOLCLIENT_SUBCODE_ENDPOINT_MODIFIED = 121  # The client attempted to commit a transaction with
    # an Endpoint being shutdown or deleted.
    SOLCLIENT_SUBCODE_INVALID_CONNECTION_OWNER = 122  # The client attempted to commit a transaction
    # with an unknown connection ID.
    SOLCLIENT_SUBCODE_KERBEROS_AUTHENTICATION_IS_SHUTDOWN = 123  # The client attempted to connect to
    # an appliance that has the Kerberos authentication shutdown.
    SOLCLIENT_SUBCODE_COMMIT_OR_ROLLBACK_IN_PROGRESS = 124  # The client attempted to send/receive a message
    # or commit/rollback a transaction when a transaction commit/rollback is in progress.
    SOLCLIENT_SUBCODE_UNBIND_RESPONSE_LOST = 125  # The application called solClient_flow_destroy() and the
    # unbind-response was not received.
    SOLCLIENT_SUBCODE_MAX_TRANSACTIONS_EXCEEDED = 126  # The client failed to open a Transacted Session as
    # the maximum number of transactions was exceeded.
    SOLCLIENT_SUBCODE_COMMIT_STATUS_UNKNOWN = 127  # The commit response was lost due to a transport layer
    # reconnection to an alternate host in the host list.
    SOLCLIENT_SUBCODE_PROXY_AUTH_REQUIRED = 128  # The host entry did not contain proxy authentication
    # when required by the proxy server.
    SOLCLIENT_SUBCODE_PROXY_AUTH_FAILURE = 129  # The host entry contained invalid proxy authentication
    # when required by the proxy server.
    SOLCLIENT_SUBCODE_NO_SUBSCRIPTION_MATCH = 130  # The client attempted to publish a guaranteed message to a
    # topic that did not have any guaranteed subscription matches or only matched a replicated topic.
    SOLCLIENT_SUBCODE_SUBSCRIPTION_MATCH_ERROR = 131  # The client attempted to bind to a non-exclusive topic
    # endpoint that is already bound with a different subscription.
    SOLCLIENT_SUBCODE_SELECTOR_MATCH_ERROR = 132  # The client attempted to bind to a non-exclusive topic endpoint
    # that is already bound with a different ingress selector.
    SOLCLIENT_SUBCODE_REPLAY_NOT_SUPPORTED = 133  # Replay is not supported on the Solace Message Router.
    SOLCLIENT_SUBCODE_REPLAY_DISABLED = 134  # Replay is not enabled in the message-vpn.
    SOLCLIENT_SUBCODE_CLIENT_INITIATED_REPLAY_NON_EXCLUSIVE_NOT_ALLOWED = 135  # The client attempted to start
    # replay on a flow bound to a non-exclusive endpoint.
    SOLCLIENT_SUBCODE_CLIENT_INITIATED_REPLAY_INACTIVE_FLOW_NOT_ALLOWED = 136  # The client attempted to start
    # replay on an inactive flow.
    SOLCLIENT_SUBCODE_CLIENT_INITIATED_REPLAY_BROWSER_FLOW_NOT_ALLOWED = 137  # The client attempted to bind with
    # both ::SOLCLIENT_FLOW_PROP_BROWSER enabled and ::SOLCLIENT_FLOW_PROP_REPLAY_START_LOCATION set.
    SOLCLIENT_SUBCODE_REPLAY_TEMPORARY_NOT_SUPPORTED = 138  # Replay is not supported on temporary endpoints.
    SOLCLIENT_SUBCODE_UNKNOWN_START_LOCATION_TYPE = 139  # The client attempted to start a replay but provided an
    # unknown start location type.
    SOLCLIENT_SUBCODE_REPLAY_MESSAGE_UNAVAILABLE = 140  # A replay in progress on a flow failed because messages
    # to be replayed were trimmed from the replay log.
    SOLCLIENT_SUBCODE_REPLAY_STARTED = 141  # A replay was started on the queue/topic endpoint, either by another
    # client or by an administrator on the message router.
    SOLCLIENT_SUBCODE_REPLAY_CANCELLED = 142  # A replay in progress on a flow was administratively cancelled,
    # causing the flow to be unbound.
    SOLCLIENT_SUBCODE_REPLAY_START_TIME_NOT_AVAILABLE = 143  # A replay was requested but the requested start
    # time is not available in the replay log.
    SOLCLIENT_SUBCODE_REPLAY_MESSAGE_REJECTED = 144  # The Solace Message Router attempted to replay a message,
    # but the queue/topic endpoint rejected the message to the sender.
    SOLCLIENT_SUBCODE_REPLAY_LOG_MODIFIED = 145  # A replay in progress on a flow failed because the replay
    # log was modified.
    SOLCLIENT_SUBCODE_MISMATCHED_ENDPOINT_ERROR_ID = 146  # Endpoint error ID in the bind request does not
    # match the endpoint's error ID.
    SOLCLIENT_SUBCODE_OUT_OF_REPLAY_RESOURCES = 147  # A replay was requested, but the router does not have
    # sufficient resources to fulfill the request, due to too many active replays.
    SOLCLIENT_SUBCODE_TOPIC_OR_SELECTOR_MODIFIED_ON_DURABLE_TOPIC_ENDPOINT = 148  # A replay was in progress on a
    # Durable Topic Endpoint (DTE) when its topic or selector was modified, causing the replay to fail.
    SOLCLIENT_SUBCODE_REPLAY_FAILED = 149  # A replay in progress on a flow failed.
    SOLCLIENT_SUBCODE_COMPRESSED_SSL_NOT_SUPPORTED = 150  # The client attempted to establish a Session or Flow
    # with ssl and compression, but the capability is not supported by the appliance.
    SOLCLIENT_SUBCODE_SHARED_SUBSCRIPTIONS_NOT_SUPPORTED = 151  # The client attempted to add a shared subscription,
    # but the capability is not supported by the appliance.
    SOLCLIENT_SUBCODE_SHARED_SUBSCRIPTIONS_NOT_ALLOWED = 152  # The client attempted to add a shared subscription on a
    # client that is not permitted to use shared subscriptions.
    SOLCLIENT_SUBCODE_SHARED_SUBSCRIPTIONS_ENDPOINT_NOT_ALLOWED = 153  # The client attempted to add a shared
    # subscription to a queue or topic endpoint.


# Threshold to pause & resume the flow for persistent receiver
HIGH_THRESHOLD = 50  # pause the flow
LOW_THRESHOLD = 40  # resume the flow
GRACE_PERIOD_MIN_MS = 1000
GRACE_PERIOD_MAX_MS = 60000

SOLCLIENT_FLOW_PROP_SELECTOR = "FLOW_SELECTOR"  # A Java Message System (JMS) defined selector.

SOLCLIENT_GLOBAL_PROP_DEFAULT_SSL_LIB_UNIX = "libssl.so"  # The default SSL library name for Unix
# (including Linux and AIX)
SOLCLIENT_GLOBAL_PROP_DEFAULT_SSL_LIB_MACOSX = "libssl.1.1.dylib"  # The default SSL library name for MacOSX
SOLCLIENT_GLOBAL_PROP_DEFAULT_SSL_LIB_VMS = "SSL1$LIBSSL_SHR.EXE"  # The default SSL library name for OpenVMS
SOLCLIENT_GLOBAL_PROP_DEFAULT_SSL_LIB_WINDOWS = "libssl-1_1.dll"  # The default SSL library name for Windows
SOLCLIENT_GLOBAL_PROP_DEFAULT_CRYPTO_LIB_UNIX = "libcrypto.so"  # The default crypto library name for Unix
# (including Linux and AIX).
SOLCLIENT_GLOBAL_PROP_DEFAULT_CRYPTO_LIB_MACOSX = "libcrypto.1.1.dylib"  # The default crypto library name for MacOSX.
SOLCLIENT_GLOBAL_PROP_DEFAULT_CRYPTO_LIB_VMS = "SSL1$LIBCRYPTO_SHR.EXE"  # The default crypto library name for OpenVMS.
SOLCLIENT_GLOBAL_PROP_DEFAULT_CRYPTO_LIB_WINDOWS = "libcrypto-1_1.dll"  # The default crypto library name for Windows.
