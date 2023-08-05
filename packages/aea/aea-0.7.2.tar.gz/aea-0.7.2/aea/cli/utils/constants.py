# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2020 Fetch.AI Limited
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
#
# ------------------------------------------------------------------------------

"""Module with constants of the aea cli."""

import os
from pathlib import Path
from typing import Dict

from aea.configurations.base import (
    DEFAULT_CONNECTION_CONFIG_FILE,
    DEFAULT_CONTRACT_CONFIG_FILE,
    DEFAULT_PROTOCOL_CONFIG_FILE,
    DEFAULT_SKILL_CONFIG_FILE,
)


AEA_DIR = str(Path("."))

ITEM_TYPES = ("connection", "contract", "protocol", "skill")

AEA_LOGO = "    _     _____     _    \r\n   / \\   | ____|   / \\   \r\n  / _ \\  |  _|    / _ \\  \r\n / ___ \\ | |___  / ___ \\ \r\n/_/   \\_\\|_____|/_/   \\_\\\r\n                         \r\n"
AUTHOR_KEY = "author"
CLI_CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".aea", "cli_config.yaml")
NOT_PERMITTED_AUTHORS = [
    "skills",
    "connections",
    "protocols",
    "contracts",
    "vendor",
    "packages",
    "aea",
]


FROM_STRING_TO_TYPE = dict(
    str=str, int=int, bool=bool, float=float, dict=dict, list=list
)

ALLOWED_PATH_ROOTS = [
    "agent",
    "skills",
    "protocols",
    "connections",
    "contracts",
    "vendor",
]
RESOURCE_TYPE_TO_CONFIG_FILE = {
    "skills": DEFAULT_SKILL_CONFIG_FILE,
    "protocols": DEFAULT_PROTOCOL_CONFIG_FILE,
    "connections": DEFAULT_CONNECTION_CONFIG_FILE,
    "contracts": DEFAULT_CONTRACT_CONFIG_FILE,
}  # type: Dict[str, str]
FALSE_EQUIVALENTS = ["f", "false", "False"]

REQUIREMENTS = "requirements.txt"
