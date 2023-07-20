import binascii

from aptos_sdk.bcs import Serializer
from aptos_sdk.transactions import EntryFunction, TransactionArgument
from aptos_sdk.type_tag import TypeTag, StructTag

from src.const import BRIDGE_ADDRESS, MAINNET
from src.sdk.aptos_sdk import AptosSdk
from src.utils import get_u64_raw_address, get_raw_address


class Bridge:
    BRIDGE_ADDRESS = BRIDGE_ADDRESS[MAINNET]

    def __init__(self, private_key: str):
        self.sdk = AptosSdk(private_key=private_key)
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
            msglib_params: list[str]
    ):
        dst_receiver = get_u64_raw_address(dst_receiver)
        adapter_params = get_raw_address(adapter_params)  # adapter_params has HEX format, 0x000000000
        return {
            "module": self.module,
            "function": "send_coin_from",
            "type_arguments": [TypeTag(StructTag.from_str(f'{self.BRIDGE_ADDRESS}::asset::USDC'))],
            "arguments": [
                TransactionArgument(
                    dst_chain_id, Serializer.u64  # noqa
                ),
                TransactionArgument(
                    list(binascii.unhexlify(dst_receiver)), Serializer.sequence_serializer(Serializer.u8)  # noqa
                ),
                TransactionArgument(
                    amount, Serializer.u64  # noqa
                ),
                TransactionArgument(
                    int(native_fee), Serializer.u64  # noqa
                ),
                TransactionArgument(
                    int(zro_fee), Serializer.u64  # noqa
                ),
                TransactionArgument(
                    unwrap, Serializer.bool  # noqa
                ),
                TransactionArgument(
                    list(binascii.unhexlify(adapter_params)), Serializer.sequence_serializer(Serializer.u8)  # noqa
                ),
                TransactionArgument(
                    msglib_params, Serializer.sequence_serializer(Serializer.u8)  # noqa
                ),
            ]
        }

    def get_claim_coin_payload(self):
        return {
            "module": self.module,
            "function": "claim_coin",
            "type_arguments": [
                TypeTag(
                    StructTag.from_str(
                        f"{self.BRIDGE_ADDRESS}::asset::USDC"
                    )),
            ],
            "arguments": [],
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
            msglib_params=[],
        )

        payload = EntryFunction.natural(
            send_coin_payload["module"],
            send_coin_payload["function"],
            send_coin_payload["type_arguments"],
            send_coin_payload["arguments"],
        )

        return self.sdk.send_and_submit_transaction(payload)

    def claim_coin(self):
        claim_coin_payload = self.get_claim_coin_payload()

        payload = EntryFunction.natural(
            claim_coin_payload["module"],
            claim_coin_payload["function"],
            claim_coin_payload["type_arguments"],
            claim_coin_payload["arguments"],
        )

        return self.sdk.send_and_submit_transaction(payload)
