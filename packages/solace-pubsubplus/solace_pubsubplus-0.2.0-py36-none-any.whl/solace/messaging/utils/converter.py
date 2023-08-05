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
# Module for type-safe to/from target type object converter is a marker
# """
from abc import ABC, abstractmethod
from typing import Union, TypeVar, Generic

T = TypeVar('T')  # pylint: disable=invalid-name


class BytesToObject(Generic[T], ABC):  # pylint: disable=too-few-public-methods, missing-class-docstring
    # """turns byte array to Business object """

    @abstractmethod
    def convert(self, src: bytearray) -> T:
        """this method converts the byte array to Object"""


class ObjectToBytes(Generic[T], ABC):  # pylint: disable=too-few-public-methods, missing-class-docstring
    # """turns business object to byte array"""
    ...

    @abstractmethod
    def to_bytes(self, src: T) -> bytes:  # pylint: disable=missing-function-docstring
        # """This Method turns given business object into byte array"""
        ...  # pragma: no cover

    @abstractmethod
    def get_message_properties(self) -> Union[dict, None]:  # pylint: disable=missing-function-docstring
        # """
        # Provides optional message header properties which will be included into outbound message during message
        # composition using given instance of converter. Developer of the particular converters may decide to inject
        # some message header properties as part of the business object conversion to a message (i.e schema URL is a
        # good candidate for this) This method will be called from the API at appropriate time to retrieve desired
        # message properties and inject them into a message.
        #
        # Returns: default impl returns None (no additional properties will be added)
        # """
        ...
