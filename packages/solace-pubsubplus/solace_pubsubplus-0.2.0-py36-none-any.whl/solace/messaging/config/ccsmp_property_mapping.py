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


# this module contains the CCSMP session properties mapping.   # pylint: disable= missing-module-docstring

from solace.messaging.config.sol_constants import SOLCLIENT_PROP_ENABLE_VAL, SOLCLIENT_PROP_DISABLE_VAL, \
    SOLCLIENT_FLOW_PROP_BIND_ENTITY_DURABLE, SOLCLIENT_FLOW_PROP_ACKMODE, \
    SOLCLIENT_FLOW_PROP_ACKMODE_CLIENT, SOLCLIENT_FLOW_PROP_BIND_ENTITY_ID, \
    SOLCLIENT_FLOW_PROP_BIND_ENTITY_QUEUE, SOLCLIENT_FLOW_PROP_ACTIVE_FLOW_IND, \
    SOLCLIENT_ENDPOINT_PROP_ID, SOLCLIENT_ENDPOINT_PROP_QUEUE, \
    SOLCLIENT_ENDPOINT_PROP_DURABLE, SOLCLIENT_ENDPOINT_PROP_ACCESSTYPE, \
    SOLCLIENT_ENDPOINT_PROP_ACCESSTYPE_EXCLUSIVE, SOLCLIENT_ENDPOINT_PROP_PERMISSION, SOLCLIENT_ENDPOINT_PERM_DELETE
from solace.messaging.config.solace_properties import service_properties, authentication_properties, \
    transport_layer_properties, client_properties, transport_layer_security_properties, receiver_properties
from solace.messaging.config.solace_properties.authentication_properties import SCHEME_BASIC_USER_NAME, \
    SCHEME_BASIC_PASSWORD
from solace.messaging.config.solace_properties.service_properties import VPN_NAME
from solace.messaging.config.solace_properties.transport_layer_properties import HOST

default_props = {"SESSION_TOPIC_DISPATCH": SOLCLIENT_PROP_ENABLE_VAL,
                 "SESSION_SEND_BLOCKING": SOLCLIENT_PROP_DISABLE_VAL,
                 "SESSION_REAPPLY_SUBSCRIPTIONS": SOLCLIENT_PROP_ENABLE_VAL,
                 "SESSION_IGNORE_DUP_SUBSCRIPTION_ERROR": SOLCLIENT_PROP_ENABLE_VAL}

flow_props = {SOLCLIENT_FLOW_PROP_BIND_ENTITY_ID: SOLCLIENT_FLOW_PROP_BIND_ENTITY_QUEUE,
              SOLCLIENT_FLOW_PROP_BIND_ENTITY_DURABLE: SOLCLIENT_PROP_ENABLE_VAL,
              SOLCLIENT_FLOW_PROP_ACKMODE: SOLCLIENT_FLOW_PROP_ACKMODE_CLIENT,
              SOLCLIENT_FLOW_PROP_ACTIVE_FLOW_IND: SOLCLIENT_PROP_ENABLE_VAL}
# enable active flow indication default is disabled

end_point_props = {SOLCLIENT_ENDPOINT_PROP_ID: SOLCLIENT_ENDPOINT_PROP_QUEUE,
                   SOLCLIENT_ENDPOINT_PROP_DURABLE: SOLCLIENT_PROP_ENABLE_VAL,
                   SOLCLIENT_ENDPOINT_PROP_ACCESSTYPE: SOLCLIENT_ENDPOINT_PROP_ACCESSTYPE_EXCLUSIVE,
                   SOLCLIENT_ENDPOINT_PROP_PERMISSION: SOLCLIENT_ENDPOINT_PERM_DELETE}

mandatory_props = [HOST, VPN_NAME, SCHEME_BASIC_USER_NAME, SCHEME_BASIC_PASSWORD]

