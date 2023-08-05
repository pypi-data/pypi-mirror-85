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


""""This modules contains dictionary keys for
:py:class:`~solace.messaging.publisher.message_publisher.MessagePublisher`   # pylint: disable=trailing-whitespace
properties """  # pylint: disable=trailing-whitespace


PUBLISHER_BACK_PRESSURE_STRATEGY = "solace.messaging.publisher.back-pressure.strategy"
"""Property key to define a back pressure strategy."""

PUBLISHER_BACK_PRESSURE_BUFFER_CAPACITY = "solace.messaging.publisher.back-pressure.buffer-capacity"
"""Property key to define back pressure buffer capacity measured in messages. 
This property only has effect in conjunction with back pressure strategy"""

PUBLISHER_BACK_PRESSURE_BUFFER_WAIT_TIMEOUT = "solace.messaging.publisher.back-pressure.buffer-wait-timeout"
"""Property key to define back pressure buffer wait timeouts. 
This property only has effect in conjunction with back pressure strategy"""
