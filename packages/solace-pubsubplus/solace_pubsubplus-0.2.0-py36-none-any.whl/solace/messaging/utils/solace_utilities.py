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


# """module for solace internal utilities"""   # pylint: disable=missing-module-docstring
import configparser
import os
from os.path import dirname

from solace.messaging.config.solace_message_constants import INVALID_DATATYPE
from solace.messaging.errors.pubsubplus_client_error import PubSubPlusClientError, \
    InvalidDataTypeError


class Util:  # pylint: disable=missing-class-docstring,missing-function-docstring
    # """Utilities class"""

    @staticmethod
    def is_type_matches(actual, expected_type, raise_exception=True, ignore_none=False) -> bool:
        # """
        # Args:
        #     actual: target input parameter
        #     expected_type: compare ACTUAL data type with this
        #     raise_exception: if actual and expected date type doesn't matches
        #     ignore_none: ignore type check if ACTUAL is None
        #
        # Returns: True if actual and expected date type matches, else False
        # """
        if isinstance(actual, expected_type) or (ignore_none and actual is None):
            return True
        if raise_exception:
            raise InvalidDataTypeError(f'{INVALID_DATATYPE} Expected type: [{type(expected_type)}], '
                                       f'but actual [{type(actual)}]')
        return False

    @staticmethod
    def read_solace_props_from_config(section):
        # """method to read the dictionary template based on the file path provided
        # Returns:
        #     dict template
        # """
        config_ini_file_name = 'config.ini'
        base_folder = dirname(dirname(dirname(__file__)))
        config_ini_full_path = os.path.join(base_folder, config_ini_file_name)

        try:
            config = configparser.ConfigParser()
            config.read(config_ini_full_path)
            config_parser_dict = {s: dict(config.items(s)) for s in config.sections()}
            if section not in config_parser_dict:
                raise PubSubPlusClientError(f'Unable to locate "{section}" properties in '
                                            f'[{config_ini_full_path}]')  # pragma: no cover
            return config_parser_dict[section]
        except Exception as exception:  # pragma: no cover
            raise PubSubPlusClientError(f'Unable to locate "{section}" properties in '
                                        f'[{config_ini_full_path}] Exception: {exception}') from exception

    @staticmethod
    def read_key_from_config(section: str, key_name: str):
        # """method to read the key name from the config.ini file"""

        # noinspection PyBroadException
        try:
            kvp = Util.read_solace_props_from_config(section)
            return kvp[key_name]
        except PubSubPlusClientError:  # pragma: no cover
            return None
