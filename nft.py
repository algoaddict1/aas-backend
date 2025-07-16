import os
from algosdk.v2client import algod
from algosdk import mnemonic, transaction, account
from dotenv import load_dotenv

load_dotenv()

ALGOD_TOKEN = os.getenv("ALGOD_TOKEN")
ALGOD_URL = os.getenv("ALGOD_URL")
MNEMONIC = os.getenv("WALLET_MNEMONIC")

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_URL)

def mint_story_nft(story_text):
    print("🔨 Avvio minting NFT...")
    try:
        private_key = mnemonic.to_private_key(MNEMONIC)
        public_address = account.address_from_private_key(private_key)
        print("👛 Address:", public_address)

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
            url="https://aas-backend.onrender.com",
            note=story_text.encode(),
            decimals=0
        )

        signed_txn = txn.sign(private_key)
        txid = algod_client.send_transaction(signed_txn)
        print("📤 TX inviata, ID:", txid)

        txinfo = transaction.wait_for_confirmation(algod_client, txid, 4)
        asset_id = txinfo["asset-index"]
        print("✅ NFT creato con ID:", asset_id)

        return asset_id

    except Exception as e:
        print("❌ ERRORE MINTING NFT:", str(e))
        raise
