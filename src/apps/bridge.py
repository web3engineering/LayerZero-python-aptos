from aptos_sdk.client import RestClient


class Bridge:
    def __init__(self, sdk: RestClient):
        self.sdk = sdk
        self.module = f'{address}::coin_bridge'
        self.module_name = 'bridge::coin_bridge'
        self.ua_type = f'{address}::coin_bridge::BridgeUA'

#     def get_send_coin_payload(self, ):
#         return {
#             function: `${this.module}::send_coin_from`,
#         type_arguments: [this.coin.getCoinType(coin)],
#         arguments: [
#             dstChainId.toString(),
#             Array.from(dstReceiver),
#         amountLD.toString(),
#         nativeFee.toString(),
#         zroFee.toString(),
#         unwrap.toString(),
#         Array.from(adapterParams),
#         Array.from(msglibPararms),
#         ],
#         };
#         }
#
#     def send_coin(self):
#         send_coin_payload = self.get_send_coin_payload()
#
#         sendCoinPayload(coin, dstChainId, dstReceiver, amountLD, nativeFee, zroFee, unwrap, adapterParams, msglibPararms) {
#
#     async sendCoin(signer, coin, dstChainId, dstReceiver, amountLD, nativeFee, zroFee, unwrap, adapterParams, msglibParams) {
#     const transaction = this.sendCoinPayload(coin, dstChainId, dstReceiver, amountLD, nativeFee, zroFee, unwrap, adapterParams, msglibParams);
#     return this.sdk.sendAndConfirmTransaction(signer, transaction);
# }