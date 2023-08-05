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
This module contains the AuthenticationStrategy abstract base class and implementation classes for each
available ``AuthenticationStrategy`` instance available.
"""
import logging
from abc import ABC, abstractmethod

from solace.messaging.config import sol_constants
from solace.messaging.config.solace_properties import authentication_properties

logger = logging.getLogger('solace.messaging')

__all_ = ["AuthenticationStrategy", "BasicUserNamePassword", "ClientCertificateAuthentication"]


class AuthenticationStrategy(ABC):  # pylint: disable=too-few-public-methods
    """
    Abstract base class for all authentication strategy classes that include:

    - :py:class:`solace.messaging.config.authentication_strategy.BasicUserNamePassword`
    - :py:class:`solace.messaging.config.authentication_strategy.ClientCertificateAuthentication`
    """

    @property
    @abstractmethod
    def authentication_configuration(self) -> dict:
        """
        Retrieves the authentication strategy.

        Returns:
         dict: A dictionary with the authentication configuration.
        """


class BasicUserNamePassword(AuthenticationStrategy):
    """
    The implementation class for basic username and password concrete class for the authentication strategy.
    """

    def __init__(self, username: str, password: str):
        logger.debug('[%s] initialized', type(self).__name__)

        self._authentication_configuration = dict()
        self._authentication_configuration[authentication_properties.SCHEME_BASIC_USER_NAME] = username
        self._authentication_configuration[authentication_properties.SCHEME_BASIC_PASSWORD] = password
        self._authentication_configuration[
            authentication_properties.SCHEME] = sol_constants.SOLCLIENT_SESSION_PROP_AUTHENTICATION_SCHEME_BASIC

    @property
    def authentication_configuration(self):
        """
        The authentication strategy configuration.
        """
        return self._authentication_configuration

    @staticmethod
    def of(username: str, password: str) -> 'BasicUserNamePassword':  # pylint: disable=invalid-name
        """
        Creates an instance of :py:class:`BasicUserNamePassword` based on the specified from the ``username``
        and ``password``.
        Args:
            username (str): The user name to use to create a BasicUserNamePassword object.
            password (str): The password to use to create a BasicUserNamePassword object.
        Returns:
            BasicUserNamePassword: The created object.
        """
        logger.debug('Authentication Strategy with basic username: [%s] and password: [****]', username)
        return BasicUserNamePassword(username, password)


class ClientCertificateAuthentication(AuthenticationStrategy):
    """
    Implementation of client Certificate authentication concrete class for the authentication strategy.
    Client certificate authentication can be used when the client connections to
    the PubSub+ broker are TLS/SSL-encrypted.

    For a client to use a client certificate authentication scheme, the PubSub+ event broker must
    be properly configured for TLS/SSL connections, and the verification of the client certificate must be
    enabled for the particular Message VPN that the client connects to.
    """

    @property
    def authentication_configuration(self) -> dict:
        """
        The authentication strategy configuration.
        """
        return self._authentication_configuration

    def __init__(self, certificate_file: str, key_file: str, key_password: str):
        logger.debug('[%s] initialized', type(self).__name__)
        self._authentication_configuration = dict()
        self._authentication_configuration[authentication_properties.SCHEME] = \
            sol_constants.SOLCLIENT_SESSION_PROP_AUTHENTICATION_SCHEME_CLIENT_CERTIFICATE
        self._authentication_configuration[authentication_properties.SCHEME_CLIENT_PRIVATE_KEY_FILE_PASSWORD] = \
            key_password
        self._authentication_configuration[authentication_properties.SCHEME_SSL_CLIENT_PRIVATE_KEY_FILE] = key_file
        self._authentication_configuration[authentication_properties.SCHEME_SSL_CLIENT_CERT_FILE] = certificate_file

    @staticmethod
    def of(certificate_file: str, key_file: str, key_password: str) -> \
            'ClientCertificateAuthentication':  # pylint: disable=invalid-name
        """"
        A static method that creates an instance of :py:class:`ClientCertificateAuthentication` from
        the given client certificate configuration.

        Args:
            certificate_file (str):  The file that contains the client certificate or the client-certificate chain.
            key_file (str): The file contains the client private key.
            key_password (str): Password if the private key (key_file) is password protected.

        Returns:
            ClientCertificateAuthentication: The instance of the object.
        """
        logger.debug('Authentication Strategy with Client Certificate Authentication. Certficate: '
                     '[%s], Key: [%s] and Keystore password: [****]', certificate_file, key_file)
        return ClientCertificateAuthentication(certificate_file, key_file, key_password)

    def with_certificate_and_key_pem(self, certificate_pem_file: str) \
            -> 'ClientCertificateAuthentication':
        """
        Set the client certificate or the client-certificate chain, and the client private
        key from a single `.PEM` file.

        Args:
            certificate_pem_file (str): TThe file that contains the client certificate or the client-certificate chain,
            and the client private key. Both must be PEM-encoded.

        Returns:
            ClientCertificateAuthentication: The instance of the object.
        """
        self._authentication_configuration[authentication_properties.SCHEME_SSL_CLIENT_PRIVATE_KEY_FILE] = \
            certificate_pem_file
        self._authentication_configuration[authentication_properties.SCHEME_SSL_CLIENT_CERT_FILE] = certificate_pem_file
        return self

    def with_private_key_password(self, private_key_password: str) \
            -> 'ClientCertificateAuthentication':  # pragma: no cover
        """"
        Sets the password needed to use the client-certificate key file.

        Args:
            private_key_password (str): The password if the file is password-protected.

        Returns:
            ClientCertificateAuthentication: The instance of the object.
        """
        self._authentication_configuration[authentication_properties.SCHEME_CLIENT_PRIVATE_KEY_FILE_PASSWORD] = \
            private_key_password
        logger.debug('Set private key password')
        return self


class AuthenticationConfiguration(ABC):  # pylint: disable=too-few-public-methods
    """
    An abstract base class that provides the `with_authentication_strategy()` interface for
    the ``build()`` method in the :py:class:`solace.messaging.message_service.MessagingServiceClientBuilder` instance.
    """

    @abstractmethod
    def with_authentication_strategy(self, authentication_strategy: AuthenticationStrategy) \
            -> 'AuthenticationConfiguration':
        """
        Specifies the authentication strategy to configure.

        Args:
            authentication_strategy (AuthenticationStrategy): The authentication strategy to use  for connections to the PubSub+ event broker.

        Returns:
            AuthenticationConfiguration: The authentication configuration instance that can be used for method chaining.
        """
