from aptos_sdk.account import Account
from aptos_sdk.client import RestClient
from aptos_sdk.transactions import EntryFunction, TransactionPayload

from src.const import APTOS_RPC
from src.sdk.base_sdk import BaseSdk


class AptosSdk(BaseSdk):
    def __init__(self, private_key: str | None = None):
        self.account = Account.load_key(private_key) if private_key else None
        self.client = RestClient(APTOS_RPC)

    def send_and_submit_transaction(self, payload: EntryFunction) -> str:
        raw_transaction = self.client.create_bcs_transaction(
            self.account, TransactionPayload(payload)
        )

        simulated_transaction = self.client.simulate_transaction(
            transaction=raw_transaction,
            sender=self.account
        )

        if not simulated_transaction[0]["success"]:  # noqa
            raise ValueError(simulated_transaction[0]["vm_status"])  # noqa

        signed_transaction = self.client.create_bcs_signed_transaction(
            self.account, TransactionPayload(payload)
        )
        txn = self.client.submit_bcs_transaction(signed_transaction)
        self.client.wait_for_transaction(txn)

        return txn
