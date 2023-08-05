#!/usr/bin/env python3

# Copyright (C) 2020 The btclib developers
#
# This file is part of btclib. It is subject to the license terms in the
# LICENSE file found in the top-level directory of this distribution.
#
# No part of btclib including this file, may be copied, modified, propagated,
# or distributed except according to the terms contained in the LICENSE file.

"""Partially Signed Bitcoin Transaction.

https://en.bitcoin.it/wiki/BIP_0174
"""

from base64 import b64decode, b64encode
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Type, TypeVar, Union

from dataclasses_json import DataClassJsonMixin

from . import script, varint
from .alias import Octets, ScriptToken, String
from .bip32 import bytes_from_bip32_path
from .psbt_in import PartialSigs, PsbtIn
from .psbt_out import HdKeyPaths, PsbtOut
from .scriptpubkey import payload_from_scriptPubKey
from .tx import Tx
from .tx_out import TxOut
from .utils import (
    bytes_from_octets,
    hash160,
    sha256,
    token_or_string_to_hex_string,
)

_PSbt = TypeVar("_PSbt", bound="Psbt")

_PSBT_MAGIC_BYTES = b"psbt"
_PSBT_SEPARATOR = b"\xff"
_PSBT_DELIMITER = b"\x00"

_PSBT_UNSIGNED_TX = b"\x00"
_PSBT_XPUB = b"\x01"
_PSBT_VERSION = b"\xfb"
_PSBT_PROPRIETARY = b"\xfc"


