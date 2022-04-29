from .constants import w3
from .erc721_abi import erc721_abi


class Erc721Contract:
    def __init__(self, contract_address):
        self.contract = w3.eth.contract(address=contract_address, abi=erc721_abi)

    def name(self):
        try:
            return self.contract.functions.name().call()
        except:
            return None

    def token_uri(self, i):
        try:
            i = int(i)
            return self.contract.functions.tokenURI(i).call()
        except:
            return None