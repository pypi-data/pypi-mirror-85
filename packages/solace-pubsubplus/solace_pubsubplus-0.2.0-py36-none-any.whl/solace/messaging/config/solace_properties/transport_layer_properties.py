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


"""This modules contains dictionary keys for the :py:class:`solace.messaging.messaging_service.MessagingService`
transport layer properties."""  # pylint: disable=trailing-whitespace

HOST = "solace.messaging.transport.host"
"""The IPv4 or IPv6 address or host name of the PubSub+ broker to connect to.

Multiple entries are allowed, separated by commas.
The entry for the HOST property should provide a protocol, host, and port.
"""

CONNECTION_ATTEMPTS_TIMEOUT = "solace.messaging.transport.connection-attempts-timeout"
"""The timeout period (in milliseconds) for a connect operation to a given host."""

CONNECTION_RETRIES = "solace.messaging.transport.connection-retries"
"""How many times to try to connect to the PubSub+ broker (or list of PubSub+ broker) during connection setup.

Zero means no automatic connection retries (that is, try once and give up). -1 means try to connect forever. 
The default valid range is >= -1.

When using a host list, each time the API works through the host list without establishing a connection is
considered a connect retry. For example, if a CONNECTION_RETRIES value of two is used,
the API could possibly work through all of the listed hosts without connecting to them three times: one time
through for the initial connect attempt, and then two times through for connect retries.
Each connect retry begins with the first host listed. After each unsuccessful attempt to connect to a host,
the API waits for the amount of time set for RECONNECTION_ATTEMPTS_WAIT_INTERVAL before attempting
another connection to a host, and the number times to attempt to connect to one host before moving on to the
next listed host is determined by the value set for CONNECTION_RETRIES_PER_HOST.
"""

CONNECTION_RETRIES_PER_HOST = "solace.messaging.transport.connection.retries-per-host"
"""When using a host list, this property defines how many times to try to connect or reconnect to a
single host before moving to the next host in the list."""

RECONNECTION_ATTEMPTS = "solace.messaging.transport.reconnection-attempts"
"""How many times to retry to reconnect to the PubSub+ broker (or list of PubSub+ broker) after a connected Messaging 
Service goes down. 

Zero means no automatic reconnection attempts. -1 means try to reconnect forever. The default valid range is >= -1.

When using a host list, each time the API works through the host list without establishing a connection is considered a
reconnect retry. Each reconnect retry begins with the first host listed. After each unsuccessful attempt to reconnect
to a host, the API waits for the amount of time set for RECONNECTION_ATTEMPTS_WAIT_INTERVAL before attempting another
connection to a PubSub+ broker, and the number times to attempt to connect to one PubSub+ broker before moving on to the
next listed host is determined by the value set for CONNECTION_RETRIES_PER_HOST."""

RECONNECTION_ATTEMPTS_WAIT_INTERVAL = "solace.messaging.transport.reconnection-attempts-wait-interval"
"""How much time (in milliseconds) to wait between each attempt to connect or reconnect to the configured HOST.

If a connect or reconnect attempt to the configured HOST (which may be a list) is not successful, the API waits for
the amount of time set for RECONNECTION_ATTEMPTS_WAIT_INTERVAL, and then makes another connect or reconnect attempt.
The valid range is >=0."""

KEEP_ALIVE_INTERVAL = "solace.messaging.transport.keep-alive-interval"
"""The amount of time (in milliseconds) to wait between sending out Keep-Alive messages."""

KEEP_ALIVE_WITHOUT_RESPONSE_LIMIT = "solace.messaging.transport.keep-alive-without-response-limit"
"""The maximum number of consecutive Keep-Alive messages that can be sent without receiving a response before
the connection is closed by the API."""

SOCKET_OUTPUT_BUFFER_SIZE = "solace.messaging.transport.socket.output-buffer-size"
"""The value for the socket send buffer size (in bytes).

0 indicates do not set and leave at operating system default. The valid range is 0 or >= 1024."""

SOCKET_INPUT_BUFFER_SIZE = "solace.messaging.transport.socket.input-buffer-size"
"""The value for socket receive buffer size (in bytes).

0 indicates do not set and leave at operating system default. The valid range is 0 or >= 1024. """

SOCKET_TCP_OPTION_NO_DELAY = "solace.messaging.transport.socket.tcp-option-no-delay"
"""Boolean value to enable TCP no delay."""

COMPRESSION_LEVEL = "solace.messaging.transport.compression-level"
"""Enables messages to be compressed with ZLIB before transmission and decompressed on receive.

This property should preferably be set by
:py:meth:`MessagingServiceClientBuilder.with_compression_level()
<solace.messaging.messaging_service.MessagingServiceClientBuilder.with_message_compression>`

The valid range is 0 (off) or 1..9, where 1 is less compression (fastest) and 9 is most compression (slowest).

Note: If no port is specified in the HOST property, the API will automatically connect to either the default 
non-compressed listen port (55555) or default compressed listen port (55003) based on the specified 
COMPRESSION_LEVEL. If a port is specified in the HOST property you must specify the non-compressed listen port if not 
using compression (compression level 0) or the compressed listen port if using compression (compression levels 1 to 
9). """
