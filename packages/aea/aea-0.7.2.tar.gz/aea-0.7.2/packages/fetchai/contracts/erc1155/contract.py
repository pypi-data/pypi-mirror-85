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

"""This module contains the erc1155 contract definition."""

import json
import logging
import random
from typing import Any, Dict, List, Optional, cast

from vyper.utils import keccak256

from aea.common import Address
from aea.configurations.base import PublicId
from aea.contracts.base import Contract
from aea.crypto.base import LedgerApi
from aea.crypto.cosmos import CosmosApi
from aea.crypto.ethereum import EthereumApi
from aea.crypto.fetchai import FetchAIApi


_default_logger = logging.getLogger("aea.packages.fetchai.contracts.erc1155.contract")
MAX_UINT_256 = 2 ^ 256 - 1

PUBLIC_ID = PublicId.from_str("fetchai/erc1155:0.12.0")


class ERC1155Contract(Contract):
    """The ERC1155 contract class which acts as a bridge between AEA framework and ERC1155 ABI."""

    contract_id = PUBLIC_ID

    @classmethod
    def generate_token_ids(
        cls, token_type: int, nb_tokens: int, starting_index: int = 0
    ) -> List[int]:
        """
        Generate token_ids.

        :param token_type: the token type (nft or ft)
        :param nb_tokens: the number of tokens
        :param starting_index: the index at which to start constructing ids
        :return: the list of token ids generated
        """
        token_ids = []
        for i in range(nb_tokens):
            index = starting_index + i
            token_id = cls._generate_id(index, token_type)
            token_ids.append(token_id)
        return token_ids

    @staticmethod
    def _generate_id(index: int, token_type: int) -> int:
        """
        Generate a token_id.

        :param index: the index to byte-shift
        :param token_type: the token type
        :return: the token id
        """
        token_id = (token_type << 128) + index
        return token_id

    @classmethod
    def get_create_batch_transaction(  # pylint: disable=unused-argument
        cls,
        ledger_api: LedgerApi,
        contract_address: Address,
        deployer_address: Address,
        token_ids: List[int],
        data: Optional[bytes] = b"",
        gas: int = 300000,
    ) -> Dict[str, Any]:
        """
        Get the transaction to create a batch of tokens.

        :param ledger_api: the ledger API
        :param contract_address: the address of the contract
        :param deployer_address: the address of the deployer
        :param token_ids: the list of token ids for creation
        :param data: the data to include in the transaction
        :param gas: the gas to be used
        :return: the transaction object
        """
        if ledger_api.identifier == EthereumApi.identifier:
            nonce = ledger_api.api.eth.getTransactionCount(deployer_address)
            instance = cls.get_instance(ledger_api, contract_address)
            tx = instance.functions.createBatch(
                deployer_address, token_ids
            ).buildTransaction(
                {
                    "gas": gas,
                    "gasPrice": ledger_api.api.toWei("50", "gwei"),
                    "nonce": nonce,
                }
            )
            tx = cls._try_estimate_gas(ledger_api, tx)
            return tx
        if ledger_api.identifier in [CosmosApi.identifier, FetchAIApi.identifier]:
            tokens = []
            for token_id in token_ids:
                tokens.append({"id": str(token_id), "path": str(token_id)})

            msg = {
                "create_batch": {"item_owner": str(deployer_address), "tokens": tokens}
            }
            cosmos_api = cast(CosmosApi, ledger_api)
            tx = cosmos_api.get_handle_transaction(
                deployer_address, contract_address, msg, amount=0, tx_fee=0, gas=gas
            )
            return tx
        raise NotImplementedError

    @classmethod
    def get_create_single_transaction(
        cls,
        ledger_api: LedgerApi,
        contract_address: Address,
        deployer_address: Address,
        token_id: int,
        data: Optional[bytes] = b"",
        gas: int = 300000,
    ) -> Dict[str, Any]:
        """
        Get the transaction to create a single token.

        :param ledger_api: the ledger API
        :param contract_address: the address of the contract
        :param deployer_address: the address of the deployer
        :param token_id: the token id for creation
        :param data: the data to include in the transaction
        :param gas: the gas to be used
        :return: the transaction object
        """
        if ledger_api.identifier == EthereumApi.identifier:
            nonce = ledger_api.api.eth.getTransactionCount(deployer_address)
            instance = cls.get_instance(ledger_api, contract_address)
            tx = instance.functions.createSingle(
                deployer_address, token_id, data
            ).buildTransaction(
                {
                    "gas": gas,
                    "gasPrice": ledger_api.api.toWei("50", "gwei"),
                    "nonce": nonce,
                }
            )
            tx = cls._try_estimate_gas(ledger_api, tx)
            return tx
        if ledger_api.identifier in [CosmosApi.identifier, FetchAIApi.identifier]:
            msg = {
                "create_single": {
                    "item_owner": deployer_address,
                    "id": str(token_id),
                    "path": str(data),
                }
            }
            cosmos_api = cast(CosmosApi, ledger_api)
            tx = cosmos_api.get_handle_transaction(
                deployer_address, contract_address, msg, amount=0, tx_fee=0, gas=gas
            )
            return tx
        raise NotImplementedError

    @classmethod
    def get_mint_batch_transaction(
        cls,
        ledger_api: LedgerApi,
        contract_address: Address,
        deployer_address: Address,
        recipient_address: Address,
        token_ids: List[int],
        mint_quantities: List[int],
        data: Optional[bytes] = b"",
        gas: int = 500000,
    ) -> Dict[str, Any]:
        """
        Get the transaction to mint a batch of tokens.

        :param ledger_api: the ledger API
        :param contract_address: the address of the contract
        :param deployer_address: the address of the deployer
        :param recipient_address: the address of the recipient
        :param token_ids: the token ids
        :param mint_quantities: the quantity to mint for each token
        :param data: the data to include in the transaction
        :param gas: the gas to be used
        :return: the transaction object
        """
        cls.validate_mint_quantities(token_ids, mint_quantities)
        if ledger_api.identifier == EthereumApi.identifier:
            nonce = ledger_api.api.eth.getTransactionCount(deployer_address)
            instance = cls.get_instance(ledger_api, contract_address)
            tx = instance.functions.mintBatch(
                recipient_address, token_ids, mint_quantities, data
            ).buildTransaction(
                {
                    "gas": gas,
                    "gasPrice": ledger_api.api.toWei("50", "gwei"),
                    "nonce": nonce,
                }
            )
            tx = cls._try_estimate_gas(ledger_api, tx)
            return tx
        if ledger_api.identifier in [CosmosApi.identifier, FetchAIApi.identifier]:
            tokens = []
            for token_id, quantity in zip(token_ids, mint_quantities):
                tokens.append({"id": str(token_id), "value": str(quantity)})

            msg = {
                "mint_batch": {
                    "to_address": recipient_address,
                    "data": str(data),
                    "tokens": tokens,
                }
            }
            cosmos_api = cast(CosmosApi, ledger_api)
            tx = cosmos_api.get_handle_transaction(
                deployer_address, contract_address, msg, amount=0, tx_fee=0, gas=gas
            )
            return tx
        raise NotImplementedError

    @classmethod
    def validate_mint_quantities(
        cls, token_ids: List[int], mint_quantities: List[int]
    ) -> None:
        """Validate the mint quantities."""
        for token_id, mint_quantity in zip(token_ids, mint_quantities):
            decoded_type = cls.decode_id(token_id)
            if decoded_type not in [
                1,
                2,
            ]:
                raise ValueError(
                    "The token type must be 1 or 2. Found type={} for token_id={}".format(
                        decoded_type, token_id
                    )
                )
            if decoded_type == 1:
                if mint_quantity != 1:
                    raise ValueError(
                        "Cannot mint NFT (token_id={}) with mint_quantity more than 1 (found={})".format(
                            token_id, mint_quantity
                        )
                    )

    @staticmethod
    def decode_id(token_id: int) -> int:
        """
        Decode a give token id.

        :param token_id: the byte shifted token id
        :return: the non-shifted id
        """
        decoded_type = token_id >> 128
        return decoded_type

    @classmethod
    def get_mint_single_transaction(
        cls,
        ledger_api: LedgerApi,
        contract_address: Address,
        deployer_address: Address,
        recipient_address: Address,
        token_id: int,
        mint_quantity: int,
        data: Optional[bytes] = b"",
        gas: int = 300000,
    ) -> Dict[str, Any]:
        """
        Get the transaction to mint a single token.

        :param ledger_api: the ledger API
        :param contract_address: the address of the contract
        :param deployer_address: the address of the deployer
        :param recipient_address: the address of the recipient
        :param token_id: the token id
        :param mint_quantity: the quantity to mint
        :param data: the data to include in the transaction
        :param gas: the gas to be used
        :return: the transaction object
        """
        if ledger_api.identifier == EthereumApi.identifier:
            nonce = ledger_api.api.eth.getTransactionCount(deployer_address)
            instance = cls.get_instance(ledger_api, contract_address)
            tx = instance.functions.mint(
                recipient_address, token_id, mint_quantity, data
            ).buildTransaction(
                {
                    "gas": gas,
                    "gasPrice": ledger_api.api.toWei("50", "gwei"),
                    "nonce": nonce,
                }
            )
            tx = cls._try_estimate_gas(ledger_api, tx)
            return tx
        if ledger_api.identifier in [CosmosApi.identifier, FetchAIApi.identifier]:
            msg = {
                "mint_single": {
                    "to_address": recipient_address,
                    "id": str(token_id),
                    "supply": str(mint_quantity),
                    "data": str(data),
                }
            }
            cosmos_api = cast(CosmosApi, ledger_api)
            tx = cosmos_api.get_handle_transaction(
                deployer_address, contract_address, msg, amount=0, tx_fee=0, gas=gas
            )
            return tx
        raise NotImplementedError

    @classmethod
    def get_balance(
        cls,
        ledger_api: LedgerApi,
        contract_address: Address,
        agent_address: Address,
        token_id: int,
    ) -> Dict[str, Dict[int, int]]:
        """
        Get the balance for a specific token id.

        :param ledger_api: the ledger API
        :param contract_address: the address of the contract
        :param agent_address: the address
        :param token_id: the token id
        :return: the balance in a dictionary - {"balance": {token_id: int, balance: int}}
        """
        if ledger_api.identifier == EthereumApi.identifier:
            instance = cls.get_instance(ledger_api, contract_address)
            balance = instance.functions.balanceOf(agent_address, token_id).call()
            result = {token_id: balance}
            return {"balance": result}
        if ledger_api.identifier in [CosmosApi.identifier, FetchAIApi.identifier]:
            cosmos_api = cast(CosmosApi, ledger_api)
            msg = {"balance": {"address": str(agent_address), "id": str(token_id)}}
            query_res = cosmos_api.try_execute_wasm_query(contract_address, msg)
            query_json_res = json.loads(query_res)
            # Convert {"balance": balance: str} balances to Dict[token_id: int, balance: int]
            result = {token_id: int(query_json_res["balance"])}
            return {"balance": result}
        raise NotImplementedError

    @classmethod
    def get_atomic_swap_single_transaction(
        cls,
        ledger_api: LedgerApi,
        contract_address: Address,
        from_address: Address,
        to_address: Address,
        token_id: int,
        from_supply: int,
        to_supply: int,
        value: int,
        trade_nonce: int,
        signature: str,
        data: Optional[bytes] = b"",
        gas: int = 2818111,
    ) -> Dict[str, Any]:
        """
        Get the transaction for a trustless trade between two agents for a single token.

        :param ledger_api: the ledger API
        :param contract_address: the address of the contract
        :param from_address: the address of the agent sending tokens, receiving ether
        :param to_address: the address of the agent receiving tokens, sending ether
        :param token_id: the token id
        :param from_supply: the supply of tokens by the sender
        :param to_supply: the supply of tokens by the receiver
        :param value: the amount of ether sent from the to_address to the from_address
        :param trade_nonce: the nonce of the trade, this is separate from the nonce of the transaction
        :param signature: the signature of the trade
        :param data: the data to include in the transaction
        :param gas: the gas to be used
        :return: a ledger transaction object
        """
        if ledger_api.identifier == EthereumApi.identifier:
            nonce = ledger_api.api.eth.getTransactionCount(from_address)
            instance = cls.get_instance(ledger_api, contract_address)
            value_eth_wei = ledger_api.api.toWei(value, "ether")
            tx = instance.functions.trade(
                from_address,
                to_address,
                token_id,
                from_supply,
                to_supply,
                value_eth_wei,
                trade_nonce,
                signature,
                data,
            ).buildTransaction(
                {
                    "gas": gas,
                    "from": from_address,
                    "value": value_eth_wei,
                    "gasPrice": ledger_api.api.toWei("50", "gwei"),
                    "nonce": nonce,
                }
            )
            tx = cls._try_estimate_gas(ledger_api, tx)
            return tx
        raise NotImplementedError

    @classmethod
    def get_balances(
        cls,
        ledger_api: LedgerApi,
        contract_address: Address,
        agent_address: Address,
        token_ids: List[int],
    ) -> Dict[str, Dict[int, int]]:
        """
        Get the balances for a batch of specific token ids.

        :param ledger_api: the ledger API
        :param contract_address: the address of the contract
        :param agent_address: the address
        :param token_ids: the token id
        :return: the balances in dictionary - {"balances": {id: int, balance: int}}
        """
        if ledger_api.identifier == EthereumApi.identifier:
            instance = cls.get_instance(ledger_api, contract_address)
            balances = instance.functions.balanceOfBatch(
                [agent_address] * 10, token_ids
            ).call()
            result = dict(zip(token_ids, balances))
            return {"balances": result}
        if ledger_api.identifier in [CosmosApi.identifier, FetchAIApi.identifier]:
            tokens = []
            for token_id in token_ids:
                tokens.append({"address": agent_address, "id": str(token_id)})

            msg = {"balance_batch": {"addresses": tokens}}

            cosmos_api = cast(CosmosApi, ledger_api)
            query_res = cosmos_api.try_execute_wasm_query(contract_address, msg)
            query_json_res = json.loads(query_res)
            # Convert List[balances: str] balances to Dict[token_id: int, balance: int]
            result = {
                token_id: int(balance)
                for token_id, balance in zip(token_ids, query_json_res["balances"])
            }
            return {"balances": result}
        raise NotImplementedError

    @classmethod
    def get_atomic_swap_batch_transaction(
        cls,
        ledger_api: LedgerApi,
        contract_address: Address,
        from_address: Address,
        to_address: Address,
        token_ids: List[int],
        from_supplies: List[int],
        to_supplies: List[int],
        value: int,
        trade_nonce: int,
        signature: str,
        data: Optional[bytes] = b"",
        gas: int = 2818111,
    ) -> str:
        """
        Get the transaction for a trustless trade between two agents for a batch of tokens.

        :param ledger_api: the ledger API
        :param contract_address: the address of the contract
        :param from_address: the address of the agent sending tokens, receiving ether
        :param to_address: the address of the agent receiving tokens, sending ether
        :param token_id: the token id
        :param from_supply: the supply of tokens by the sender
        :param to_supply: the supply of tokens by the receiver
        :param value: the amount of ether sent from the to_address to the from_address
        :param trade_nonce: the nonce of the trade, this is separate from the nonce of the transaction
        :param signature: the signature of the trade
        :param data: the data to include in the transaction
        :param gas: the gas to be used
        :return: a ledger transaction object
        """
        if ledger_api.identifier == EthereumApi.identifier:
            nonce = ledger_api.api.eth.getTransactionCount(from_address)
            instance = cls.get_instance(ledger_api, contract_address)
            value_eth_wei = ledger_api.api.toWei(value, "ether")
            tx = instance.functions.tradeBatch(
                from_address,
                to_address,
                token_ids,
                from_supplies,
                to_supplies,
                value_eth_wei,
                trade_nonce,
                signature,
                data,
            ).buildTransaction(
                {
                    "gas": gas,
                    "from": from_address,
                    "value": value_eth_wei,
                    "gasPrice": ledger_api.api.toWei("50", "gwei"),
                    "nonce": nonce,
                }
            )
            return tx
        raise NotImplementedError

    @classmethod
    def get_hash_single(
        cls,
        ledger_api: LedgerApi,
        contract_address: Address,
        from_address: Address,
        to_address: Address,
        token_id: int,
        from_supply: int,
        to_supply: int,
        value: int,
        trade_nonce: int,
    ) -> bytes:
        """
        Get the hash for a trustless trade between two agents for a single token.

        :param ledger_api: the ledger API
        :param contract_address: the address of the contract
        :param from_address: the address of the agent sending tokens, receiving ether
        :param to_address: the address of the agent receiving tokens, sending ether
        :param token_id: the token id
        :param from_supply: the supply of tokens by the sender
        :param to_supply: the supply of tokens by the receiver
        :param value: the amount of ether sent from the to_address to the from_address
        :param ledger_api: the ledger API
        :return: the transaction hash in a dict
        """
        if ledger_api.identifier == EthereumApi.identifier:
            instance = cls.get_instance(ledger_api, contract_address)
            from_address_hash = instance.functions.getAddress(from_address).call()
            to_address_hash = instance.functions.getAddress(to_address).call()
            value_eth_wei = ledger_api.api.toWei(value, "ether")
            tx_hash = cls._get_hash_single(
                _from=from_address_hash,
                _to=to_address_hash,
                _id=token_id,
                _from_value=from_supply,
                _to_value=to_supply,
                _value_eth_wei=value_eth_wei,
                _nonce=trade_nonce,
            )
            if (
                tx_hash
                != instance.functions.getSingleHash(
                    from_address,
                    to_address,
                    token_id,
                    from_supply,
                    to_supply,
                    value_eth_wei,
                    trade_nonce,
                ).call()
            ):
                raise ValueError(
                    "On-chain and off-chain hash computation do not agree!"
                )
            return tx_hash
        raise NotImplementedError

    @staticmethod
    def _get_hash_single(
        _from: bytes,
        _to: bytes,
        _id: int,
        _from_value: int,
        _to_value: int,
        _value_eth_wei: int,
        _nonce: int,
    ) -> bytes:
        """
        Generate a hash mirroring the way we are creating this in the contract.

        :param _from: the from address hashed
        :param _to: the to address hashed
        :param _ids: the token ids
        :param _from_value: the from value
        :param _to_value: the to value
        :param _value_eth_wei: the value eth (in wei)
        :param _nonce: the trade nonce
        :return: the hash in bytes string representation
        """
        return keccak256(
            b"".join(
                [
                    _from,
                    _to,
                    _id.to_bytes(32, "big"),
                    _from_value.to_bytes(32, "big"),
                    _to_value.to_bytes(32, "big"),
                    _value_eth_wei.to_bytes(32, "big"),
                    _nonce.to_bytes(32, "big"),
                ]
            )
        )

    @classmethod
    def get_hash_batch(
        cls,
        ledger_api: LedgerApi,
        contract_address: Address,
        from_address: Address,
        to_address: Address,
        token_ids: List[int],
        from_supplies: List[int],
        to_supplies: List[int],
        value: int,
        trade_nonce: int,
    ) -> bytes:
        """
        Get the hash for a trustless trade between two agents for a single token.

        :param ledger_api: the ledger API
        :param contract_address: the address of the contract
        :param from_address: the address of the agent sending tokens, receiving ether
        :param to_address: the address of the agent receiving tokens, sending ether
        :param token_ids: the list of token ids for the bash transaction
        :param from_supplies: the quantities of tokens sent from the from_address to the to_address
        :param to_supplies: the quantities of tokens sent from the to_address to the from_address
        :param value: the value of ether sent from the from_address to the to_address
        :param trade_nonce: the trade nonce
        :return: the transaction hash in a dict
        """
        if ledger_api.identifier == EthereumApi.identifier:
            instance = cls.get_instance(ledger_api, contract_address)
            from_address_hash = instance.functions.getAddress(from_address).call()
            to_address_hash = instance.functions.getAddress(to_address).call()
            value_eth_wei = ledger_api.api.toWei(value, "ether")
            tx_hash = cls._get_hash_batch(
                _from=from_address_hash,
                _to=to_address_hash,
                _ids=token_ids,
                _from_values=from_supplies,
                _to_values=to_supplies,
                _value_eth_wei=value_eth_wei,
                _nonce=trade_nonce,
            )
            if (
                tx_hash
                != instance.functions.getHash(
                    from_address,
                    to_address,
                    token_ids,
                    from_supplies,
                    to_supplies,
                    value_eth_wei,
                    trade_nonce,
                ).call()
            ):
                raise ValueError(
                    "On-chain and off-chain hash computation do not agree!"
                )
            return tx_hash
        raise NotImplementedError

    @staticmethod
    def _get_hash_batch(
        _from: bytes,
        _to: bytes,
        _ids: List[int],
        _from_values: List[int],
        _to_values: List[int],
        _value_eth_wei: int,
        _nonce: int,
    ) -> bytes:
        """
        Generate a hash mirroring the way we are creating this in the contract.

        :param _from: the from address hashed
        :param _to: the to address hashed
        :param _ids: the token ids
        :param _from_values: the from values
        :param _to_values: the to values
        :param _value_eth_wei: the value of eth (in wei)
        :param _nonce: the trade nonce
        :return: the hash in bytes string representation
        """
        aggregate_hash = keccak256(
            b"".join(
                [
                    _ids[0].to_bytes(32, "big"),
                    _from_values[0].to_bytes(32, "big"),
                    _to_values[0].to_bytes(32, "big"),
                ]
            )
        )
        for idx, _id in enumerate(_ids):
            if not idx == 0:
                aggregate_hash = keccak256(
                    b"".join(
                        [
                            aggregate_hash,
                            _id.to_bytes(32, "big"),
                            _from_values[idx].to_bytes(32, "big"),
                            _to_values[idx].to_bytes(32, "big"),
                        ]
                    )
                )

        m_list = []
        m_list.append(_from)
        m_list.append(_to)
        m_list.append(aggregate_hash)
        m_list.append(_value_eth_wei.to_bytes(32, "big"))
        m_list.append(_nonce.to_bytes(32, "big"))
        return keccak256(b"".join(m_list))

    @classmethod
    def generate_trade_nonce(
        cls, ledger_api: LedgerApi, contract_address: Address, agent_address: Address
    ) -> Dict[str, int]:
        """
        Generate a valid trade nonce.

        :param ledger_api: the ledger API
        :param contract_address: the address of the contract
        :param agent_address: the address to use
        :return: the generated trade nonce
        """
        if ledger_api.identifier == EthereumApi.identifier:
            instance = cls.get_instance(ledger_api, contract_address)
            trade_nonce = random.randrange(0, MAX_UINT_256)  # nosec
            while instance.functions.is_nonce_used(agent_address, trade_nonce).call():
                trade_nonce = random.randrange(0, MAX_UINT_256)  # nosec
            return {"trade_nonce": trade_nonce}
        raise NotImplementedError

    @staticmethod
    def _try_estimate_gas(ledger_api: LedgerApi, tx: Dict[str, Any]) -> Dict[str, Any]:
        """
        Attempts to update the transaction with a gas estimate.

        :param ledger_api: the ledger API
        :param tx: the transaction
        :return: the transaction (potentially updated)
        """
        try:
            # try estimate the gas and update the transaction dict
            gas_estimate = ledger_api.api.eth.estimateGas(transaction=tx)
            _default_logger.debug(
                "[ERC1155Contract]: gas estimate: {}".format(gas_estimate)
            )
            tx["gas"] = gas_estimate
        except Exception as e:  # pylint: disable=broad-except
            _default_logger.debug(
                "[ERC1155Contract]: Error when trying to estimate gas: {}".format(e)
            )
        return tx

    @staticmethod
    def get_last_code_id(ledger_api: LedgerApi) -> int:
        """
        Uses wasmcli to get ID of latest deployed .wasm bytecode

        :param ledger_api: the ledger API

        :return: code id of last deployed .wasm bytecode
        """
        if ledger_api.identifier in [CosmosApi.identifier, FetchAIApi.identifier]:
            cosmos_api = cast(CosmosApi, ledger_api)
            return cosmos_api.get_last_code_id()
        raise NotImplementedError

    @staticmethod
    def get_contract_address(ledger_api: LedgerApi, code_id: int) -> str:
        """
        Uses wasmcli to get contract address of latest initialised contract by its ID

        :param ledger_api: the ledger API
        :param code_id: the ID of stored contract CosmWasm

        :return: contract address of last initialised contract
        """
        if ledger_api.identifier in [CosmosApi.identifier, FetchAIApi.identifier]:
            cosmos_api = cast(CosmosApi, ledger_api)
            return cosmos_api.get_contract_address(code_id)
        raise NotImplementedError
