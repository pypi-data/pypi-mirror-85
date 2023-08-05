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


""" This modules contains dictionary keys for :py:class:`~solace.messaging.messaging_service.MessagingService`
client properties """   # pylint: disable=trailing-whitespace

NAME = "solace.messaging.client.name"
"""
NAME may be used as a key in the :py:class:`~solace.messaging.messaging_service.MessagingService` properties when
configured from a dictionary.

Also known as the application_id, it is preferable for applications to set NAME as an argument to
:py:meth:`MessagingServiceClientBuilder.build()
<solace.messaging.messaging_service.MessagingServiceClientBuilder.build>`

If NAME is not specified, and application_id is not set, then a application_id is automically generated.
"""


APPLICATION_DESCRIPTION = "solace.messaging.client.application-description"
"""APPLICATION_DESCRIPTION may be used as a key in the 
:py:class:`~solace.messaging.messaging_service.MessagingService` properties when configured from a dictionary. 

When set, the APPLICATION_DESCRIPTION appears in detailed client info for connected clients on the 
Solace PubSub+ broker.
"""
