import os
import requests
import json


class EcdsaService(object):
    def __init__(self) -> None:
        self.decode_microservice = os.environ.get("DECODE_MICROSERVICE_URL")

    def get_device_public_key(self, device_id: str):
        """
        Query the ecdsa microservice to return the private keys of the device
        """
        key_request = requests.get(
            f"{self.decode_microservice}query?type=public&device_id={device_id}"
        )
        if key_request.status_code == 200:
            public_key = json.loads(key_request.content.decode("UTF-8"))
            return public_key.get("data")
        elif key_request.status_code == 404:
            return None
