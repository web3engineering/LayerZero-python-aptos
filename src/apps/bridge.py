import binascii

from aptos_sdk.account import Account
from aptos_sdk.client import RestClient
from aptos_sdk.type_tag import TypeTag, StructTag
from aptos_sdk.bcs import Serializer
from aptos_sdk.transactions import EntryFunction, TransactionPayload, TransactionArgument


class Bridge:
    WALLET_RPC = "https://fullnode.mainnet.aptoslabs.com/v1"
    BRIDGE_ADDRESS = "0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa"

    def __init__(self, private_key: str):
        self.account = Account.load_key(private_key)
        self.sdk = RestClient(self.WALLET_RPC)
        self.module = f'{self.BRIDGE_ADDRESS}::coin_bridge'
        self.module_name = 'bridge::coin_bridge'
        self.ua_type = f'{self.BRIDGE_ADDRESS}::coin_bridge::BridgeUA'

    def get_send_coin_payload(
            self,
            dst_chain_id: int,
            dst_receiver: str,
            amount: int,
            native_fee: int,
            zro_fee: int,
            unwrap: bool,
            adapter_params: str,
            msglib_pararms: list[str]
    ):
        dst_receiver = dst_receiver[2:].rjust(64, "0")
        adapter_params = adapter_params[2:]
        return {
            "module": self.module,
            "function": "send_coin_from",
            "type_arguments": [TypeTag(StructTag.from_str(f'{self.BRIDGE_ADDRESS}::asset::USDC'))],
            "arguments": [
                TransactionArgument(dst_chain_id, Serializer.u64),
                TransactionArgument(list(binascii.unhexlify(dst_receiver)), Serializer.sequence_serializer(Serializer.u8)),
                TransactionArgument(amount, Serializer.u64),
                TransactionArgument(int(native_fee) * 2, Serializer.u64),
                TransactionArgument(int(zro_fee), Serializer.u64),
                TransactionArgument(unwrap, Serializer.bool),
                TransactionArgument(list(binascii.unhexlify(adapter_params)), Serializer.sequence_serializer(Serializer.u8)),
                TransactionArgument(msglib_pararms, Serializer.sequence_serializer(Serializer.u8)),
            ]
        }

    def send_coin(self, amount, dst_chain_id, dst_receiver, fee, adapter_params):
        send_coin_payload = self.get_send_coin_payload(
            dst_chain_id=dst_chain_id,
            dst_receiver=dst_receiver,
            amount=amount,
            native_fee=fee,
            zro_fee=0,
            unwrap=False,
            adapter_params=adapter_params,
            msglib_pararms=[],
        )

        payload = EntryFunction.natural(
            send_coin_payload["module"],
            send_coin_payload["function"],
            send_coin_payload["type_arguments"],
            send_coin_payload["arguments"],
        )

        raw_transaction = self.sdk.create_bcs_transaction(
            self.account, TransactionPayload(payload)
        )

        simulated_transacation = self.sdk.simulate_transaction(
            transaction=raw_transaction,
            sender=self.account
        )

        if not simulated_transacation[0]["success"]:
            raise ValueError(simulated_transacation[0]["vm_status"])

        signed_transaction = self.sdk.create_bcs_signed_transaction(
            self.account, TransactionPayload(payload)
        )
        txn = self.sdk.submit_bcs_transaction(signed_transaction)
        self.sdk.wait_for_transaction(txn)

        return txn
