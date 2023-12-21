
from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel

from src.types import STR_255


class CategoryDiseaseCreateScheme(BaseModel):
    name: Annotated[str, STR_255]

class CategoryDiseaseScheme(CategoryDiseaseCreateScheme):
    id: int
    created_at: datetime
    updated_at: datetime

class DiseaseCreateScheme(BaseModel):
    name: Annotated[str, STR_255]
    description: Optional[str]
    category_disease_id: int

class DiseaseScheme(DiseaseCreateScheme):
    id: int
    created_at: datetime
    updated_at: datetime

class DiagnosisCreateScheme(BaseModel):
    name: Annotated[str, STR_255]
    description: Optional[str]
    status: str
    client_id: int
    doctor_id: int
    date_closed: Optional[datetime]

class DiagnosisScheme(DiagnosisCreateScheme):
    id: int
    created_at: datetime
    updated_at: datetime
