from aptos_sdk.account import Account
from aptos_sdk.client import RestClient
from aptos_sdk.type_tag import TypeTag, StructTag
from aptos_sdk.transactions import EntryFunction, TransactionPayload


class Bridge:
    WALLET_RPC = "https://fullnode.mainnet.aptoslabs.com/v1"
    BRIDGE_ADDRESS = "0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa"

    def __init__(self, private_key: str):
        self.account = Account.load_key(private_key)
        self.sdk = RestClient(self.WALLET_RPC)
        self.module = f'{self.BRIDGE_ADDRESS}::coin_bridge'
        self.module_name = 'bridge::coin_bridge'
        self.ua_type = f'{self.BRIDGE_ADDRESS}::coin_bridge::BridgeUA'

    def get_send_coin_payload(self, coin, dst_chain_id, dst_receiver, amount, native_fee, zro_fee, unwrap, adapter_params, msglib_pararms):
        return {
            "module": self.module,
            "function": f"{self.module}::send_coin_from",
            "type_arguments": [coin],
            "arguments": [
                str(dst_chain_id),
                dst_receiver,
                str(amount),
                str(native_fee),
                str(zro_fee),
                str(unwrap),
                adapter_params,
                msglib_pararms,
            ]
        }

    def send_coin(self, amount, dst_chain_id, dst_receiver, fee, adapter_params):
        send_coin_payload = self.get_send_coin_payload(
            coin="USDC",
            dst_chain_id=dst_chain_id,
            dst_receiver=dst_receiver,
            amount=amount,
            native_fee=fee,
            zro_fee=0,
            unwrap="false",
            adapter_params=adapter_params,
            msglib_pararms=[],
        )

        payload = EntryFunction.natural(
            send_coin_payload["module"],
            send_coin_payload["function"],
            ["USDC", ],
            send_coin_payload["arguments"],
        )

        # raw_transaction = self.sdk.create_bcs_transaction(
        #     self.account, TransactionPayload(payload)
        # )
        simulated_transacation = self.sdk.simulate_transaction(payload, self.account)
        print(f"Симуляция транзакции: {simulated_transacation}")

        if not simulated_transacation[0]["success"]:
            raise ValueError(simulated_transacation[0]["vm_status"])

        signed_transaction = self.sdk.create_bcs_signed_transaction(
            self.account, payload
        )
        txn = self.sdk.submit_bcs_transaction(signed_transaction)
        self.sdk.wait_for_transaction(txn)

        return txn


'''
How to:
    bridge = Bridge(private_key=*****)
    sdk = RestClient(RPC_URL)
    executor = Executor(sdk)
    endpoint = Endpoint(sdk)
    
    adapter_params = executor.get_default_adapter_params(110)  # 110 is chain
    fee = endpoint.quote_fee(
        ua_address=wallet.address,
        dst_chain_id=106,  # Avalanche?
        adapter_params=adapter_params,
        payload_size=74,  # CONST
    )

    bridge.send_coin(
        amount=10000000,  # 10 USDC
        dst_chain_id=106,  # Avalanche?
        dst_receiver=evm_wallet_address,  # Не уверен че за пар-р, методом тыка
        fee=fee,
        adapter_params=adapter_params,
    )
'''