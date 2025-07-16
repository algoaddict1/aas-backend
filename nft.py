import os
from algosdk.v2client import algod
from algosdk import mnemonic, transaction, account

ALGOD_TOKEN = os.getenv("ALGOD_TOKEN")
ALGOD_URL = os.getenv("ALGOD_URL")
MNEMONIC = os.getenv("WALLET_MNEMONIC")

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)
private_key = mnemonic.to_private_key(MNEMONIC)
public_address = account.address_from_private_key(private_key)

def mint_story_nft(story_text):
    params = algod_client.suggested_params()
    txn = transaction.AssetConfigTxn(
        sender=public_address,
        sp=params,
        total=1,
        default_frozen=False,
        unit_name="AAS",
        asset_name="Anonymous Story",
        manager=public_address,
        reserve=public_address,
        freeze=public_address,
        clawback=public_address,
        url="https://aas-backend.onrender.com",  # o frontend
        note=story_text.encode(),
        decimals=0
    )

    signed_txn = txn.sign(private_key)
    txid = algod_client.send_transaction(signed_txn)
    txinfo = transaction.wait_for_confirmation(algod_client, txid, 4)

    return txinfo["asset-index"]
