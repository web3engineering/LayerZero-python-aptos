from aptos_sdk.client import RestClient
from executor import Executor
from endpoint import Endpoint
import binascii

rest_client = RestClient("https://mainnet.aptoslabs.com/v1")

# We are trying to mimic the most basic thing: 
# https://github.com/LayerZero-Labs/LayerZero-Aptos-Contract/blob/991a2f250d1445d98b83cdbea6751c08b60fb3e0/sdk/src/modules/uln/uln_signer.ts#L120

# const resource = await this.sdk.client.getAccountResource(address, `${this.module}::Config`);
# const { fees } = resource.data;
# const response = await this.sdk.client.getTableItem(fees.handle, {
#     key_type: `u64`,
#     value_type: `${this.module}::Fee`,
#     key: dstChainId.toString(),
# });
# console.log("RETURNING", response.base_fee, response.fee_per_byte)
# return {
#     base_fee: BigInt(response.base_fee),
#     fee_per_byte: BigInt(response.fee_per_byte),
# };

# Logs were:
# SIGNER GET FEE 0x12e12de0af996d9611b0b78928cd9f4cbf50d94d972043cdd829baa77a78929b 110
# RETURNING 19139828 0
# SIGNER GET FEE 0x1d8727df513fa2a8785d0834e40b34223daff1affc079574082baadb74b66ee4 110
# RETURNING 19139828 3

DEST_CHAIN = 110

def test():

    # Account owns resources. 0x12 is account, 0x54 is a resource_type.
    # You can find resources associated with accounts here:
    # https://explorer.aptoslabs.com/account/0x1d8727df513fa2a8785d0834e40b34223daff1affc079574082baadb74b66ee4/resources?network=mainnet
    r1 = rest_client.account_resource(
        "0x12e12de0af996d9611b0b78928cd9f4cbf50d94d972043cdd829baa77a78929b",
        "0x54ad3d30af77b60d939ae356e6606de9a4da67583f02b962d2d3f2e481484e90::uln_signer::Config")

    # as a result we are getting a resource HANDLE - this is a way to READ resource (table)
    # where fee is stored
    print(r1)

    r1_table = rest_client.get_table_item(
        r1['data']['fees']['handle'],
        'u64',
        "0x54ad3d30af77b60d939ae356e6606de9a4da67583f02b962d2d3f2e481484e90::uln_signer::Fee",
        str(DEST_CHAIN)
    )

    print(r1_table)

    # Same here. Generally, L0 has two accounts (oracle + executor), 
    # and we are reading fees from them.
    r2 = rest_client.account_resource(
        "0x1d8727df513fa2a8785d0834e40b34223daff1affc079574082baadb74b66ee4",
        "0x54ad3d30af77b60d939ae356e6606de9a4da67583f02b962d2d3f2e481484e90::uln_signer::Config"
    )

    print(r2)

    r2_table = rest_client.get_table_item(
        r2['data']['fees']['handle'],
        'u64',
        "0x54ad3d30af77b60d939ae356e6606de9a4da67583f02b962d2d3f2e481484e90::uln_signer::Fee",
        str(DEST_CHAIN)
    )

    print(r2_table)

ep = Endpoint(rest_client)
print('final fee=', ep.quote_fee(
        "0xf22bede237a07e121b56d91a491eb7bcdfd1f5907926a9e58338f964a01b17fa",
        DEST_CHAIN,
        "0x" + binascii.hexlify(bytes([0, 1, 0,0,0 , 0 , 0, 22 ,  227, 96])).decode('ascii'),
        74
))