import asyncio
import base64
import json

import discord
import requests
import websockets
from web3 import Web3

from utils.Erc1155Contract import Erc1155Contract
from utils.Erc721Contract import Erc721Contract
from utils.constants import w3, NETWORK, ALCHEMY_API_KEY, DISCORD_CHANNEL, DISCORD_TOKEN, COLLECTION_TYPE, COLLECTION_ADDRESS, WEBSITE_URL, EXCHANGE_CONTRACT, ERC_721_SAFE_TRANSFER_TOPIC, ERC_1155_SAFE_TRANSFER_TOPIC


client = discord.Client()

@client.event
async def on_ready():
    print("Connected to Discord")
    await alchemy_websocket()

@client.event
async def on_error(self):
    print("Caught discord error")


def pull_metadata(contract, token_id):
    metadata_uri = contract.token_uri(token_id)
    if not metadata_uri:
        return

    ipfs_prefix = "ipfs://"
    if metadata_uri.startswith(ipfs_prefix):
        try:
            r = requests.get(f"https://ipfs.io/ipfs/{metadata_uri[len(ipfs_prefix):]}")
            metadata_str = r.text
            metadata = json.loads(metadata_str)
        except json.JSONDecodeError:
            metadata = {}
    elif metadata_uri.startswith("data:application/json;base64"):
        prefix, msg = metadata_uri.split(",")
        metadata = json.loads(base64.b64decode(msg))
    else:
        try:
            r = requests.get(metadata_uri)
            metadata = json.loads(r.text)
        except:
            return None

    return metadata


async def send_discord_message(transfer_event):
    transfer_txn_id = transfer_event["transactionHash"]
    full_txn = w3.eth.get_transaction(transfer_txn_id)

    if not full_txn['to'] == EXCHANGE_CONTRACT:
        return

    amount = Web3.fromWei(full_txn["value"], "ether")

    if amount == 0:
        print(f"Transaction value is 0")
        return

    amount = str(amount) + " ETH"

    contract_address = Web3.toChecksumAddress(transfer_event['address'])
    func_hash, *other_topics = transfer_event['topics']

    if func_hash == ERC_721_SAFE_TRANSFER_TOPIC:
        contract = Erc721Contract(contract_address)
        from_bytes, to_bytes, token_id_bytes = other_topics
        token_id = int(token_id_bytes, 16)
    elif func_hash == ERC_1155_SAFE_TRANSFER_TOPIC:
        contract = Erc1155Contract(contract_address)
        token_id, quantity = int(transfer_event['data'][:66], 16), int(transfer_event['data'][66:], 16)

    metadata = pull_metadata(contract, token_id)
    if not metadata:
        print(f"Could not pull metadata")
        return

    name = metadata.get("name")
    if not name:
        try:
            contract_name = contract.name()
            name = f"{contract_name} #{token_id}"
        except:
            print(f"Name missing from metadata")
            return

    url = f"{WEBSITE_URL}/asset/{contract_address}/{token_id}"
    message = f"{name} sold for {amount}: {url}"

    channel = client.get_channel(int(DISCORD_CHANNEL))
    await channel.send(message)


async def alchemy_websocket():
    ws_url = f"wss://{NETWORK}.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
    async with websockets.connect(ws_url) as websocket:
        if COLLECTION_TYPE == '721':
            req = f'{{"jsonrpc":"2.0","id": 1, "method": "eth_subscribe", "params": ["logs", {{"address": "{COLLECTION_ADDRESS}", "topics": ["{ERC_721_SAFE_TRANSFER_TOPIC}"]}}]}}'
        elif COLLECTION_TYPE == '1155':
            req = f'{{"jsonrpc":"2.0","id": 1, "method": "eth_subscribe", "params": ["logs", {{"address": "{COLLECTION_ADDRESS}", "topics": ["{ERC_1155_SAFE_TRANSFER_TOPIC}"]}}]}}'
        else:
            return

        await websocket.send(req)

        async for message_str in websocket:
            message = json.loads(message_str)
            params = message.get('params')
            if params:
                transfer_event = params['result']
                asyncio.create_task(send_discord_message(transfer_event))

asyncio.run(client.run(DISCORD_TOKEN, reconnect=True))