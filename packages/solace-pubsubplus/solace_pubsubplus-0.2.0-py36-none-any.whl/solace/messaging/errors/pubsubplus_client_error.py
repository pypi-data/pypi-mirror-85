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


""" Module contains error classes for PubSub+ Messaging API for Python. """


class TransportError(Exception):
    """ Reserved for future use. """


class PubSubPlusClientError(Exception):
    """ Base error class for PubSub+ Messaging API for Python. """

    def __init__(self, message):
        """
        Args:
            message: The error message.

        Raises:
            PubSubPlusClientError: Raises the error.
        """

        super().__init__(self, message)


class ServiceUnreachableError(PubSubPlusClientError):
    """
    A class for throwing errors when a service is unreachable.

    This error is thrown when the ``MessageService`` in unable
    to create a transport connection to the PubSub+ event broker.
    """


class AuthenticationError(PubSubPlusClientError):
    """ Reserved for future use. """


class BackPressureError(PubSubPlusClientError):
    """ A class for throwing errors when back pressure occurs.  This class is a base class for more specific error. """


class PublisherOverflowError(PubSubPlusClientError):
    """
    A class for throwing errors for throwing publisher overflows.

    ``PublisherOverflowError`` is thrown when unable to publish a message because the transport is full and
    buffer space is not available.
    """


class IllegalArgumentError(ValueError):
    """
    A class for throwing errors for illegal argument, which extends ``ValueError``.
    """


class InvalidDataTypeError(TypeError):
    """
    A class for throwing errors for invalid data type in the configuration.
    This error is thrown when an argument to a function contains an invalid object.
    """


class IllegalStateError(PubSubPlusClientError):
    """
     A class for throwing errors for illegal states.

    This error is thrown when the operation requested cannot be performed as the API state necessary for
    the operation has not been established.
    """


class IncompatibleMessageError(PubSubPlusClientError):
    """An exception class for incompatible an message.
       This error is thrown when the message are incompatible and the broker is unable to process the message."""


class InvalidConfigurationError(PubSubPlusClientError):
    """ A class for throwing errors for invalid configuration."""


class PubSubTimeoutError(PubSubPlusClientError):
    """ A class for throwing errors when a time-out occurs."""


class IncompatibleServiceError(PubSubPlusClientError):
    """ A class for throwing errors for incompatible services. """


class MessageDestinationDoesNotExistError(PubSubPlusClientError):
    """ A class for throwing errors when the message destination does not exist. """


class InvalidServiceURLError(PubSubPlusClientError):
    """ A class for throwing errors for when an invalid service URL is provided.  """


class AuthorizationError(PubSubPlusClientError):
    """ A class for throwing errors when authorization violations occur. """


class PubSubPlusClientIOError(PubSubPlusClientError):
    """ A class for throwing I/O errors that occur on client applications."""


class MessageRejectedByBrokerError(PubSubPlusClientError):
    """ A class for throwing errors when a message has bee rejected by event broker. """


class MessageNotAcknowledgedByBrokerError(PubSubPlusClientError):
    """ A class for throwing  errors when message is not acknowledged by the event broker."""


class MessageTooBigError(PubSubPlusClientError):
    """ A class for throwing errors when a message too large. """


class MissingReplierError(PubSubPlusClientError):
    """ A class for throwing errors when missing a replier to a message. """


class IncompleteMessageDeliveryError(PubSubPlusClientError):
    """A class for throwing an error when a publisher has been terminated gracefully, but there are some messages
       left in the buffer.
    """
