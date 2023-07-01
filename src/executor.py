from aptos_sdk.client import RestClient


class Executor:
    executor_address = '0x1d8727df513fa2a8785d0834e40b34223daff1affc079574082baadb74b66ee4'
    oracle_address = '0x12e12de0af996d9611b0b78928cd9f4cbf50d94d972043cdd829baa77a78929b'
    layerzero_address = '0x54ad3d30af77b60d939ae356e6606de9a4da67583f02b962d2d3f2e481484e90'
    module = f'{layerzero_address}::executor_v1'
    module_name = 'layerzero::executor_v1'
    type = f'${module}::Executor'

    def __init__(self, sdk: RestClient):
        self.sdk = sdk

    def decode_adapter_params(self, adapter_params: str):
        raise NotImplementedError

    def get_default_adapter_params(self, executor: str, dst_chain_id: int):
        resource = self.sdk.account_resource(
            executor,
            f"{self.layerzero_address}::executor_v1::AdapterParamsConfig"
        )

        response = self.sdk.get_table_item(
            resource['data']['params']['handle'],
            'u64',
            'vector<u8>',
            str(dst_chain_id)
        )

        return response

    def get_fee(self, executor: str, dst_chain_id: str):
        resource = self.sdk.account_resource(
            executor,
            f"{self.layerzero_address}::executor_v1::ExecutorConfig"
        )

        response = self.sdk.get_table_item(
            resource['data']['fee']['handle'],
            'u64',
            f'{self.module}::Fee',
            str(dst_chain_id)
        )

        return {
            "airdrop_amt_cap": response['airdrop_amt_cap'],
            "gas_price": response["gas_price"],
            "price_ratio": response["price_ratio"]
        }

    def quote_fee(self, executor: str, dst_chain_id: int, adapter_params: None | list) -> int:
        if not adapter_params:
            adapter_params = self.get_default_adapter_params(
                self.layerzero_address, dst_chain_id
            )

        fee = self.get_fee(self.executor_address, dst_chain_id)
        _, ua_gas, airdrop_amount = self.decode_adapter_params(adapter_params)

        return ((ua_gas * fee['gas_price'] + airdrop_amount) * fee['price_ratio']) / 10000000000
