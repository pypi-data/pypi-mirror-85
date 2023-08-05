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


# """module for class and methods for error monitoring"""  # pylint: disable=missing-module-docstring
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from solace.messaging.messaging_service import ServiceInterruptionListener  # pragma: no cover


class ErrorMonitoring(ABC):  # pylint: disable=missing-class-docstring
    # """An class for the global error monitoring capabilities"""

    @abstractmethod
    def add_service_interruption_listener(self, listener: 'ServiceInterruptionListener') \
            :  # pylint: disable=missing-function-docstring
        # """Adds a service listener for listening to non recoverable service interruption events
        #
        # Args:
        #     listener: service interruption listener
        # """
        ...  # pragma: no cover

    @abstractmethod
    def remove_service_interruption_listener(self, listener: 'ServiceInterruptionListener') \
            :  # pylint: disable=missing-function-docstring
        # """Removes a service listener for listening to non recoverable service interruption events
        #
        # Args:
        #     listener: service interruption listener
        #
        # Returns: true if removal was successful false otherwise
        # """
        ...  # pragma: no cover
