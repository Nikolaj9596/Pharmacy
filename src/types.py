
from typing import Final
from pydantic import Field


STR_50: Final[str] = Field(max_length=50)
STR_255: Final[str] = Field(max_length=255)
POS_INT: Final[int] = Field(gt=0)