CCSMP_SESSION_PROP_MAPPING = {
    transport_layer_properties.HOST: 'SESSION_HOST',
    transport_layer_properties.CONNECTION_ATTEMPTS_TIMEOUT: 'SESSION_CONNECT_TIMEOUT_MS',
    transport_layer_properties.CONNECTION_RETRIES: 'SESSION_CONNECT_RETRIES',
    transport_layer_properties.CONNECTION_RETRIES_PER_HOST: 'SESSION_CONNECT_RETRIES_PER_HOST',
    transport_layer_properties.RECONNECTION_ATTEMPTS: 'SESSION_RECONNECT_RETRIES',
    transport_layer_properties.RECONNECTION_ATTEMPTS_WAIT_INTERVAL: 'SESSION_RECONNECT_RETRY_WAIT_MS',
    transport_layer_properties.KEEP_ALIVE_INTERVAL: 'SESSION_KEEP_ALIVE_INTERVAL_MS',
    transport_layer_properties.KEEP_ALIVE_WITHOUT_RESPONSE_LIMIT: 'SESSION_KEEP_ALIVE_LIMIT',
    transport_layer_properties.SOCKET_INPUT_BUFFER_SIZE: 'SESSION_SOCKET_RCV_BUF_SIZE',
    transport_layer_properties.SOCKET_OUTPUT_BUFFER_SIZE: 'SESSION_SOCKET_SEND_BUF_SIZE',
    transport_layer_properties.SOCKET_TCP_OPTION_NO_DELAY: 'SESSION_TCP_NODELAY',
    transport_layer_properties.COMPRESSION_LEVEL: 'SESSION_COMPRESSION_LEVEL',
    transport_layer_security_properties.CERT_VALIDATED: 'SESSION_SSL_VALIDATE_CERTIFICATE',
    transport_layer_security_properties.CERT_REJECT_EXPIRED: 'SESSION_SSL_VALIDATE_CERTIFICATE_DATE',
    transport_layer_security_properties.CERT_VALIDATE_SERVERNAME: 'SESSION_SSL_VALIDATE_CERTIFICATE_HOST',
    transport_layer_security_properties.EXCLUDED_PROTOCOLS: 'SESSION_SSL_EXCLUDED_PROTOCOLS',
    transport_layer_security_properties.PROTOCOL_DOWNGRADE_TO: 'SESSION_SSL_CONNECTION_DOWNGRADE_TO',
    transport_layer_security_properties.CIPHER_SUITES: 'SOLCLIENT_SESSION_PROP_SSL_CIPHER_SUITES',
    transport_layer_security_properties.TRUST_STORE_PATH: 'SESSION_SSL_TRUST_STORE_DIR',
    transport_layer_security_properties.TRUSTED_COMMON_NAME_LIST: 'SESSION_SSL_TRUSTED_COMMON_NAME_LIST',
    service_properties.VPN_NAME: 'SESSION_VPN_NAME',
    service_properties.GENERATE_SENDER_ID: 'SESSION_SEND_SENDER_ID',
    service_properties.GENERATE_RECEIVE_TIMESTAMPS: 'SESSION_RCV_TIMESTAMP',
    service_properties.GENERATE_SEND_TIMESTAMPS: 'SESSION_SEND_TIMESTAMP',
    authentication_properties.SCHEME: 'SESSION_AUTHENTICATION_SCHEME',
    authentication_properties.SCHEME_BASIC_USER_NAME: 'SESSION_USERNAME',
    authentication_properties.SCHEME_BASIC_PASSWORD: 'SESSION_PASSWORD',
    authentication_properties.SCHEME_SSL_CLIENT_CERT_FILE: 'SESSION_SSL_CLIENT_CERTIFICATE_FILE',
    authentication_properties.SCHEME_SSL_CLIENT_PRIVATE_KEY_FILE: 'SESSION_SSL_CLIENT_PRIVATE_KEY_FILE',
    authentication_properties.SCHEME_CLIENT_PRIVATE_KEY_FILE_PASSWORD: 'SESSION_SSL_CLIENT_PRIVATE_KEY_FILE_PASSWORD',
    receiver_properties.PERSISTENT_NO_LOCAL_PUBLISHED_MESSAGES: 'FLOW_NO_LOCAL',
    client_properties.NAME: 'SESSION_CLIENT_NAME',
    client_properties.APPLICATION_DESCRIPTION: 'SESSION_APPLICATION_DESCRIPTION'
}
