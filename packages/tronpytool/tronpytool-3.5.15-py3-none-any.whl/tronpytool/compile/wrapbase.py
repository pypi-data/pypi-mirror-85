#!/usr/bin/env python
"""Base wrapper class for accessing ethereum smart contracts."""

from typing import Any, Union, Tuple

from tronpytool import Tron
from tronpytool.common.key import to_hex_address, keccak256, is_address
from tronpytool.common.normalizers import to_checksum_address
from tronpytool.compile import abi
from tronpytool.contract import Contract
from tronpytool.exceptions import DoubleSpending
from tronpytool.transactionbuilder import TransactionBuilder


# from trx import is_list, is_object

class Validator:
    """Base class for validating inputs to methods."""

    def __init__(
            self,
            web3_or_provider: Tron,
            contract_address: str,
    ):
        """Initialize the instance."""

    def assert_valid(
            self, method_name: str, parameter_name: str, argument_value: Any
    ):
        """Raise an exception if method input is not valid.

        :param method_name: Name of the method whose input is to be validated.
        :param parameter_name: Name of the parameter whose input is to be
            validated.
        :param argument_value: Value of argument to parameter to be validated.
        """


class ContractMethod:
    def __init__(self, abi: dict, contract: Contract, owner_address: str, contract_address: str,
                 validator: Validator = None):

        self._abi = abi
        self.validator = validator
        self._owner_address = owner_address
        self._client = contract.tron.trx
        self._tron: Tron = contract.tron
        self.transaction_builder = contract.tron.transaction_builder
        self.inputs = abi.get("inputs", [])
        self.outputs = abi.get("outputs", [])
        self.method_name = abi.get("name", "")
        self.element_type = abi.get("type", "")
        self.call_value = 0
        self.call_token_value = 0
        self.call_token_id = 0
        self.contract_address = contract_address

    def __str__(self):
        return self.function_type

    @staticmethod
    def validate_and_checksum_address(address: str):
        """Validate the given address, and return it's checksum address."""
        if not is_address(address):
            raise TypeError("Invalid address provided: {}".format(address))
        return to_checksum_address(address)

    def normalize_tx_params(self, tx_params) -> dict:
        """Normalize and return the given transaction parameters."""
        params = dict()
        return params

    def with_owner(self, addr: str) -> "ContractMethod":
        """Set the calling owner address.

        Can also be changed through :meth:`TransactionBuilder.with_owner() <tronpy.tron.TransactionBuilder.with_owner>`.
        """
        self._owner_address = addr
        return self

    def with_transfer(self, amount: int) -> "ContractMethod":
        """Call a contract function with TRX transfer. ``amount`` in `SUN`."""
        self.call_value = amount
        return self

    def with_asset_transfer(self, amount: int, token_id: int) -> "ContractMethod":
        """Call a contract function with TRC10 token transfer."""
        self.call_token_value = amount
        self.call_token_id = token_id
        return self

    def call(self, *args, **kwargs) -> "TransactionBuilder":
        """Call the contract method."""
        return self.__call__(*args, **kwargs)

    def trackEventReceipt(self, trnId: str):
        event = self._tron.get_event_transaction_id(trnId)
        print("=======debug event returns on this Transaction ID {}".format(trnId))
        print(event)
        print("=======end event report ========")

    def handle_ret(self, r: dict) -> any:
        ok, key, message = self.transaction_builder.handle_ret(r)

        if ok:
            print("=======debug request result {}".format(key))
            print(r)
            print(message)
            print("=======end event report ========")
            return self.parse_output(message)
        else:
            raise KeyError('Request returns Error - {} msg:{} txt:{}'.format(key, message, self.parse_output(message)))

    def parse_output(self, raw: any) -> any:
        if type(raw) is bytes:
            """Parse contract result as result."""
            parsed_result = abi.decode_single(self.output_type, bytes.fromhex(raw))
            if len(self.outputs) == 1:
                return parsed_result[0]
            if len(self.outputs) == 0:
                return None
            return parsed_result
        else:
            return raw

    def __call__(self, *args, **kwargs) -> "TransactionBuilder":
        """Call the contract method."""
        parameter = ""

        if args and kwargs:
            raise ValueError("do not mix positional arguments and keyword arguments")

        if len(self.inputs) == 0:
            if args or kwargs:
                raise TypeError("{} expected {} arguments".format(self.name, len(self.inputs)))
        elif args:
            if len(args) != len(self.inputs):
                raise TypeError("wrong number of arguments, require {} got {}".format(len(self.inputs), len(args)))
            parameter = abi.encode_single(self.input_type, args).hex()
        elif kwargs:
            if len(kwargs) != len(self.inputs):
                raise TypeError("wrong number of arguments, require {} got {}".format(len(self.inputs), len(args)))
            args = []
            for arg in self.inputs:
                try:
                    args.append(kwargs[arg["name"]])
                except KeyError:
                    raise TypeError("missing argument '{}'".format(arg["name"]))
            parameter = abi.encode_single(self.input_type, args).hex()
        else:
            raise TypeError("wrong number of arguments, require {}".format(len(self.inputs)))

        paramdict = dict(
            contract_address=self.contract_address,
            function_selector=self.function_signature,
            issuer_address=self._owner_address,
            fee_limit=30000,
            call_value=0
        )

        if self._abi.get("stateMutability", None).lower() in ["view", "pure"]:
            # const call, contract ret
            ret = self.transaction_builder.trigger_smart_contract(paramdict)
            return self.handle_ret(ret)
        else:
            paramdict.setdefault('parameters', []).append(parameter)
            ret = self.transaction_builder.trigger_smart_contract(paramdict)
            return self.handle_ret(ret)

    @property
    def name(self) -> str:
        return self._abi["name"]

    @property
    def input_type(self) -> str:
        return "(" + (",".join(self.__format_json_abi_type_entry(arg) for arg in self.inputs)) + ")"

    @property
    def output_type(self) -> str:
        return "({})".format(",".join(self.__format_json_abi_type_entry(arg) for arg in self.outputs))

    def __format_json_abi_type_entry(self, entry) -> str:
        if entry['type'].startswith('tuple'):
            surfix = entry['type'][5:]
            if 'components' not in entry:
                raise ValueError("ABIEncoderV2 used, ABI should be set by hand")
            return "({}){}".format(
                ",".join(self.__format_json_abi_type_entry(arg) for arg in entry['components']), surfix
            )
        else:
            return entry['type']

    @property
    def function_signature(self) -> str:
        return self.name + self.input_type

    @property
    def function_signature_hash(self) -> str:
        return keccak256(self.function_signature.encode())[:4].hex()

    @property
    def function_type(self) -> str:
        types = ", ".join(arg["type"] + " " + arg.get("name", "") for arg in self.inputs)
        ret = "function {}({})".format(self.name, types)
        if self._abi.get("stateMutability", None).lower() == "view":
            ret += " view"
        elif self._abi.get("stateMutability", None).lower() == "pure":
            ret += " pure"
        if self.outputs:
            ret += " returns ({})".format(", ".join(arg["type"] + " " + arg.get("name", "") for arg in self.outputs))
        return ret

    def as_shielded_trc20(self, contractaddr: str) -> "ShieldedTRC20":
        return ShieldedTRC20(self._contract, self._tron, contractaddr)


