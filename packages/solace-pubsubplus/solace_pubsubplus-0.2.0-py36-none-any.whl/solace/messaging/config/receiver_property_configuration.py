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


"""
This module abstracts property-based and extended fine-tuning of the configuration for the message receiver."""
from abc import abstractmethod

from solace.messaging.config.property_based_configuration import PropertyBasedConfiguration


class ReceiverPropertyConfiguration(PropertyBasedConfiguration):  # pylint: disable=too-few-public-methods
    """
        Enables property-based configuration and extended fine-tuning of the configuration for the message receiver.
    """

    @abstractmethod
    def from_properties(self, configuration: dict) -> 'ReceiverPropertyConfiguration':
        """
        Enables a dictionary based on the configuration.

        NOTE:
            Callbacks are not expected to be configurable using this approach beca callbacks
            are expected to be configured programmatically.

        Args:
            configuration (dict): The dictionary containing the properties.

        Raises:
            IllegalArgumentError : When invalid properties are added.
        """
