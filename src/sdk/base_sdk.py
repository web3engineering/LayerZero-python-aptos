from abc import ABC

from aptos_sdk.transactions import EntryFunction


class BaseSdk(ABC):
    def __int__(self, private_key: str | None = None): ...

    def send_and_submit_transaction(self, payload: EntryFunction) -> str: ...
