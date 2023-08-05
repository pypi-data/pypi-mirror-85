#!/usr/bin/env python
# coding: utf-8
import codecs
import json
import os
import subprocess
import time

from tronpytool import Tron

ROOT = os.path.join(os.path.dirname(__file__))


class WrapContract(object):
    """docstring for WrapContract The contract for this BOBA TEA"""

    def __init__(self, _network):
        nn1 = Tron().setNetwork(_network)
        if nn1.is_connected():
            self.tron_client = nn1
        else:
            print(
                "client v1 is not connected. please check the internet connection or the service is down! network: {}".format(
                    _network))

        self._tron_module = nn1.trx
        self._contract = None

    def getClientV1(self) -> "Tron":
        return self.tron_client

    def setMasterKey(self, pub: str, pri: str) -> "WrapContract":
        self.tron_client.private_key = pri
        self.tron_client.default_address = pub
        return self

    def loadContract(self, contract_metadata) -> "WrapContract":
        """
        Load and initiate contract interface by using the deployed contract json metadata
        """
        try:
            print("start loading {}".format(contract_metadata))
            contractDict = json.load(codecs.open(contract_metadata, 'r', 'utf-8-sig'))
            trn = contractDict["transaction"]
            hex_address = trn["contract_address"]
            self.transction_detail = contractDict
            self.trc_address = self.tron_client.address.from_hex(hex_address)
        except Exception as e:
            print("Problems from loading items from the file: ", e)
        self.init_internal_contract()

        return self

    def getTxID(self):
        return self.transction_detail["txid"]

    def init_internal_contract(self):
        """
        Initiate internal contract using the tronpytool contract factory object.
        """

        sol_contr = SolcWrap().WrapModel()
        _abi, _bytecode = sol_contr.GetCode("vault/tokenization/BobaToken.sol", "BobaToken")
        self._contract = self._tron_module.contract(address=self.trc_address, abi=_abi, bytecode=_bytecode)
        self._contract.functions.print_functions()



class SolcWrap(object):
    """docstring for SolcWrap"""
    outputfolder = "build"
    solfolder = ""
    file_name = "xxx.sol"
    prefixname = ""
    statement = 'End : {}, IO File {}'

    def __init__(self):
        super(SolcWrap, self).__init__()

    def SetOutput(self, path):
        self.outputfolder = path
        return self

    def SetSolPath(self, path):
        self.solfolder = path
        return self

    def BuildRemote(self):
        list_files = subprocess.run(["{}/solc_remote".format(ROOT)])
        print("The exit code was: %d" % list_files.returncode)
        return self

    def WrapModel(self):
        # path="{}/combinded.json".format(self.outputfolder)
        pathc = os.path.join(os.path.dirname(__file__), self.outputfolder, "combined.json")
        try:
            pathcli = codecs.open(pathc, 'r', 'utf-8-sig')
            self.combined_data = json.load(pathcli)
        except Exception as e:
            print("Problems from loading items from the file: ", e)
        return self

    def byClassName(self, path, classname):
        return "{prefix}:{name}".format(prefix=path, name=classname)

    def GetCode(self, fullname):
        return self.combined_data["contracts"][fullname]["abi"], self.combined_data["contracts"][fullname]["bin"]

    def GetCode(self, path, classname) -> [str, str]:
        return self.combined_data["contracts"][self.byClassName(path, classname)]["abi"], \
               self.combined_data["contracts"][self.byClassName(path, classname)]["bin"]

    def writeFile(self, content, filename):
        fo = open(filename, "w")
        fo.write(content)
        fo.close()
        print(self.statement.format(time.ctime(), filename))

    def StoreTxResult(self, tx_result_data, filepath):
        self.writeFile(json.dumps(tx_result_data, ensure_ascii=False), filepath)
