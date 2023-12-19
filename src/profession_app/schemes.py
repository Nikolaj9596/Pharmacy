from datetime import datetime
from pydantic import BaseModel, Field


class ProfessionCreateScheme(BaseModel):
    name: str = Field(max_length=255)

class ProfessionScheme(ProfessionCreateScheme):
    id: int
    created_at: datetime
    updated_at: datetime

class ProfessionDetailScheme(ProfessionScheme):
    number_of_specialists: int
