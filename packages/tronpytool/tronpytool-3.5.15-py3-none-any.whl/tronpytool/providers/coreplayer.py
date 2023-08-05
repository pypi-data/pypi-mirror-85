#!/usr/bin/env python
# coding: utf-8


import codecs
import json
import os
import random
import string
import time

from tronpytool import Tron
from tronpytool.compile.basetest import WrapContract
from tronpytool.trx import Trx

INVITE = "invitecode"
UPLINE = "upline"


class CoreSimulatePlayers:
    """DEFI Contract deployment
       the player with game
        """
    statement = 'End : {}, IO File {}'
    _contract_dict: dict
    _network: str
    FILE_CONTRACT = "backedup"
    ACTION_FOLDER = "deploy_results"
    COLLECTION_CONTRACTS = "players"
    GENESIS_INVITE_CODE = "DPXUS"
    GENESIS_UPLINE_CODE = "OOOOO"

    def __init__(self, network: str, workspace: str):
        self._contract_dict = dict()
        self._tron_clients = dict()
        self._workspace = workspace
        self._network = network
        """try to load up the file from the existing path"""
        try:
            self._contract_dict = json.load(codecs.open(self.playerAddrsFilePath(), 'r', 'utf-8-sig'))
            print("==== 🛄 data is prepared and the player metadata is now ready... ")
            self.preview_all_addresses()
            print("==== 🛄 End ==== ")
        except FileNotFoundError:
            pass
        except TypeError as e:
            print(e)

    def _writeFile(self, content, filename: str) -> None:
        fo = open(filename, "w")
        fo.write(content)
        fo.close()
        print(self.statement.format(time.ctime(), filename))

    def _storeTxDict(self, tx_result_data, filepath) -> None:
        self._writeFile(json.dumps(tx_result_data, ensure_ascii=False), filepath)

    @property
    def backupname(self) -> str:
        """preview the file name"""
        return self.FILE_CONTRACT

    @backupname.setter
    def backupname(self, filename: str) -> None:
        """the file name does not require extension name"""
        self.FILE_CONTRACT = filename

    @property
    def playermeta_data(self) -> str:
        return self.COLLECTION_CONTRACTS

    @playermeta_data.setter
    def playermeta_data(self, path: str) -> None:
        self.COLLECTION_CONTRACTS = path

    def getGroupByAddr(self, keyname: str) -> dict:
        """example: TT67rPNwgmpeimvHUMVzFfKsjL9GZ1wGw8"""
        return self._contract_dict.get(keyname)

    def getAllAddress(self) -> dict:
        return self._contract_dict

    def preview_all_addresses(self) -> None:
        print(self._contract_dict)

    def playerAddrsFilePath(self) -> str:
        return os.path.join(self._workspace, self.ACTION_FOLDER,
                            "{}.json".format(self.COLLECTION_CONTRACTS))

    def GetMetadataByAddr(self, address: str) -> dict:
        return self._contract_dict[address]

    def SaveMetaFile(self) -> "CoreSimulatePlayers":
        self._storeTxDict(self._contract_dict, self.playerAddrsFilePath())
        return self

    def SyncBalances(self) -> "CoreSimulatePlayers":
        if len(self._contract_dict) > 0:
            for address in self._contract_dict:
                amount = self.GetTronModule(address).get_balance(address, False)
                self._contract_dict[address]["balance"] = amount
                print("===✅ balance: {} trx --> {}".format(amount, address))

        return self

    def AppendInitPlayer(self, address_wallet: str, private_key: str) -> "CoreSimulatePlayers":
        amount = self.GetTronModule(address_wallet).get_balance(address_wallet, False)
        self._contract_dict[address_wallet] = dict(
            balance=amount,
            upline="",
            invitecode="",
            privkey=private_key,
        )
        return self

    def GetTronModule(self, address: str) -> "Trx":
        return self.GetTronByAddr(address).trx

    def GetTronByAddr(self, address: str) -> Tron:
        if not address in self._tron_clients:
            address_wallet = self._contract_dict[address]
            privatekey = self._contract_dict[address]["privkey"]
            tron = WrapContract(self._network).setMasterKey(address_wallet, privatekey).getClientTron()
            self._tron_clients[address] = tron
            print("===✅ Tron client initiated for --> {}".format(address))

        return self._tron_clients[address]

    def _set_upline_code(self, address: str, line: str) -> None:
        if len(self._contract_dict) > 0:
            if UPLINE in self._contract_dict[address]:
                self._contract_dict[address][UPLINE] = line

    def _set_invite_code(self, address: str, invite: str) -> None:
        if len(self._contract_dict) > 0:
            if INVITE in self._contract_dict[address]:
                self._contract_dict[address][INVITE] = invite

    def NewMemberSetup(self, address: str, invite: str, upline: str) -> None:
        self._set_invite_code(address, invite)
        self._set_upline_code(address, upline)
        print("==> new member with invite code: {}, and upline code: {}".format(invite, upline))

    def NewInviteCode(self) -> str:
        return ''.join(random.sample(string.ascii_uppercase, 5))

    def is_empty_data(self) -> bool:
        return not len(self._contract_dict) > 0

    def GetUplineCode(self) -> str:
        if len(self._contract_dict) > 0:
            for address in self._contract_dict:
                uplinecode = self._contract_dict[address][UPLINE]
                invitecode = self._contract_dict[address][INVITE]
                if len(uplinecode) > 0 and len(invitecode) > 0:
                    return invitecode
            return self.GENESIS_INVITE_CODE
        else:
            return self.GENESIS_UPLINE_CODE