class ShieldedTRC20(object):
    """Shielded TRC20 Wrapper."""

    def __init__(self, contract: Contract, client: Tron, address: str):
        self.shielded = address
        """The shielded TRC20 contract."""
        self._client = client
        self._trx_module = client.trx
        self._contract = contract
        # lazy properties
        self._trc20 = None
        self._scale_factor = None

    @property
    def trc20(self) -> Contract:
        """The corresponding TRC20 contract."""
        if self._trc20 is None:
            trc20_address = "41" + str(self.shielded)._bytecode[-52:-32].hex()
            self._trc20 = self._trx_module.get_contract(trc20_address)
        return self._trc20

    @property
    def scale_factor(self) -> int:
        """Scaling factor of the shielded contract."""
        if self._scale_factor is None:
            self._scale_factor = self._contract.functions.scalingFactor()
        return self._scale_factor

    def get_rcm(self) -> str:
        return self._client.manager.request("wallet/getrcm")["value"]

    def mint(self, taddr: str, zaddr: str, amount: int, memo: str = "") -> "TransactionBuilder":
        """Mint, transfer from T-address to z-address."""
        rcm = self.get_rcm()
        payload = {
            "from_amount": str(amount),
            "shielded_receives": {
                "note": {
                    "value": amount // self.scale_factor,
                    "payment_address": zaddr,
                    "rcm": rcm,
                    "memo": memo.encode().hex(),
                }
            },
            "shielded_TRC20_contract_address": to_hex_address(self._contract.contract_address),
        }

        ret = self._client.manager.request("wallet/createshieldedcontractparameters", payload)
        self._client._handle_api_error(ret)
        parameter = ret["trigger_contract_input"]
        function_signature = self._contract.functions.mint.function_signature_hash
        return self._trx_module._build_transaction(
            "TriggerSmartContract",
            {
                "owner_address": to_hex_address(taddr),
                "contract_address": to_hex_address(self._contract.contract_address),
                "data": function_signature + parameter,
            },
            method=self._contract.functions.mint,
        )

    def transfer(
            self, zkey: dict, notes: Union[list, dict], *to: Union[Tuple[str, int], Tuple[str, int, str]],
    ) -> "tronpy.tron.TransactionBuilder":
        """Transfer from z-address to z-address."""
        if isinstance(notes, (dict,)):
            notes = [notes]

        assert 1 <= len(notes) <= 2

        spends = []
        spend_amount = 0
        for note in notes:
            if note.get("is_spent", False):
                raise DoubleSpending
            alpha = self.get_rcm()
            root, path = self.get_path(note.get("position", 0))
            spends.append(
                {"note": note["note"], "alpha": alpha, "root": root, "path": path, "pos": note.get("position", 0)}
            )
            spend_amount += note["note"]["value"]

        receives = []
        receive_amount = 0
        for recv in to:
            addr = recv[0]
            amount = recv[1]
            receive_amount += amount
            if len(recv) == 3:
                memo = recv[2]
            else:
                memo = ""

            rcm = self.get_rcm()

            receives.append(
                {"note": {"value": amount, "payment_address": addr, "rcm": rcm, "memo": memo.encode().hex()}}
            )

        if spend_amount != receive_amount:
            raise ValueError("spend amount is not equal to receive amount")

        payload = {
            "ask": zkey["ask"],
            "nsk": zkey["nsk"],
            "ovk": zkey["ovk"],
            "shielded_spends": spends,
            "shielded_receives": receives,
            "shielded_TRC20_contract_address": to_hex_address(self.shielded.contract_address),
        }
        ret = self._client.provider.make_request("wallet/createshieldedcontractparameters", payload)
        self._client._handle_api_error(ret)
        parameter = ret["trigger_contract_input"]
        function_signature = self.shielded.functions.transfer.function_signature_hash
        return self._trx_module._build_transaction(
            "TriggerSmartContract",
            {
                "owner_address": "0000000000000000000000000000000000000000",
                "contract_address": to_hex_address(self.shielded.contract_address),
                "data": function_signature + parameter,
            },
            method=self.shielded.functions.transfer,
        )

    def burn(
            self, zkey: dict, note: dict, *to: Union[Tuple[str, int], Tuple[str, int, str]]
    ) -> "tronpy.tron.TransactionBuilder":
        """Burn, transfer from z-address to T-address."""
        spends = []
        alpha = self.get_rcm()
        root, path = self.get_path(note.get("position", 0))
        if note.get("is_spent", False):
            raise DoubleSpending
        spends.append(
            {"note": note["note"], "alpha": alpha, "root": root, "path": path, "pos": note.get("position", 0)}
        )
        change_amount = 0
        receives = []
        to_addr = None
        to_amount = 0
        to_memo = ''
        if not to:
            raise ValueError('burn must have a output')
        for receive in to:
            addr = receive[0]
            amount = receive[1]
            if len(receive) == 3:
                memo = receive[2]
            else:
                memo = ""

            if addr.startswith('ztron1'):
                change_amount += amount
                rcm = self.get_rcm()
                receives = [
                    {"note": {"value": amount, "payment_address": addr, "rcm": rcm, "memo": memo.encode().hex()}}
                ]
            else:
                # assume T-address
                to_addr = addr
                to_amount = amount
                to_memo = memo

        if note["note"]["value"] * self.scale_factor - change_amount * self.scale_factor != to_amount:
            raise ValueError("Balance amount is wrong")

        payload = {
            "ask": zkey["ask"],
            "nsk": zkey["nsk"],
            "ovk": zkey["ovk"],
            "shielded_spends": spends,
            "shielded_receives": receives,
            "to_amount": str(to_amount),
            "transparent_to_address": to_hex_address(to_addr),
            "shielded_TRC20_contract_address": to_hex_address(self.shielded.contract_address),
        }

        ret = self._client.provider.make_request("wallet/createshieldedcontractparameters", payload)
        self._client._handle_api_error(ret)
        parameter = ret["trigger_contract_input"]
        function_signature = self.shielded.functions.burn.function_signature_hash
        txn = self._trx_module._build_transaction(
            "TriggerSmartContract",
            {
                "owner_address": "410000000000000000000000000000000000000000",
                "contract_address": to_hex_address(self.shielded.contract_address),
                "data": function_signature + parameter,
            },
            method=self.shielded.functions.burn,
        )
        if to_memo:
            txn = txn.memo(to_memo)
        return txn

    def _fix_notes(self, notes: list) -> list:
        for note in notes:
            if "position" not in note:
                note["position"] = 0
            if "is_spent" not in note:
                note["is_spent"] = False
            # if "memo" in note["note"]:
            #     note["note"]["memo"] = bytes.fromhex(note["note"]["memo"]).decode("utf8", 'ignore')
        return notes

    # use zkey pair from wallet/getnewshieldedaddress
    def scan_incoming_notes(self, zkey: dict, start_block_number: int, end_block_number: int = None) -> list:
        """Scan incoming notes using ivk, ak, nk."""
        if end_block_number is None:
            end_block_number = start_block_number + 1000
        payload = {
            "start_block_index": start_block_number,
            "end_block_index": end_block_number,
            "shielded_TRC20_contract_address": to_hex_address(self.shielded.contract_address),
            "ivk": zkey["ivk"],
            "ak": zkey["ak"],
            "nk": zkey["nk"],
        }
        ret = self._client.provider.make_request("wallet/scanshieldedtrc20notesbyivk", payload)
        self._client._handle_api_error(ret)
        return self._fix_notes(ret.get("noteTxs", []))

    def scan_outgoing_notes(
            self, zkey_or_ovk: Union[dict, str], start_block_number: int, end_block_number: int = None
    ) -> list:
        """Scan outgoing notes using ovk."""
        if end_block_number is None:
            end_block_number = start_block_number + 1000

        ovk = zkey_or_ovk
        if isinstance(zkey_or_ovk, (dict,)):
            ovk = zkey_or_ovk["ovk"]

        payload = {
            "start_block_index": start_block_number,
            "end_block_index": end_block_number,
            "shielded_TRC20_contract_address": to_hex_address(self.shielded.contract_address),
            "ovk": ovk,
        }
        ret = self._client.provider.make_request("wallet/scanshieldedtrc20notesbyovk", payload)
        self._client._handle_api_error(ret)
        return ret.get("noteTxs", [])

    # (root, path)
    def get_path(self, position: int = 0) -> (str, str):
        root, path = self.shielded.functions.getPath(position)
        root = root.hex()
        path = "".join(p.hex() for p in path)
        return (root, path)

    def is_note_spent(self, zkey: dict, note: dict) -> bool:
        """Is a note spent."""
        payload = dict(note)
        payload["shielded_TRC20_contract_address"] = to_hex_address(self.shielded.contract_address)
        if "position" not in note:
            payload["position"] = 0
        payload["ak"] = zkey["ak"]
        payload["nk"] = zkey["nk"]

        ret = self._client.provider.make_request("wallet/isshieldedtrc20contractnotespent", payload)

        return ret.get('is_spent', None)
