import os
import sys
from web3 import Web3

private_key = os.getenv("WALLET_PRIVATE_KEY")

if not private_key:
    print("Error: WALLET_PRIVATE_KEY secret is missing!")
    sys.exit(1)

# Derive public address safely from private key
try:
    w3_temp = Web3()
    account = w3_temp.eth.account.from_key(private_key)
    wallet_address = account.address
    print(f"Successfully loaded wallet address: {wallet_address}")
except Exception as e:
    print(f"Error parsing private key: {e}")
    sys.exit(1)

# Define public RPC endpoints for multi-network checks
NETWORKS = {
    "Optimism Sepolia": "https://sepolia.optimism.io",
    "Arbitrum Sepolia": "https://sepolia-rollup.arbitrum.io/rpc",
    "Base Sepolia": "https://sepolia.base.org"
}

print("\n--- STARTING MULTI-NETWORK BALANCE CHECK ---")
for name, rpc_url in NETWORKS.items():
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if w3.is_connected():
            balance_wei = w3.eth.get_balance(wallet_address)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            print(f"[{name}] Connected | Balance: {balance_eth} ETH")
        else:
            print(f"[{name}] Failed to connect to RPC node.")
    except Exception as e:
        print(f"[{name}] Error checking balance: {e}")

print("--- MULTI-NETWORK TASK COMPLETED ---\n")
