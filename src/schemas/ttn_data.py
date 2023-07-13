from pydantic import BaseModel


class TTNData(BaseModel):
    device_id: str
    data: dict
    hash: str
