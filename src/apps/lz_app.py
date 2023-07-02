from aptos_sdk.client import RestClient


class LzApp:
    def __init__(self, sdk: RestClient):
        self.sdk = sdk
