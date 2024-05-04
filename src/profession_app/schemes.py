from datetime import datetime
from pydantic import Field

from src.models import BaseScheme


class ProfessionCreateScheme(BaseScheme):
    name: str = Field(max_length=255)


class ProfessionScheme(ProfessionCreateScheme):
    id: int
    created_at: datetime
    updated_at: datetime


class ProfessionDetailScheme(ProfessionScheme):
    number_of_specialists: int
