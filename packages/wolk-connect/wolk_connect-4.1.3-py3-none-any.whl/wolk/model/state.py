"""States of actuators & configurations as defined on WolkAbout IoT Platform."""
#   Copyright 2020 WolkAbout Technology s.r.o.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
from enum import Enum
from enum import unique


@unique
class State(Enum):
    """
    Enumeration of available states.

    :ivar BUSY: Currently in busy state
    :vartype BUSY: str
    :ivar ERROR: Currently in error state
    :vartype ERROR: str
    :ivar READY: Currently in ready state
    :vartype READY: str
    """

    READY = "READY"
    BUSY = "BUSY"
    ERROR = "ERROR"
