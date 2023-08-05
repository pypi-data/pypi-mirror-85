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


""" Module for property based configuration """
from abc import ABC, abstractmethod


class PropertyBasedConfiguration(ABC):  # pylint: disable=too-few-public-methods
    """
    An abstract class that abstracts extended property-based configuration for fine-tuning.
    """

    @abstractmethod
    def from_properties(self, configuration: dict):
        """
        Enables a dictionary based on the configuration.

        NOTE:
            Callbacks are not expected to be configurable using this approach because
            callbacks are expected to be configured programmatically.

        Args:
            configuration (dict): The dictionary containing the properties.

        Raises:
            IllegalArgumentError : When invalid properties are added.
        """
