from aptos_sdk.account import Account
from aptos_sdk.client import RestClient
from aptos_sdk.transactions import EntryFunction, TransactionPayload

from src.const import APTOS_RPC
from src.sdk.base_sdk import BaseSdk


class ClientConfig:
    """Common configuration for clients, particularly for submitting transactions"""

    expiration_ttl: int = 600
    gas_unit_price: int = 100
    max_gas_amount: int = 50_000
    transaction_wait_in_seconds: int = 20


class AptosSdk(BaseSdk):
    def __init__(self, private_key: str | None = None):
        self.account = Account.load_key(private_key) if private_key else None
        self.client = RestClient(base_url=APTOS_RPC, client_config=ClientConfig())

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
