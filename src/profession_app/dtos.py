
from datetime import datetime
from typing import TypedDict

class ProfessionDataCreate(TypedDict):
    name: str

class ProfessionDataGet(TypedDict):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime
