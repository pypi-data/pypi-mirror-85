# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
#
#   Copyright 2018-2019 Fetch.AI Limited
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

"""This package contains the strategy model."""

from typing import Dict, Optional, Tuple, cast

from aea.crypto.ledger_apis import LedgerApis
from aea.helpers.transaction.base import Terms
from aea.skills.base import Model

from packages.fetchai.contracts.staking_erc20.contract import PUBLIC_ID
from packages.fetchai.skills.confirmation_aw1.registration_db import RegistrationDB


REQUIRED_KEYS = [
    "ethereum_address",
    "fetchai_address",
    "signature_of_ethereum_address",
    "signature_of_fetchai_address",
    "developer_handle",
]
DEFAULT_TOKEN_DISPENSE_AMOUNT = 100000
DEFAULT_TOKEN_DENOMINATION = "atestfet"  # nosec
DEFAULT_CONTRACT_ADDRESS = "0x351bac612b50e87b46e4b10a282f632d41397de2"
DEFAULT_OVERRIDE = False


class Strategy(Model):
    """This class is the strategy model."""

    def __init__(self, **kwargs) -> None:
        """
        Initialize the strategy of the agent.

        :return: None
        """
        self._token_denomination = kwargs.pop(
            "token_denomination", DEFAULT_TOKEN_DENOMINATION
        )
        self._token_dispense_amount = kwargs.pop(
            "token_dispense_amount", DEFAULT_TOKEN_DISPENSE_AMOUNT
        )
        self._fetchai_staking_contract_address = kwargs.pop(
            "fetchai_staking_contract_address", DEFAULT_CONTRACT_ADDRESS
        )
        self._override_staking_check = kwargs.pop(
            "override_staking_check", DEFAULT_OVERRIDE
        )
        super().__init__(**kwargs)
        self._is_ready_to_register = False
        self._is_registered = False
        self.is_registration_pending = False
        self.signature_of_ethereum_address: Optional[str] = None
        self._ledger_id = self.context.default_ledger_id
        self._max_tx_fee = 100
        self._contract_ledger_id = "ethereum"
        self._contract_callable = "get_stake"
        self._contract_id = str(PUBLIC_ID)
        self._in_process_registrations: Dict[str, Dict[str, str]] = {}

    @property
    def contract_id(self) -> str:
        """Get the ledger on which the contract is deployed."""
        return self._contract_id

    @property
    def contract_address(self) -> str:
        """Get contract address."""
        return self._fetchai_staking_contract_address

    @property
    def contract_ledger_id(self) -> str:
        """Get the ledger on which the contract is deployed."""
        return self._contract_ledger_id

    @property
    def contract_callable(self) -> str:
        """Get the ledger on which the contract is deployed."""
        return self._contract_callable

    def lock_registration_temporarily(self, address: str, info: Dict[str, str]) -> None:
        """Lock this address for registration."""
        self._in_process_registrations.update({address: info})

    def finalize_registration(self, address: str) -> None:
        """Lock this address for registration."""
        info = self._in_process_registrations.pop(address)
        self.context.logger.info(
            f"finalizing registration for address={address}, info={info}"
        )
        registration_db = cast(RegistrationDB, self.context.registration_db)
        registration_db.set_registered(
            address=address,
            ethereum_address=info["ethereum_address"],
            ethereum_signature=info["signature_of_ethereum_address"],
            fetchai_signature=info["signature_of_fetchai_address"],
            developer_handle=info["developer_handle"],
            tweet=info.get("tweet", ""),
        )

    def unlock_registration(self, address: str) -> None:
        """Unlock this address for registration."""
        info = self._in_process_registrations.pop(address, {})
        self.context.logger.info(
            f"registration info did not pass staking checks = {info}"
        )

    def valid_registration(
        self, registration_info: Dict[str, str], sender: str
    ) -> Tuple[bool, int, str]:
        """
        Check if the registration info is valid.

        :param registration_info: the registration info
        :param sender: the sender
        :return: tuple of success, error code and error message
        """
        if not all([key in registration_info for key in REQUIRED_KEYS]):
            return (
                False,
                1,
                f"missing keys in registration info, required: {REQUIRED_KEYS}!",
            )
        if not sender == registration_info["fetchai_address"]:
            return (
                False,
                1,
                "fetchai address of agent and registration info do not match!",
            )
        if not self._valid_signature(
            registration_info["ethereum_address"],
            registration_info["signature_of_fetchai_address"],
            sender,
            "ethereum",
        ):
            return (False, 1, "fetchai address and signature do not match!")
        if not self._valid_signature(
            sender,
            registration_info["signature_of_ethereum_address"],
            registration_info["ethereum_address"],
            "fetchai",
        ):
            return (False, 1, "ethereum address and signature do not match!")
        if sender in self._in_process_registrations:
            return (False, 1, "registration in process for this address!")
        registration_db = cast(RegistrationDB, self.context.registration_db)
        if registration_db.is_registered(sender):
            return (False, 1, "already registered!")
        return (True, 0, "all good!")

    def _valid_signature(
        self, expected_signer: str, signature: str, message_str: str, ledger_id: str
    ) -> bool:
        """
        Check if the signature and message match the expected signer.

        :param expected_signer: the signer
        :param signature: the signature
        :param message_str: the message
        :param ledger_id: the ledger id
        :return: bool indiciating validity
        """
        try:
            result = expected_signer in LedgerApis.recover_message(
                ledger_id, message_str.encode("utf-8"), signature
            )
        except Exception as e:  # pylint: disable=broad-except
            self.context.logger.warning(f"Signing exception: {e}")
            result = False
        return result

    def get_terms(self, counterparty: str) -> Terms:
        """
        Get terms of transaction.

        :param counterparty: the counterparty to receive funds
        :return: the terms
        """
        terms = Terms(
            ledger_id=self._ledger_id,
            sender_address=self.context.agent_address,
            counterparty_address=counterparty,
            amount_by_currency_id={
                self._token_denomination: -self._token_dispense_amount
            },
            quantities_by_good_id={},
            is_sender_payable_tx_fee=True,
            nonce="some",
            fee_by_currency_id={self._token_denomination: self._max_tx_fee},
        )
        return terms

    @staticmethod
    def get_kwargs(info: Dict[str, str]) -> Dict[str, str]:
        """
        Get the kwargs for the contract state call.

        :param counterparty:
        """
        counterparty = info["ethereum_address"]
        return {"address": counterparty}

    def has_staked(self, state: Dict[str, str]) -> bool:
        """
        Check if the agent has staked.

        :return: bool, indicating outcome
        """
        if self._override_staking_check:
            return True
        result = int(state.get("stake", "0")) > 0
        return result
