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


# """  # pylint: disable=missing-module-docstring
# Module for Publishing message
# """
import logging
from ctypes import c_int, c_char_p
from typing import TYPE_CHECKING

from solace.messaging.config.sol_constants import SOLCLIENT_TOPIC_DESTINATION, SOLCLIENT_OK, SOLCLIENT_WOULD_BLOCK, \
    SOLCLIENT_FAIL
from solace.messaging.config.solace_message_constants import SET_DESTINATION_FAILED, UNABLE_TO_PUBLISH_MESSAGE, \
    CCSMP_SUB_CODE, CCSMP_INFO_SUB_CODE, TOPIC_NAME_TOO_LONG, TOPIC_NAME_CANNOT_BE_EMPTY, \
    CCSMP_SUBCODE_PARAM_OUT_OF_RANGE
from solace.messaging.core._message import _SolClientContextDestination
from solace.messaging.core._solace_message import _SolaceMessage
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError, \
    IllegalArgumentError
from solace.messaging.solace_logging.core_api_log import last_error_info

if TYPE_CHECKING:
    from solace.messaging.resources.topic import Topic
    from solace.messaging.messaging_service import MessagingService

logger = logging.getLogger('solace.messaging.core')


class _SolacePublish:  # pylint: disable=too-few-public-methods, missing-class-docstring, missing-function-docstring
    # """ Class for publishing the message"""

    def __init__(self, messaging_service: 'MessagingService'):
        logger.debug('[%s] initialized', type(self).__name__)
        self._messaging_service: 'MessagingService' = messaging_service

    def publish(self, solace_message: _SolaceMessage, topic: 'Topic') -> int:
        # """
        # Args:
        #     topic (str): topic endpoint name
        #     solace_message (SolaceMessage): SolaceMessage instance
        #
        # Returns:
        #     an integer value stating message sent (i.e. SOLCLIENT_OK) or would block (i.e. SOLCLIENT_WOULD_BLOCK)
        # Raises:
        #     PubSubPlusClientError: when status_code is not 0 (i.e. SOLCLIENT_OK) or 1 (i.e. SOLCLIENT_WOULD_BLOCK)
        # """
        self.__set_topic(solace_message, topic)
        publish_message_status_code = self._messaging_service.api.send_message(solace_message.msg_p)
        if publish_message_status_code in [SOLCLIENT_OK, SOLCLIENT_WOULD_BLOCK]:
            logger.debug("Message PUBLISH on [%s] status: %d", topic.get_name(), publish_message_status_code)
            return publish_message_status_code

        core_exception_msg = last_error_info(status_code=publish_message_status_code,
                                             caller_desc='On PUBLISH')
        logger.debug('\nSub code: %s. Error: %s. Sub code: %s. Return code: %s',
                     core_exception_msg[CCSMP_INFO_SUB_CODE],
                     core_exception_msg["error_info_contents"],
                     core_exception_msg[CCSMP_SUB_CODE], core_exception_msg["return_code"])
        raise PubSubPlusClientError(message=UNABLE_TO_PUBLISH_MESSAGE)

    @staticmethod
    def __set_topic(solace_message: _SolaceMessage, topic: 'Topic'):
        # """
        # Set the topic for a message
        # Args:
        #     solace_message (SolaceMessage): Message object with pointer to the message
        #     topic (Topic): topic endpoint
        # Raises:
        #     PubSubPlusClientError : if the return_code is not 0
        # """
        topic_name = topic.get_name()
        destination = _SolClientContextDestination(destType=c_int(SOLCLIENT_TOPIC_DESTINATION),
                                                   dest=c_char_p(topic_name.encode('utf-8')))
        msg_set_destination_status = solace_message.message_set_destination(destination)
        if msg_set_destination_status != SOLCLIENT_OK:
            core_exception_msg = last_error_info(status_code=msg_set_destination_status,
                                                 caller_desc='On SET destination')
            if msg_set_destination_status == SOLCLIENT_FAIL and \
                    core_exception_msg[CCSMP_SUB_CODE] == CCSMP_SUBCODE_PARAM_OUT_OF_RANGE:
                error_message = 'Invalid topic name'
                if 'Empty string dest pointer' in core_exception_msg["error_info_contents"]:
                    error_message = TOPIC_NAME_CANNOT_BE_EMPTY
                elif 'exceeds maximum of 250' in core_exception_msg["error_info_contents"]:
                    error_message = TOPIC_NAME_TOO_LONG
                logger.warning(error_message)
                raise IllegalArgumentError(error_message)
            logger.warning(SET_DESTINATION_FAILED)
            raise PubSubPlusClientError(message=SET_DESTINATION_FAILED)  # pragma: no cover
        logger.debug('Destination [%s] is successfully set', topic_name)
