const lz_aptos = require('@layerzerolabs/lz-aptos')
const aptos = require('aptos')

const CHAIN_ID = 110;

const lzSdk = new lz_aptos.SDK({
    provider: new aptos.AptosClient("https://mainnet.aptoslabs.com/v1"),
    stage: 0
})

const printFee = async () => {
    const fee = await lzSdk.LayerzeroModule.Endpoint.quoteFee(
        "0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa",
        CHAIN_ID,
        Uint8Array.from([0, 1, 0,0,0 , 0 , 0, 22 ,  227, 96]),
        74
    )
    console.log('Final fee=', fee)
}

const getAdapterParams = async () => {
    const e = await lzSdk.LayerzeroModule.Executor.getDefaultAdapterParams(CHAIN_ID)
    console.log('raw params', e)
    const dp = lzSdk.LayerzeroModule.Executor.decodeAdapterParams(e)
    console.log(dp)
}

printFee()