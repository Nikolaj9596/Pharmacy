from datetime import date, datetime
from typing import Annotated
from src.models import BaseScheme

from src.types import POS_INT, STR_255, STR_50


class ClientCreateScheme(BaseScheme):
    first_name: Annotated[str, STR_50]
    last_name: Annotated[str, STR_50]
    middle_name: Annotated[str, STR_50]
    date_birthday: date
    address: Annotated[str, STR_255]
    avatar: str | None = None


class ClientScheme(ClientCreateScheme):
    id: Annotated[int, POS_INT]
    created_at: datetime
    updated_at: datetime
