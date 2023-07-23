from aptos_sdk import ed25519
from aptos_sdk.account import Account
from aptos_sdk.authenticator import Authenticator, Ed25519Authenticator
from aptos_sdk.client import RestClient
from aptos_sdk.transactions import EntryFunction, TransactionPayload, RawTransaction, SignedTransaction
from aptos_sdk.client import ApiError

from src.const import APTOS_RPC
from src.sdk.base_sdk import BaseSdk

from typing import Any, Dict


class AptosSdk(BaseSdk):
    def __init__(self, private_key: str | None = None):
        self.account = Account.load_key(private_key) if private_key else None
        self.client = RestClient(APTOS_RPC)

    def send_and_submit_transaction(self, payload: EntryFunction) -> str:
        GAS_SAFETY_FACTOR = 0.2
        raw_transaction = self.client.create_bcs_transaction(
            self.account, TransactionPayload(payload)
        )

        simulated_transaction = self.simulate_transaction_with_gas_estimate(
            transaction=raw_transaction,
            sender=self.account
        )

        if not simulated_transaction[0]["success"]:  # noqa
            raise ValueError(simulated_transaction[0]["vm_status"])  # noqa
        raw_transaction.max_gas_amount = int(int(simulated_transaction[0]['gas_used'], base=10) * (1 + GAS_SAFETY_FACTOR))
        signed_transaction = self.client.create_bcs_signed_transaction(
            self.account, TransactionPayload(payload)
        )
        txn = self.client.submit_bcs_transaction(signed_transaction)
        self.client.wait_for_transaction(txn)

        return txn

    def simulate_transaction_with_gas_estimate(
    self,
        transaction: RawTransaction,
        sender: Account,
    ) -> Dict[str, Any]:
        authenticator = Authenticator(
            Ed25519Authenticator(
                sender.public_key(),
                ed25519.Signature(b"\x00" * 64),
            )
        )
        signed_transaction = SignedTransaction(transaction, authenticator)
        params = {'estimate_gas_unit_price': True,
                  'estimate_max_gas_amount': True}
        headers = {"Content-Type": "application/x.aptos.signed_transaction+bcs"}
        response = self.client.client.post(
            f"{self.client.base_url}/transactions/simulate",
            headers=headers,
            content=signed_transaction.bytes(),
            params=params
        )
        if response.status_code >= 400:
            raise ApiError(response.text, response.status_code)

        return response.json()

    
