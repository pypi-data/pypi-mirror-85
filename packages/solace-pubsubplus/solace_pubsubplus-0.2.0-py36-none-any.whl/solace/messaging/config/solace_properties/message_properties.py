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

"""This module contains Message properties"""

# pylint: disable=trailing-whitespace, pointless-string-statement

""" Property key to specify application message type, This value is used by applications only,
and is passed through the API untouched """
APPLICATION_MESSAGE_TYPE = "solace.messaging.message.application-message-type"

"""Property key to specify whether the message is eligible for eliding"""
ELIDING_ELIGIBLE = "solace.messaging.message.eliding-eligible"

"""
Property key to specify optional message priority.
The valid priority value range is 0-255 with 0 as the lowest priority and 255 as the
highest. Value -1 indicates the priority is not set and a default priority value is used instead."""
PRIORITY = "solace.messaging.message.priority"

"""Property key to specify HTTP content type header value for interaction with an HTTP client 
Accepted values Defined in rfc7231 section-3.1.2.2"""
HTTP_CONTENT_TYPE = "solace.messaging.message.http-content"

"""Property key to specify HTTP content type encoding value for interaction with an HTTP client
Accepted values Defined in rfc2616 section-14.11"""
HTTP_CONTENT_ENCODING = "solace.messaging.message.http-encoding"

"""Property key to specify correlation ID. The correlation ID is used for correlating a request
to a reply and should be as random as possible.
This variable is being also used for the Request-Reply API, this is why it is suggested
not to use this property on a message builder instance but only on a publisher interface
where available."""
CORRELATION_ID = "solace.messaging.message.correlationId"

"""Property key to specify number of milliseconds before the message is discarded or moved to a
Dead Message Queue.
The value of 0 means the message never expires. The default value is 0.
This property is only valid for persistent messages"""
PERSISTENT_TIME_TO_LIVE = "solace.messaging.message.persistent.time-to-live"

"""Property key to specify The UTC time (in milliseconds, from midnight, January 1, 1970 UTC)
when the message is supposed to expire. Setting this property has no effect if the TimeToLive 
is set in the same message. It is carried to clients that receive the message, unmodified and 
does not effect the life cycle of the message.This property is only valid for persistent messages"""
PERSISTENT_EXPIRATION = "solace.messaging.message.persistent.expiration"

"""Property key to specify if message is eligible to be moved to a Dead Message Queue.
 The default value is True
 This property is only valid for persistent messages."""
PERSISTENT_DMQ_ELIGIBLE = "solace.messaging.message.persistent.dmq-eligible"

"""Property key to specify if appliance should ACK this message immediately upon receipt.
 The default value is False
 This property is only valid for persistent messages"""
PERSISTENT_ACK_IMMEDIATELY = "solace.messaging.message.persistent.ack-immediately"

SEQUENCE_NUMBER = "solace.messaging.message.sequence-number"
APPLICATION_MESSAGE_ID = "solace.messaging.message.application-message-id"
