from fastapi import FastAPI, HTTPException
from ecdsa import VerifyingKey
from .schemas import TTNData
from .services.decode_info import EcdsaService
import json
import ecdsa
import requests
import os
app = FastAPI()


@app.post("/")
async def webhook_ttn(ttn_data: TTNData):
    ecdsa_service = EcdsaService()
    key = ecdsa_service.get_device_public_key(device_id=ttn_data.device_id)
    if key is None:
        raise HTTPException(status_code=404, detail="device not found")

    verifying_key = ecdsa.VerifyingKey.from_string(bytearray.fromhex(key))
    # Data signature from ttn given by the edge component
    data_signature = bytearray.fromhex(ttn_data.hash)

    try:
        verifying_key.verify(data_signature, json.dumps(
            ttn_data.data).encode("utf-8"))
        r = requests.post(os.getenv("PROCESS_MICROSERVICE"), json={
            "device_id": ttn_data.device_id,
            "hash": ttn_data.hash,
            "data": ttn_data.data
        })
        if r.status_code != 200:
            return False
        return True
    except ecdsa.keys.BadSignatureError:
        raise HTTPException(status_code=400, detail={"error": "Bad Signature"})
