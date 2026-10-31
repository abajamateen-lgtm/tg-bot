import os
import sys
from web3 import Web3
from eth_account import Account

# Enable mnemonic seed phrase support
Account.enable_unaudited_hdwallet_features()

secret_input = os.getenv("WALLET_PRIVATE_KEY")

if not secret_input:
    print("Error: WALLET_PRIVATE_KEY secret is missing!")
    sys.exit(1)

secret_input = secret_input.strip()

# Check if input is a 12-word seed phrase or a private key
if len(secret_input.split()) >= 12:
    try:
        account = Account.from_mnemonic(secret_input)
        wallet_address = account.address
        print(f"Loaded wallet address from seed phrase: {wallet_address}")
    except Exception as e:
        print(f"Error reading seed phrase: {e}")
        sys.exit(1)
else:
    if not secret_input.startswith('0x'):
        secret_input = '0x' + secret_input
    try:
        account = Account.from_key(secret_input)
        wallet_address = account.address
        print(f"Loaded wallet address from private key: {wallet_address}")
    except Exception as e:
        print(f"Error reading private key: {e}")
        sys.exit(1)

NETWORKS = {
    "Optimism Sepolia": "https://sepolia.optimism.io",
    "Arbitrum Sepolia": "https://sepolia-rollup.arbitrum.io/rpc",
    "Base Sepolia": "https://sepolia.base.org"
}

print("\n--- STARTING MULTI-NETWORK BALANCE CHECK ---")
for name, rpc_url in NETWORKS.items():
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={'timeout': 10}))
        if w3.is_connected():
            balance_wei = w3.eth.get_balance(wallet_address)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            print(f"[{name}] Connected | Balance: {balance_eth} ETH")
        else:
            print(f"[{name}] Could not connect to RPC, skipping...")
    except Exception as e:
        print(f"[{name}] Network check skipped: {e}")

print("--- MULTI-NETWORK TASK COMPLETED ---\n")