@dataclass
class Psbt(DataClassJsonMixin):
    tx: Tx = field(default=Tx())
    inputs: List[PsbtIn] = field(default_factory=list)
    outputs: List[PsbtOut] = field(default_factory=list)
    version: Optional[int] = 0
    hd_keypaths: HdKeyPaths = field(default_factory=HdKeyPaths)
    proprietary: Dict[int, Dict[str, bytes]] = field(default_factory=dict)
    unknown: Dict[str, bytes] = field(default_factory=dict)

    @classmethod
    def deserialize(cls: Type[_PSbt], data: bytes, assert_valid: bool = True) -> _PSbt:

        out = cls()

        assert data[:4] == _PSBT_MAGIC_BYTES, "malformed psbt: missing magic bytes"
        assert data[4:5] == _PSBT_SEPARATOR, "malformed psbt: missing separator"

        global_map, data = deserialize_map(data[5:])
        for key, value in global_map.items():
            if key[0:1] == _PSBT_UNSIGNED_TX:
                assert len(key) == 1, f"invalid key length: {len(key)}"
                assert not out.tx.nVersion, "duplicated transaction"
                out.tx = Tx.deserialize(value)  # legacy trensaction
            elif key[0:1] == _PSBT_XPUB:
                # TODO duplicated?
                # why extended key here?
                assert len(key) == 78 + 1, f"invalid key length: {len(key)}"
                out.hd_keypaths.add_hd_keypath(key[1:], value[:4], value[4:])
            elif key[0:1] == _PSBT_VERSION:
                assert len(key) == 1, f"invalid key length: {len(key)}"
                assert not out.version, "duplicated version"
                assert len(value) == 4, f"invalid version length: {len(value)}"
                out.version = int.from_bytes(value, "little")
            elif key[0:1] == _PSBT_PROPRIETARY:
                # TODO duplicated?
                prefix = varint.decode(key[1:])
                if prefix not in out.proprietary.keys():
                    out.proprietary[prefix] = {}
                key = key[1 + len(varint.encode(prefix)) :]
                out.proprietary[prefix][key.hex()] = value
            else:  # unknown keys
                # TODO duplicated?
                out.unknown[key.hex()] = value

        assert out.tx.nVersion, "missing transaction"
        for _ in out.tx.vin:
            input_map, data = deserialize_map(data)
            out.inputs.append(PsbtIn.deserialize(input_map))
        for _ in out.tx.vout:
            output_map, data = deserialize_map(data)
            out.outputs.append(PsbtOut.deserialize(output_map))

        if assert_valid:
            out.assert_valid()
        return out

    @classmethod
    def decode(cls: Type[_PSbt], string: str, assert_valid: bool = True) -> _PSbt:
        data = b64decode(string)
        return cls.deserialize(data, assert_valid)

    def serialize(self, assert_valid: bool = True) -> bytes:

        if assert_valid:
            self.assert_valid()

        out = _PSBT_MAGIC_BYTES + _PSBT_SEPARATOR

        out += b"\x01" + _PSBT_UNSIGNED_TX
        tx = self.tx.serialize()
        out += varint.encode(len(tx)) + tx
        if self.hd_keypaths:
            for xpub, hd_keypath in self.hd_keypaths.hd_keypaths.items():
                out += b"\x4f\x01" + bytes.fromhex(xpub)
                keypath = bytes.fromhex(hd_keypath["fingerprint"])
                keypath += bytes_from_bip32_path(
                    hd_keypath["derivation_path"], "little"
                )
                out += varint.encode(len(keypath)) + keypath
        if self.version:
            out += b"\x01" + _PSBT_VERSION
            out += b"\x04" + self.version.to_bytes(4, "little")
        if self.proprietary:
            for (owner, dictionary) in self.proprietary.items():
                for key, value in dictionary.items():
                    key_bytes = (
                        _PSBT_PROPRIETARY + varint.encode(owner) + bytes.fromhex(key)
                    )
                    out += varint.encode(len(key_bytes)) + key_bytes
                    out += varint.encode(len(value)) + value
        if self.unknown:
            for key, value in self.unknown.items():
                out += varint.encode(len(key) // 2) + bytes.fromhex(key)
                out += varint.encode(len(value)) + value

        out += _PSBT_DELIMITER
        for input_map in self.inputs:
            out += input_map.serialize() + b"\x00"
        for output_map in self.outputs:
            out += output_map.serialize() + b"\x00"
        return out

    def encode(self, assert_valid: bool = True) -> str:
        out = self.serialize(assert_valid)
        return b64encode(out).decode("ascii")

    def assert_valid(self) -> None:
        "Assert logical self-consistency."

        self.tx.assert_valid()
        assert len(self.tx.vin) == len(
            self.inputs
        ), "mismatched number of tx.vin and psbt_in"
        for vin in self.tx.vin:
            assert vin.scriptSig == b""
            assert vin.txinwitness == []
        assert len(self.tx.vout) == len(
            self.outputs
        ), "mismatched number of tx.vout and psbt_out"

        for psbt_in in self.inputs:
            psbt_in.assert_valid()

        for psbt_out in self.outputs:
            psbt_out.assert_valid()

        # TODO: validate version
        # TODO: validate hd_keypaths
        # TODO: validate proprietary
        # TODO: validate unknown

    def assert_signable(self) -> None:

        for i, tx_in in enumerate(self.tx.vin):

            non_witness_utxo = self.inputs[i].non_witness_utxo
            witness_utxo = self.inputs[i].witness_utxo

            if non_witness_utxo:
                txid = tx_in.prevout.hash
                assert isinstance(non_witness_utxo, Tx)
                assert non_witness_utxo.txid == txid

            if witness_utxo:
                assert isinstance(witness_utxo, TxOut)
                scriptPubKey = witness_utxo.scriptPubKey
                script_type = payload_from_scriptPubKey(scriptPubKey)[0]
                if script_type == "p2sh":
                    scriptPubKey = self.inputs[i].redeem_script
                script_type = payload_from_scriptPubKey(scriptPubKey)[0]
                assert script_type in ["p2wpkh", "p2wsh"]

            if self.inputs[i].redeem_script:
                if non_witness_utxo:
                    scriptPubKey = non_witness_utxo.vout[tx_in.prevout.n].scriptPubKey
                elif witness_utxo:
                    scriptPubKey = witness_utxo.scriptPubKey
                hash = hash160(self.inputs[i].redeem_script)
                assert hash == payload_from_scriptPubKey(scriptPubKey)[1]

            if self.inputs[i].witness_script:
                if non_witness_utxo:
                    scriptPubKey = non_witness_utxo.vout[tx_in.prevout.n].scriptPubKey
                elif witness_utxo:
                    scriptPubKey = witness_utxo.scriptPubKey
                if self.inputs[i].redeem_script:
                    scriptPubKey = self.inputs[i].redeem_script

                hash = sha256(self.inputs[i].witness_script)
                assert hash == payload_from_scriptPubKey(scriptPubKey)[1]

    def add_unknown(self, key: String, val: Octets):

        key_str = token_or_string_to_hex_string(key)

        self.unknown[key_str] = bytes_from_octets(val)

    def get_unknown(self, key: String) -> bytes:

        key_str = token_or_string_to_hex_string(key)

        return self.unknown[key_str]


def deserialize_map(data: bytes) -> Tuple[Dict[bytes, bytes], bytes]:
    assert len(data) != 0, "Malformed psbt: at least a map is missing"
    partial_map: Dict[bytes, bytes] = {}
    while True:
        if data[0] == 0:
            data = data[1:]
            return partial_map, data
        key_len = varint.decode(data)
        data = data[len(varint.encode(key_len)) :]
        key = data[:key_len]
        data = data[key_len:]
        value_len = varint.decode(data)
        data = data[len(varint.encode(value_len)) :]
        value = data[:value_len]
        data = data[value_len:]
        assert key not in partial_map.keys(), "Malformed psbt: duplicate keys"
        partial_map[key] = value


def psbt_from_tx(tx: Tx) -> Psbt:
    tx = deepcopy(tx)
    for input in tx.vin:
        input.scriptSig = b""
        input.txinwitness = []
    inputs = [PsbtIn() for _ in tx.vin]
    outputs = [PsbtOut() for _ in tx.vout]
    return Psbt(tx=tx, inputs=inputs, outputs=outputs)


def _combine_field(
    psbt_map: Union[PsbtIn, PsbtOut, Psbt], out: Union[PsbtIn, PsbtOut, Psbt], key: str
) -> None:
    item = getattr(psbt_map, key)
    a = getattr(out, key)
    if isinstance(item, dict) and a and isinstance(a, dict):
        a.update(item)
    elif isinstance(item, dict) or item and not a:
        setattr(out, key, item)
    elif isinstance(item, PartialSigs) and isinstance(a, PartialSigs):
        a.sigs.update(item.sigs)
    elif isinstance(item, HdKeyPaths) and isinstance(a, HdKeyPaths):
        a.hd_keypaths.update(item.hd_keypaths)
    elif item:
        assert item == a, key


def combine_psbts(psbts: List[Psbt]) -> Psbt:
    final_psbt = psbts[0]
    txid = psbts[0].tx.txid
    for psbt in psbts[1:]:
        assert psbt.tx.txid == txid

    for psbt in psbts[1:]:

        for x in range(len(final_psbt.inputs)):
            _combine_field(psbt.inputs[x], final_psbt.inputs[x], "non_witness_utxo")
            _combine_field(psbt.inputs[x], final_psbt.inputs[x], "witness_utxo")
            _combine_field(psbt.inputs[x], final_psbt.inputs[x], "partial_sigs")
            _combine_field(psbt.inputs[x], final_psbt.inputs[x], "sighash")
            _combine_field(psbt.inputs[x], final_psbt.inputs[x], "redeem_script")
            _combine_field(psbt.inputs[x], final_psbt.inputs[x], "witness_script")
            _combine_field(psbt.inputs[x], final_psbt.inputs[x], "hd_keypaths")
            _combine_field(psbt.inputs[x], final_psbt.inputs[x], "final_script_sig")
            _combine_field(psbt.inputs[x], final_psbt.inputs[x], "final_script_witness")
            _combine_field(psbt.inputs[x], final_psbt.inputs[x], "por_commitment")
            _combine_field(psbt.inputs[x], final_psbt.inputs[x], "proprietary")
            _combine_field(psbt.inputs[x], final_psbt.inputs[x], "unknown")

        for _ in final_psbt.outputs:
            _combine_field(psbt.outputs[x], final_psbt.outputs[x], "redeem_script")
            _combine_field(psbt.outputs[x], final_psbt.outputs[x], "witness_script")
            _combine_field(psbt.outputs[x], final_psbt.outputs[x], "hd_keypaths")
            _combine_field(psbt.outputs[x], final_psbt.outputs[x], "proprietary")
            _combine_field(psbt.outputs[x], final_psbt.outputs[x], "unknown")

        _combine_field(psbt, final_psbt, "tx")
        _combine_field(psbt, final_psbt, "version")
        _combine_field(psbt, final_psbt, "hd_keypaths")
        _combine_field(psbt, final_psbt, "proprietary")
        _combine_field(psbt, final_psbt, "unknown")

    return final_psbt


def finalize_psbt(psbt: Psbt) -> Psbt:
    psbt = deepcopy(psbt)
    for psbt_in in psbt.inputs:
        assert psbt_in.partial_sigs, "missing signatures"
        sigs = psbt_in.partial_sigs.sigs.values()
        multi_sig = len(sigs) > 1
        if psbt_in.witness_script:
            psbt_in.final_script_sig = script.serialize([psbt_in.redeem_script.hex()])
            psbt_in.final_script_witness = [b""] if multi_sig else []
            psbt_in.final_script_witness += sigs
            psbt_in.final_script_witness += [psbt_in.witness_script]
        else:
            # https://github.com/bitcoin/bips/blob/master/bip-0147.mediawiki#motivation
            final_script_sig: List[ScriptToken] = [0] if multi_sig else []
            final_script_sig += [sig.hex() for sig in sigs]
            final_script_sig += [psbt_in.redeem_script.hex()]
            psbt_in.final_script_sig = script.serialize(final_script_sig)
        psbt_in.partial_sigs = PartialSigs()
        psbt_in.sighash = None
        psbt_in.redeem_script = b""
        psbt_in.witness_script = b""
        psbt_in.hd_keypaths = HdKeyPaths()
        psbt_in.por_commitment = None
    return psbt


def extract_tx(psbt: Psbt) -> Tx:
    tx = psbt.tx
    for i, vin in enumerate(tx.vin):
        vin.scriptSig = psbt.inputs[i].final_script_sig
        if psbt.inputs[i].final_script_witness:
            vin.txinwitness = psbt.inputs[i].final_script_witness
    return tx
