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
"""This test module contains the tests for commands in aea.cli.generate_wealth module."""

from unittest import TestCase, mock

import pytest

from aea.cli import cli
from aea.cli.generate_wealth import _try_generate_wealth
from aea.test_tools.exceptions import AEATestingException
from aea.test_tools.test_cases import AEATestCaseMany

from tests.conftest import (
    CLI_LOG_OPTION,
    CliRunner,
    FETCHAI,
    MAX_FLAKY_RERUNS_INTEGRATION,
)
from tests.test_cli.tools_for_testing import ContextMock


class GenerateWealthTestCase(TestCase):
    """Test case for _generate_wealth method."""

    @mock.patch("aea.cli.utils.package_utils.Wallet")
    @mock.patch("aea.cli.generate_wealth.click.echo")
    @mock.patch("aea.cli.generate_wealth.try_generate_testnet_wealth")
    @mock.patch("aea.cli.utils.package_utils.verify_or_create_private_keys_ctx")
    def test__generate_wealth_positive(self, *mocks):
        """Test for _generate_wealth method positive result."""
        ctx = ContextMock()
        _try_generate_wealth(ctx, "cosmos", True)


@mock.patch("aea.cli.utils.decorators.try_to_load_agent_config")
@mock.patch("aea.cli.utils.package_utils.verify_or_create_private_keys_ctx")
@mock.patch("aea.cli.generate_wealth._try_generate_wealth")
class GenerateWealthCommandTestCase(TestCase):
    """Test case for CLI generate_wealth command."""

    def setUp(self):
        """Set it up."""
        self.runner = CliRunner()

    def test_run_positive(self, *mocks):
        """Test for CLI generate_wealth positive result."""
        result = self.runner.invoke(
            cli,
            [
                *CLI_LOG_OPTION,
                "--skip-consistency-check",
                "generate-wealth",
                "--sync",
                FETCHAI,
            ],
            standalone_mode=False,
        )
        self.assertEqual(result.exit_code, 0)


class TestWealthCommandsPositive(AEATestCaseMany):
    """Test case for CLI wealth commands."""

    @pytest.mark.integration
    @pytest.mark.flaky(reruns=MAX_FLAKY_RERUNS_INTEGRATION)
    def test_wealth_commands(self):
        """Test wealth commands."""
        agent_name = "test_aea"
        self.create_agents(agent_name)

        self.set_agent_context(agent_name)

        self.generate_private_key()
        self.add_private_key()

        self.generate_wealth()


class TestWealthCommandsNegative(AEATestCaseMany):
    """Test case for CLI wealth commands, negative case."""

    def test_wealth_commands_negative(self):
        """Test wealth commands."""
        agent_name = "test_aea"
        self.create_agents(agent_name)

        self.set_agent_context(agent_name)

        self.generate_private_key()
        self.add_private_key()

        settings = {"unsupported_crypto": "path"}
        self.nested_set_config("agent.private_key_paths", settings)
        with pytest.raises(AEATestingException) as excinfo:
            self.generate_wealth()

        assert "Item not registered with id 'unsupported_crypto'." in str(excinfo.value)
