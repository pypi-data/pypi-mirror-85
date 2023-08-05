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
Modules contains the abstract classes used to define MessagePublisher and MessageReceiver life cycle.

An object in the PubSub+ API for Python that contains these interfaces may be:
- started
- terminated
- tested for state
"""
import concurrent
from abc import ABC, abstractmethod

from solace.messaging.config.sol_constants import GRACE_PERIOD_MAX_MS


class LifecycleControl(ABC):  # pylint: disable=too-few-public-methods
    """ class that abstracts control service lifecycle operations such as start and terminate"""

    @abstractmethod
    def start(self):
        """
        Enables service regular duties. Before this method is called, service is considered off duty.
        In order to operate normally this method needs to be called on a service instance. If the service
        is already started, or starting, this operation has no effect.

        Raises:
            PubSubPlusClientError When service start failed for some internal reason
            IllegalStateError If method has been invoked at an illegal or inappropriate time for some
            another reason
        """

    @abstractmethod
    def terminate(self, grace_period: int = GRACE_PERIOD_MAX_MS):
        """
        Disables regular duties of a service. If this service is already terminated or terminating, this
        operation has no effect.  All attempts to use a service after termination is requested will be
        refused with an exception.

        Raises:
            PubSubPlusClientError When service termination failed for some internal reason
            IllegalStateError If method has been invoked at an illegal or inappropriate time for some
            another reason
        """

    @abstractmethod
    def terminate_now(self):
        """
        Attempts to stop all actively executing tasks and duties of a service ignoring unfinished tasks
        or in-flight messages. This method is idempotent. Only way to resume service operation after
        this method is called is to recreate a new instance of a service. This is a non graceful
        service termination path.

        Raises:
            PubSubPlusClientError When service termination failed for some internal reason
            IllegalStateError If method has been invoked at an illegal or inappropriate time for some
            another reason
        """

    @abstractmethod
    def is_running(self) -> bool:
        """
        Checks if process was successfully started and not stopped yet

        Returns:
        False if process was not started or already stopped, true otherwise
        """

    @abstractmethod
    def is_terminated(self) -> bool:
        """
        Checks if message delivery process is terminated

        Returns:
            True if message delivery process is terminated, false otherwise
        """

    @abstractmethod
    def is_terminating(self) -> bool:
        """
        Checks if message delivery process termination is ongoing

        Returns:
            True if message delivery process being terminated, but termination is not finished, False otherwise
        """


class AsyncLifecycleControl(ABC):  # pylint: disable=too-few-public-methods
    """
    class that abstracts asynchronous control service lifecycle operations such as start_async
    and terminate_async
    """

    @abstractmethod
    def start_async(self) -> concurrent.futures.Future:
        """
        Enables service regular duties. Before this method is called, service is considered off duty.
        In order to operate normally this method needs to be called on a service instance. If the service
        is already started, or starting, this operation has no effect.

        Returns:
            This method returns a :py:class:`concurrent.futures.Future` that the application may use
            to determine when the start has completed.

        """

    @abstractmethod
    def terminate_async(self, grace_period: int = GRACE_PERIOD_MAX_MS) -> concurrent.futures:
        """
        Disables regular duties of a service. If this service is already terminated or terminating, this
        operation has no effect. All attempts to use a service after termination is requested will be
        refused with an exception.

        Returns:
            This method returns a :py:class:`concurrent.futures.Future` that the application may use
            to determine when the terminate has completed.
        """
