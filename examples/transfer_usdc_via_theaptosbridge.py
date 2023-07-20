import argparse

from aptos_sdk.account import Account
from aptos_sdk.client import RestClient

from src.apps.bridge import Bridge
from src.endpoint import Endpoint
from src.executor import Executor

WALLET_RPC = "https://fullnode.mainnet.aptoslabs.com/v1"


def get_usdc_balance_aptos_wallet(address: str) -> int:
    client = RestClient(WALLET_RPC)

    return int(client.account_resource(
        account_address=address,  # noqa
        resource_type="0x1::coin::CoinStore<0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa::asset::USDC>",
        # noqa
    )['data']['coin']['value'])


def transfer_usdc_via_theaptosbridge(private_key: str, evm_address: str, dst_chain_id: int, amount: int) -> str:
    client = RestClient(WALLET_RPC)
    account = Account.load_key(private_key)

    bridge = Bridge(private_key=private_key)
    endpoint = Endpoint(client)
    executor = Executor(client)
    adapter_params = executor.get_default_adapter_params(dst_chain_id)

    fee = endpoint.quote_fee(
        ua_address=account.address().hex(),
        dst_chain_id=dst_chain_id,
        adapter_params=adapter_params,
        payload_size=74,  # CONST
    )

    tx_hash = bridge.send_coin(
        amount=amount,
        dst_chain_id=dst_chain_id,
        dst_receiver=evm_address,
        fee=fee,
        adapter_params=adapter_params,
    )

    return tx_hash


def main(private_key: str, evm_address: str, dst_chain_id: int):
    account = Account.load_key(private_key)

    amount = get_usdc_balance_aptos_wallet(address=account.address().hex())
    tx_hash = transfer_usdc_via_theaptosbridge(
        private_key=private_key, evm_address=evm_address, dst_chain_id=dst_chain_id, amount=amount
    )
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Example code for transfers from Aptos chain to EVM chain via theaptosbridge."
    )
    parser.add_argument(
        "--private-key", type=str, required=True,
        help="Aptos chain private key",
    )
    parser.add_argument(
        "--evm-address", type=str, required=True,
        help="Destination EVM (Avalanche, Polygon, etc.) public key aka address",
    )
    parser.add_argument(
        "--dst-chain-id", type=int, required=True,
        help="Layerzero destination chain id, e.g. 106 is Avalanche",
    )

    args = parser.parse_args()
    main(
        private_key=args.private_key,
        evm_address=args.evm_address,
        dst_chain_id=args.dst_chain_id,
    )
