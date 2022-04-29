from .constants import w3
from .erc1155_abi import erc1155_abi


class Erc1155Contract:
    def __init__(self, contract_address):
        self.contract = w3.eth.contract(address=contract_address, abi=erc1155_abi)

    def name(self):
        try:
            return self.contract.functions.name().call()
        except:
            return None

    def token_uri(self, i):
        try:
            i = int(i)
            return self.contract.functions.uri(i).call()
        except:
            return None
