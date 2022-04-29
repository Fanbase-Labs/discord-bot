import os

from web3 import Web3

NETWORK = os.environ.get("NETWORK", "opt-mainnet")  # Required: opt-mainnet or arb-mainnet
ALCHEMY_API_KEY = os.environ.get("ALCHEMY_API_KEY")  # Required: your (free) Alchemy API key

# https://github.com/0xEssential/opensea-discord-bot#prerequisites
DISCORD_CHANNEL = os.getenv('DISCORD_CHANNEL')  # Required
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')  # Required

COLLECTION_TYPE = os.environ.get("COLLECTION_TYPE", "721")  # Required: 721 or 1155
COLLECTION_ADDRESS = os.environ.get("COLLECTION_ADDRESS")  # Required: your contract address

if NETWORK == "opt-mainnet":
    WEBSITE_URL = "https://quixotic.io"
    EXCHANGE_CONTRACT = "0x282619dB98F8a43E98065F5B306aE740d6d87a84"
elif NETWORK == "arb-mainnet":
    WEBSITE_URL = "https://stratosnft.io"
    EXCHANGE_CONTRACT = "0x282619dB98F8a43E98065F5B306aE740d6d87a84"

ERC_721_SAFE_TRANSFER_TOPIC = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
ERC_1155_SAFE_TRANSFER_TOPIC = "0xc3d58168c5ae7397731d063d5bbf3d657854427343f4c083240f7aacaa2d0f62"

ALCHEMY_URL = f"https://{NETWORK}.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))
