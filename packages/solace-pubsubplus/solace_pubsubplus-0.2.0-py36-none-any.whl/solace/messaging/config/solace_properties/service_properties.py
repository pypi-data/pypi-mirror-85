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


"""This modules contains dictionary keys for :py:class:`~solace.messaging.messaging_service.MessagingService`
properties """  # pylint: disable=trailing-whitespace

VPN_NAME = "solace.messaging.service.vpn-name"
"""VPN_NAME may be used as a key in the :py:class:`~solace.messaging.messaging_service.MessagingService` properties 
when configured from a dictionary. """

GENERATE_SENDER_ID = "solace.messaging.service.generate-sender-id"
"""GENERATE_SENDER_ID may be used as a key in the :py:class:`~solace.messaging.messaging_service.MessagingService` 
properties when configured from a dictionary. 

When enabled, GENERATE_SENDER_ID applies to all messages published by 
:py:class:`~solace.messaging.publisher.message_publisher.MessagePublisher` that exist on the messaging service.  Each 
message published will include the SenderId property. The application_id set in 
:py:meth:`MessagingServiceClientBuilder.build(
)<solace.messaging.messaging_service.MessagingServiceClientBuilder.build>` is used as the SenderId. """

GENERATE_RECEIVE_TIMESTAMPS = "solclient.session.prop.generate-rcv-timestamps"
"""GENERATE_RECEIVE_TIMESTAMPS may be used as a key in the 
:py:class:`~solace.messaging.messaging_service.MessagingService` properties when configured from a dictionary. 

When enabled, GENERATE_RECEIVE_TIMESTAMPS applies to all messages received by
:py:class:`~solace.messaging.receiver.message_receiver.MessageReceiver` that exist on the messaging service. Each 
message received will include a receive timestamp that reflects the time the message was received from the PubSub+ 
broker by the underlying native API."""

GENERATE_SEND_TIMESTAMPS = "solclient.session.prop.generate-send-timestamps"
"""GENERATE_RECEIVE_TIMESTAMPS may be used as a key in the 
:py:class:`~solace.messaging.messaging_service.MessagingService` properties when configured from a dictionary. 

When enabled, GENERATE_SEND_TIMESTAMPS applies to all messages received by
:py:class:`~solace.messaging.publisher.message_publisher.MessagePublisher` that exist on the messaging service. Each 
message published will include a receive timestamp that reflects the time the message was queued for transmission to
the PubSub+ broker by the underlying native API."""
