from datetime import date, datetime
from typing import TypedDict

class ClientCreateData(TypedDict):
    first_name: str
    last_name: str
    middle_name: str
    date_birthday: date
    address: str

class ClientData(ClientCreateData):
    id: int
    created_at: datetime
    updated_at: datetime
