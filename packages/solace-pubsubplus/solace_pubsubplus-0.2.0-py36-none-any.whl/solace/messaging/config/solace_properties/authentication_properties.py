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


"""This modules contains the dictionary keys for :py:class:`~solace.messaging.messaging_service.MessagingService`
authentication properties """   # pylint: disable=trailing-whitespace

SCHEME = "solace.messaging.authentication.scheme"
"""SCHEME may be used as a key in the :py:class:`~solace.messaging.messaging_service.MessagingService` properties 
when configured from a dictionary.  

Although the SCHEME may be set in :py:meth:`MessagingServiceClientBuilder.from_properties(
)<solace.messaging.messaging_service.MessagingServiceClientBuilder.from_properties>` it is preferable to use 
:py:meth:`MessagingServiceClientBuilder.with_authentication_strategy(
)<solace.messaging.messaging_service.MessagingServiceClientBuilder.with_authentication_strategy>` and avoid these 
internal details. 

The value in the dictionary may be one of:

- SCHEME_BASIC:  authenticate with username and password, equivalent to
    :py:class:`~solace.messaging.config.authentication_strategy.BasicUserNamePassword`
- SCHEME_CLIENT_CERTIFICATE: authenticate with a X509 Client Certificate, equivalent to
    :py:class:`~solace.messaging.config.authentication_strategy.ClientCertificateAuthentication`

"""

SCHEME_BASIC_USER_NAME = "solace.messaging.authentication.scheme.basic.username"
"""SCHEME_BASIC_USER_NAME may be used as a key in the 
:py:class:`~solace.messaging.messaging_service.MessagingService` properties when configured from a dictionary. This 
property is only used if :py:class:`~solace.messaging.config.authentication_strategy.BasicUserNamePassword` 
strategy is chosen. """

SCHEME_BASIC_PASSWORD = "solace.messaging.authentication.scheme.basic.password"
"""SCHEME_BASIC_PASSWORD may be used as a key in the 
:py:class:`~solace.messaging.messaging_service.MessagingService` properties when configured from a dictionary. This 
property is only used if :py:class:`~solace.messaging.config.authentication_strategy.BasicUserNamePassword` 
strategy is chosen. """

SCHEME_SSL_CLIENT_CERT_FILE = "solace.messaging.authentication.scheme.client-cert-file"
"""SCHEME_SSL_CLIENT_CERT_FILE may be used as a key in the 
:py:class:`~solace.messaging.messaging_service.MessagingService` properties when configured from a dictionary. This 
property is only used if :py:class:`~solace.messaging.config.authentication_strategy
.ClientCertificateAuthentication` strategy is chosen. """

SCHEME_SSL_CLIENT_PRIVATE_KEY_FILE = "solace.messaging.authentication.scheme.client-cert.private-key-file"
"""SCHEME_SSL_CLIENT_PRIVATE_KEY_FILE may be used as a key in the 
:py:class:`~solace.messaging.messaging_service.MessagingService` properties when configured from a dictionary. This 
property is only used if :py:class:`~solace.messaging.config.authentication_strategy
.ClientCertificateAuthentication` strategy is chosen. """

SCHEME_CLIENT_PRIVATE_KEY_FILE_PASSWORD = "solace.messaging.authentication.scheme.client-cert.private-key-password"
"""SCHEME_CLIENT_PRIVATE_KEY_FILE_PASSWORD may be used as a key in the 
:py:class:`~solace.messaging.messaging_service.MessagingService` properties when configured from a dictionary. This 
property is only used if :py:class:`~solace.messaging.config.authentication_strategy
.ClientCertificateAuthentication` strategy is chosen. """
