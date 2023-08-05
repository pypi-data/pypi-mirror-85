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


""" This modules abstracts different aspects of API manageability"""

import enum
from abc import ABC, abstractmethod

from solace.messaging.config.sol_constants import SOLCLIENTSTATSRX, SOLCLIENTSTATSTX


class Metric(enum.Enum):  # pylint: disable=too-few-public-methods
    """
    Metric is an enumeration of available statistics that may be retrieved from any class with
    the py:class:`~solace.messaging.utils.manageable.Manageable` interface.

    """
    DIRECT_BYTES_RECEIVED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_DIRECT_BYTES.name
    """The number of bytes received."""
    DIRECT_MESSAGES_RECEIVED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_DIRECT_MSGS.name
    """The number of messages received."""
    BROKER_DISCARD_NOTIFICATIONS_RECEIVED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_DISCARD_IND.name
    """ The number of receive messages with discard indication set."""
    UNKNOWN_PARAMETER_MESSAGES_DISCARDED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_DISCARD_SMF_UNKNOWN_ELEMENT.name
    """The number of messages discarded due to the presence of an unknown element or unknown protocol in the
    Solace Message Format (SMF) header."""
    TOO_BIG_MESSAGES_DISCARDED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_DISCARD_MSG_TOO_BIG.name
    """ The number of messages discarded due to msg too large. """
    PERSISTENT_ACKNOWLEDGE_SENT = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_ACKED.name
    """The number of acknowledgments sent for Guaranteed messages."""
    PERSISTENT_DUPLICATE_MESSAGES_DISCARDED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_DISCARD_DUPLICATE.name
    """The number of Guaranteed messages dropped for being duplicates. """
    PERSISTENT_NO_MATCHING_FLOW_MESSAGES_DISCARDED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_DISCARD_NO_MATCHING_FLOW.name
    """The number of Guaranteed messages discarded due to no match on the flowId."""
    PERSISTENT_OUT_OF_ORDER_MESSAGES_DISCARDED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_DISCARD_OUTOFORDER.name
    """The number of Guaranteed messages discarded for being received out of order."""
    PERSISTENT_BYTES_RECEIVED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_PERSISTENT_BYTES.name
    """The number of Persistent bytes received on the MessageReceiver. On the MessageService, it is the total
    number of Persistent bytes received across all MessageReceiver."""
    PERSISTENT_MESSAGES_RECEIVED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_PERSISTENT_MSGS.name
    """ The number of Persistent messages received on the MessageReceiver. On the MessageService, it is the
    total number of Persistent messages received across all MessageReceiver."""
    NONPERSISTENT_BYTES_RECEIVED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_NONPERSISTENT_BYTES.name
    """The number of Non-persistent bytes received on the MessageReceiver. On the MessageService, it is the total
    number of Non-persistent bytes received across all MessageReceiver."""
    NONPERSISTENT_MESSAGES_RECEIVED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_NONPERSISTENT_MSGS.name
    """ The number of Non-persistent messages received on the MessageReceiver. On the MessageService, it is the
    total number of Non-persistent messages received across all MessageReceiver."""
    CONTROL_MESSAGES_RECEIVED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_CTL_MSGS.name
    """The number of control (non-data) messages received."""
    CONTROL_BYTES_RECEIVED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_CTL_BYTES.name
    """The number of bytes received in control (non-data) messages."""
    TOTAL_BYTES_RECEIVED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_TOTAL_DATA_BYTES.name
    """ The total number of data bytes received. """
    TOTAL_MESSAGES_RECEIVED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_TOTAL_DATA_MSGS.name
    """The total number of data messages received."""
    COMPRESSED_BYTES_RECEIVED = SOLCLIENTSTATSRX.SOLCLIENT_STATS_RX_COMPRESSED_BYTES.name
    """The number of bytes received before decompression. """

    TOTAL_BYTES_SENT = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_TOTAL_DATA_BYTES.name
    """The number of data bytes transmitted in total."""
    TOTAL_MESSAGES_SENT = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_TOTAL_DATA_MSGS.name
    """The number of data messages transmitted in total. """
    PUBLISHER_WOULD_BLOCK = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_WOULD_BLOCK.name
    """The number of messages not accepted due to would block (non-blocking only)."""
    DIRECT_BYTES_SENT = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_DIRECT_BYTES.name
    """The number of bytes transmitted in Direct messages."""
    DIRECT_MESSAGES_SENT = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_DIRECT_MSGS.name
    """The number of Direct messages transmitted."""
    PERSISTENT_BYTES_SENT = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_PERSISTENT_BYTES.name
    """The number of bytes transmitted in Persistent messages. """
    NONPERSISTENT_BYTES_SENT = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_NONPERSISTENT_BYTES.name
    """The number of bytes transmitted in Non-Persistent messages. """
    PERSISTENT_MESSAGES_SENT = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_PERSISTENT_MSGS.name
    """The number of Persistent messages transmitted. """
    NONPERSISTENT_MESSAGES_SENT = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_NONPERSISTENT_MSGS.name
    """The number of Non-Persistent messages transmitted."""
    PERSISTENT_MESSAGES_REDELIVERED = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_PERSISTENT_REDELIVERED.name
    """The number of Persistent messages redelivered."""
    NONPERSISTENT_MESSAGES_REDELIVERED = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_NONPERSISTENT_REDELIVERED.name
    """The number of Non-Persistent messages redelivered."""
    PERSISTENT_BYTES_REDELIVERED = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_PERSISTENT_BYTES_REDELIVERED.name
    """The number of bytes redelivered in Persistent messages."""
    NONPERSISTENT_BYTES_REDELIVERED = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_NONPERSISTENT_BYTES_REDELIVERED.name
    """The number of bytes redelivered in Non-Persistent messages."""
    PUBLISHER_ACKNOWLEDGEMENT_RECEIVED = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_ACKS_RXED.name
    """The number of acknowledgments received."""
    PUBLISHER_WINDOW_CLOSED = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_WINDOW_CLOSE.name
    """The number of times the transmit window closed."""
    PUBLISHER_ACKNOWLEDGEMENT_TIMEOUTS = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_ACK_TIMEOUT.name
    """The number of times the acknowledgment timer expired."""
    CONTROL_MESSAGES_SENT = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_CTL_MSGS.name
    """The number of control (non-data) messages transmitted. """
    CONTROL_BYTES_SENT = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_CTL_BYTES.name
    """The number of bytes transmitted in control (non-data) messages."""
    CONNECTION_ATTEMPTS = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_TOTAL_CONNECTION_ATTEMPTS.name
    """The total number of TCP connections attempted by this MessageService"""
    PUBLISHED_MESSAGES_ACKNOWLEDGED = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_GUARANTEED_MSGS_SENT_CONFIRMED.name
    """Guaranteed messages (Persistent/Non-Persistent) published that have been acknowledged."""
    PUBLISH_MESSAGES_DISCARDED = SOLCLIENTSTATSTX.SOLCLIENT_STATS_TX_DISCARD_CHANNEL_ERROR.name
    """Messages discarded due to channel failure."""


class ApiMetrics(ABC):
    """Abstract class the contains the interfaces to retrieve metrics from a Manageable API"""

    @abstractmethod
    def get_value(self, the_metric: Metric) -> int:
        """Returns the metrics current value/count"""

    @abstractmethod
    def reset(self):
        """Resets ALL metrics"""

    @abstractmethod
    def __str__(self) -> str:
        """List of all in the API collected metrics"""


class Manageable(ABC):  # pylint: disable=too-few-public-methods
    """Interface to get api metrics"""

    @abstractmethod
    def metrics(self) -> ApiMetrics:
        """

        Returns:
            :py:class:`~solace.messaging.utils.manageable.ApiMetrics`
            Metrics of transmitted/received data and events on the Messaging Service """
